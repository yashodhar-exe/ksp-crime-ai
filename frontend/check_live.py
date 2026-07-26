import urllib.request
import re
html = urllib.request.urlopen('https://ksp-crime-ai-2026.onslate.in').read().decode('utf-8')
m = re.search(r'src="(/assets/index-[^"]+\.js)"', html)
if m:
    js_url = 'https://ksp-crime-ai-2026.onslate.in' + m.group(1)
    print("JS File:", js_url)
    js = urllib.request.urlopen(js_url).read().decode('utf-8')
    if "50044345940" in js:
        print("YES! The Catalyst URL is inside the current JS bundle!")
    else:
        print("NO! The Catalyst URL is NOT in the current JS bundle.")
else:
    print("Could not find JS file in HTML")
