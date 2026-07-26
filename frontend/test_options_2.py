import urllib.request
url = "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1/auth/test_options_reachability"
headers = {
    "Origin": "https://ksp-crime-ai-2026.onslate.in",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type"
}
req = urllib.request.Request(url, headers=headers, method="OPTIONS")
try:
    with urllib.request.urlopen(req) as res:
        print("STATUS:", res.status)
        print("HEADERS:", res.headers)
        print("BODY:", res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("HEADERS:", e.headers)
    print("BODY:", e.read().decode('utf-8'))
