import http.server
import socketserver

# https://docs.python.org/3/library/http.server.html

PORT = 1044

Handler = http.server.SimpleHTTPRequestHandler

# provides a directory listing for the local directory
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

