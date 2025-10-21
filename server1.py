import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# === Servidor UDP de Rendezvous ===
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('0.0.0.0', 8000))
clients = {}

print("Servidor de rendezvous rodando na porta 8000...")

def udp_loop():
    while True:
        try:
            data, addr = udp_server.recvfrom(1024)
            msg = data.decode().strip()
            if msg.startswith("REGISTER:"):
                _, player_id, local_port, proxy_port = msg.split(":")
                clients[player_id] = (addr[0], int(proxy_port), int(local_port))
                print(f"✅ {player_id} registrado: {addr[0]}:{proxy_port}")
            elif msg.startswith("GET:"):
                _, target = msg.split(":")
                if target in clients:
                    ip, proxy_port, local_port = clients[target]
                    response = f"CONNECT:{ip}:{proxy_port}:{local_port}"
                else:
                    response = "WAIT"
                udp_server.sendto(response.encode(), addr)
        except Exception as e:
            print("Erro UDP:", e)

# === Servidor HTTP simples para saúde ===
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Rendezvous Server Online - UDP Port 8000')
        else:
            self.send_response(404)
            self.end_headers()

def http_server():
    httpd = HTTPServer(('0.0.0.0', 8001), HealthHandler)
    print("Servidor HTTP de saúde rodando na porta 8001...")
    httpd.serve_forever()

# Inicia os dois servidores em threads
threading.Thread(target=udp_loop, daemon=True).start()
threading.Thread(target=http_server, daemon=True).start()

# Mantém o processo vivo
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nServidores encerrados.")
