import os
import sys
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler

def run():
    port = int(os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT", 8000))
    try:
        import uvicorn
        from app.main import app
        # Run uvicorn programmatically
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        err = traceback.format_exc()
        class ErrHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(err.encode('utf-8'))
        print("Starting error server on port", port)
        httpd = HTTPServer(("0.0.0.0", port), ErrHandler)
        httpd.serve_forever()

if __name__ == "__main__":
    run()
