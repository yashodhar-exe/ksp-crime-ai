import urllib.request
import json
url = "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1/auth/register"
# sending malformed json to trigger 422 or 500
data = b'{"username": "testuser"'
headers = {
    "Content-Type": "application/json",
    "Origin": "https://ksp-crime-ai-2026.onslate.in"
}
req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req) as res:
        print("STATUS:", res.status)
        print("HEADERS:", res.headers)
        print("BODY:", res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("HEADERS:", e.headers)
    print("BODY:", e.read().decode('utf-8'))
