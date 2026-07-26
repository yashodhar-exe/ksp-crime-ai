import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test")
def test():
    return {"ok": True}

client = TestClient(app)
res = client.options("/test", headers={"Origin": "https://foo.com", "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type"})
print("OPTIONS Headers:", res.headers)
res2 = client.post("/test", headers={"Origin": "https://foo.com"})
print("POST Headers:", res2.headers)
