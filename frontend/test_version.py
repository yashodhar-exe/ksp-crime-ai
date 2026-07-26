import urllib.request
import json
url = "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1/version"
try:
    with urllib.request.urlopen(url) as res:
        print("STATUS:", res.status)
        print("BODY:", res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("BODY:", e.read().decode('utf-8'))
