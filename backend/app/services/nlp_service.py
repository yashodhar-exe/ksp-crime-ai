import json
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.models.case_master import CaseMaster
from app.schemas.chat import ChatQueryResponse, ChatSource
from app.models.lookups import Unit, District, CrimeHead
from app.services import chat_store
from app.db.session import SessionLocal

# Setup Google GenAI via REST (to avoid grpcio memory crash on Catalyst)
import httpx

if settings.OPENAI_OR_LLM_API_KEY:
    # Key is set in app-config.json for production
    pass

SYSTEM_PROMPT = """You are the KSP Crime AI Assistant, a specialized AI for Karnataka State Police.
Your sole purpose is to help police officers query the case database.
Strictly refuse to answer any questions outside of the context of KS police, crimes, cases, or related policing matters.
If asked about coding, general knowledge, or other topics, say: "I am authorized only to assist with KS police data."

You have access to a PostgreSQL database with the following schema:
- case_master (crime_no, case_no, crime_registered_date, police_station_id, crime_major_head_id, case_status_id, incident_from_date)
- crime_head (crime_head_id, head_name, crime_group_name)
- unit (unit_id, unit_name, district_id)
- district (district_id, district_name)
- case_status_master (case_status_id, case_status_name)

When the user asks for trending crimes, specific cases, or counts, ALWAYS use the `query_database` tool to execute a read-only SQL query to fetch the exact data before responding.
Keep your final answers professional, concise, and focused on actionable intelligence.
"""

def query_database(sql_query: str) -> str:
    """Execute a read-only SQL query against the KS Police database to answer user queries."""
    with SessionLocal() as db:
        try:
            upper_query = sql_query.upper()
            if any(forbidden in upper_query for forbidden in ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]):
                return "Error: Only SELECT queries are allowed."
            
            result = db.execute(text(sql_query))
            rows = result.fetchall()
            
            formatted = []
            for row in rows[:50]: # limit to 50 results
                formatted.append(str(dict(row._mapping)))
            
            if not formatted:
                return "No results found."
                
            return "\n".join(formatted)
        except Exception as e:
            return f"Database error: {str(e)}"

def _call_gemini_rest(api_key: str, history: list, new_question: str) -> str:
    """Call Gemini 3.5 Flash via REST API using httpx to avoid heavy grpcio dependencies."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    
    contents = []
    # Add system prompt as a user message first (since system_instruction isn't strictly needed if we prepend)
    contents.append({"role": "user", "parts": [{"text": SYSTEM_PROMPT}]})
    contents.append({"role": "model", "parts": [{"text": "Understood. I will act as the KSP Crime AI Assistant."}]})
    
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        
    contents.append({"role": "user", "parts": [{"text": new_question}]})
    
    tools = [{
        "functionDeclarations": [
            {
                "name": "query_database",
                "description": "Execute a read-only SQL query against the KS Police database to answer user queries.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "sql_query": {
                            "type": "STRING",
                            "description": "The exact SQL query string to run."
                        }
                    },
                    "required": ["sql_query"]
                }
            }
        ]
    }]
    
    payload = {
        "contents": contents,
        "tools": tools,
        "toolConfig": {
            "functionCallingConfig": {
                "mode": "AUTO"
            }
        }
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        
        if "candidates" not in data or not data["candidates"]:
            return "Error: No response from AI."
            
        candidate = data["candidates"][0]
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        
        # Check if model wants to call a tool
        MAX_TURNS = 3
        for turn in range(MAX_TURNS):
            if "candidates" not in data or not data["candidates"]:
                return "Error: No response from AI."
                
            candidate = data["candidates"][0]
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            
            if not parts:
                break
                
            if "functionCall" in parts[0]:
                fc = parts[0]["functionCall"]
                if fc["name"] == "query_database":
                    sql_query = fc.get("args", {}).get("sql_query", "")
                    fc_id = fc.get("id", "")
                    tool_result = query_database(sql_query)
                    
                    function_response_part = {
                        "functionResponse": {
                            "name": "query_database",
                            "response": {"result": tool_result}
                        }
                    }
                    if fc_id:
                        function_response_part["functionResponse"]["id"] = fc_id
                        
                    contents.append(content)
                    contents.append({
                        "role": "user",
                        "parts": [function_response_part]
                    })
                    
                    payload["contents"] = contents
                    response = httpx.post(url, json=payload, timeout=30.0)
                    response.raise_for_status()
                    data = response.json()
                    continue
            
            if "text" in parts[0]:
                return parts[0]["text"]
                
        return "Error: Unexpected response format or too many function calls."
        
    except Exception as e:
        print(f"Gemini REST error: {e}")
        return None

def _fallback_answer(db: Session, question: str, session_id: str) -> ChatQueryResponse:
    # Full text search fallback - mock for now since complaint text was moved/removed in CaseMaster schema
    tsquery = func.plainto_tsquery("english", question)
    
    # We will just search crime group names instead as a fallback
    stmt = (
        select(CaseMaster)
        .options(
            joinedload(CaseMaster.police_station).joinedload(Unit.district),
            joinedload(CaseMaster.case_status),
            joinedload(CaseMaster.crime_major_head)
        )
        .join(CrimeHead, CaseMaster.crime_major_head_id == CrimeHead.crime_head_id)
        .where(func.to_tsvector("english", CrimeHead.crime_group_name).op("@@")(tsquery))
        .limit(5)
    )
    matches = db.execute(stmt).scalars().all()

    if not matches:
        return ChatQueryResponse(
            session_id=session_id,
            answer="I couldn't find any cases matching that question.",
            sources=[],
        )

    summary_lines = [f"Found {len(matches)} case(s) related to your question:"]
    sources = []
    for case in matches:
        crime_type = case.crime_head_name or "Unknown"
        status = case.case_status_name or "Unknown"
        district = case.police_station.district.district_name if case.police_station and case.police_station.district else "Unknown"
        
        summary_lines.append(f"- {case.crime_no} ({crime_type}, {status}, {district})")
        sources.append(
            ChatSource(
                case_id=str(case.case_master_id),
                fir_number=case.crime_no,
                snippet=crime_type,
            )
        )

    return ChatQueryResponse(session_id=session_id, answer="\n".join(summary_lines), sources=sources)

def answer_question(db: Session, question: str, session_id: str) -> ChatQueryResponse:
    if settings.OPENAI_OR_LLM_API_KEY:
        history = chat_store.get_history(session_id)
        answer = _call_gemini_rest(settings.OPENAI_OR_LLM_API_KEY, history, question)
        if answer:
            return ChatQueryResponse(session_id=session_id, answer=answer, sources=[])
            
    return _fallback_answer(db, question, session_id)
