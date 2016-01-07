import http.server
import socketserver
import os

os.chdir('public_html')

PORT = 8000


Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
print(httpd)

print("serving at port", PORT)
httpd.serve_forever()