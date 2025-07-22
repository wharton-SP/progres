import socket
import sys
from cryptography.hazmat.primitives.asymmetric import x25519

private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()

IP_ADDRESS = "0.0.0.0"
PORT_NUMBER = 5000

BUFFER_SIZE = 4096
KEY_HEADER = "===fanala-hidy miankina==="
SEPARATOR = "===fisarahana==="

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

try:
    server.bind((IP_ADDRESS, PORT_NUMBER))

# If the default port is not available
except OSError:

    # Try using any available port
    try:
        server.bind((IP_ADDRESS, 0))

    except OSError:
        print("[ERR] Unable to start the server")
        sys.exit(1)

# If everything works, listen to the actual address
server.listen()
print(f"[INFO] Server listening on : {server.getsockname()}")

client, addr = server.accept()

# Sends public key to client (in bytes)
public_key_bytes = public_key.public_bytes_raw()
client.send(KEY_HEADER.encode())
client.send(public_key_bytes)
client.send(SEPARATOR.encode())

data = client.recv(BUFFER_SIZE)
print(f"[INFO] Data received : {data}")

client.close()
server.close()
