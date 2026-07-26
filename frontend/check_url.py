import urllib.request
import re
html = urllib.request.urlopen('https://ksp-crime-ai-2026.onslate.in/assets/index-zhmtb4nG.js').read().decode('utf-8')
url = "https://ksp-crime-ai-backend-50044345940.development.catalystappsail.in/api/v1"
if url in html:
    print("YES! The catalyst URL is in the bundle.")
    # let's print 50 chars before and after to see how it's used
    idx = html.find(url)
    print(html[max(0, idx-50):idx+len(url)+50])
else:
    print("NO! The catalyst URL is NOT in the bundle.")
