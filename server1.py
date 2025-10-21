import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 8000))
clients = {}

print("Servidor de rendezvous rodando na porta 8000...")

while True:
    data, addr = server.recvfrom(1024)
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
        server.sendto(response.encode(), addr)