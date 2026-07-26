import urllib.request
import re
html = urllib.request.urlopen('https://ksp-crime-ai-2026.onslate.in/assets/index-zhmtb4nG.js').read().decode('utf-8')
m = re.search(r'VITE_API_BASE_URL:"([^"]+)"', html)
if m:
    print('VITE_API_BASE_URL is:', m.group(1))
else:
    print('VITE_API_BASE_URL NOT FOUND in the js file')
