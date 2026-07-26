import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test")
def test():
    return {"ok": True}

client = TestClient(app)
res = client.options("/test", headers={"Origin": "https://ksp-crime-ai-2026.onslate.in", "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type"})
print("OPTIONS Headers:", res.headers)
res2 = client.post("/test", headers={"Origin": "https://ksp-crime-ai-2026.onslate.in"})
print("POST Headers:", res2.headers)
