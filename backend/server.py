from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(b"Giternance backend is running\n")

def main():
	server = HTTPServer(("0.0.0.0", 3000), Handler)
	print("Server listening on port 3000")
	server.serve_forever()

if __name__ == "__main__":
	main()
