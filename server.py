from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/products":
            products = [{'id':1, 'name':'amir', 'price': 100},{'id':2, 'name':'ray', 'price': 23}]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(products).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")


server = HTTPServer(("localhost", 8000), MyHandler)
server.serve_forever()