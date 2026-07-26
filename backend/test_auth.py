import urllib.request
import urllib.parse
import json

url = "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1/auth/login"
data = json.dumps({"username": "admin.ksp", "password": "ksp@2026"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print("STATUS:", response.status)
        print("BODY:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("BODY:", e.read().decode('utf-8'))
