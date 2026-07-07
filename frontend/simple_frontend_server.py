#!/usr/bin/env python3
"""
Simple HTTP server for the frontend
This serves the HTML file to avoid CORS issues
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class FrontendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow requests from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests and serve simple.html for root path"""
        if self.path == '/':
            self.path = '/simple.html'
        return super().do_GET()

def run_frontend_server():
    """Run the frontend HTTP server"""
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, FrontendHandler)
    
    print("\n" + "=" * 60)
    print("  🤖 AUTONOMOUS CODING AGENT - FRONTEND SERVER v2.0")
    print("=" * 60)
    print("  🌐 Dashboard: http://localhost:3000")
    print("  📡 Backend API: http://localhost:8000")
    print("  📚 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print("  Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Frontend server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    run_frontend_server()
