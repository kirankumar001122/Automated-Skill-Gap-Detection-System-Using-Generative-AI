#!/usr/bin/env python3
"""
Simple HTTP server for the frontend
This serves the HTML file to avoid CORS issues
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class FrontendHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow requests from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('dashboard.html', 'text/html')
        elif self.path == '/dashboard.html':
            self.serve_file('dashboard.html', 'text/html')
        elif self.path == '/simple.html':
            self.serve_file('simple.html', 'text/html')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def serve_file(self, filename, content_type):
        """Serve a specific file"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), filename)
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

def run_frontend_server():
    """Run the frontend HTTP server"""
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, FrontendHandler)
    
    print("Frontend Server")
    print("=" * 40)
    print("Frontend running on: http://localhost:3000")
    print("Serving simple.html as main page")
    print("Backend API: http://localhost:8000")
    print("=" * 40)
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nFrontend server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    run_frontend_server()
