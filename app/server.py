import os
import sys
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Route "/" to templates/index.html
        if path == "/" or path == "/index.html":
            return os.path.join(BASE_DIR, "templates", "index.html")
        # Route static files
        if path.startswith("/static/"):
            rel_path = path.replace("/static/", "", 1)
            return os.path.join(BASE_DIR, "static", rel_path)
        return super().translate_path(path)

    def log_message(self, format, *args):
        # Keep console output clean
        pass

def run_server(port=PORT):
    # Allow address reuse immediately on restart
    TCPServer.allow_reuse_address = True
    with TCPServer(("", port), CustomHandler) as httpd:
        print(f"🚀 TechVault Server running at: http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
