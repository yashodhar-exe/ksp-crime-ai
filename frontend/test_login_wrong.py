import urllib.request
import json
url = "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1/auth/login"
data = json.dumps({"username": "admin.ksp", "password": "wrongpassword"}).encode('utf-8')
headers = {
    "Content-Type": "application/json",
    "Origin": "https://ksp-crime-ai-2026.onslate.in"
}
req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req) as res:
        print("STATUS:", res.status)
        print("HEADERS:", res.headers)
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("HEADERS:", e.headers)
