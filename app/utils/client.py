import socket
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()
shared_key = None
AES_key = None

IP_ADDRESS = "0.0.0.0"
PORT_NUMBER = 5000

BUFFER_SIZE = 4096
KEY_HEADER = "===fanala-hidy miankina==="
SEPARATOR = "===fisarahana==="

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

try:
    client.connect((IP_ADDRESS, PORT_NUMBER))
    print(f"[INFO] Socket info : {client.getsockname()}")

# If there is nothing (I guess ?) on the default port
except OSError:

    # Try using any available port
    try:
        client.connect((IP_ADDRESS, 0))
        print(f"[INFO] Socket info : {client.getsockname()}")
    except OSError:
        print("[ERR] Unable to connect to the server")
        sys.exit(1)

transfert_done = False
received_bytes = b""

peer_public_key_bytes = None
peer_public_key = None

while not transfert_done:
    data = client.recv(BUFFER_SIZE)

    if data[-16:] == SEPARATOR.encode():
        transfert_done = True
        break

    else:
        received_bytes += data


key_header, rest = received_bytes.split(KEY_HEADER.encode(), 1)
peer_public_key_bytes, rest = rest.split(SEPARATOR.encode(), 1)
peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)

shared_key = private_key.exchange(peer_public_key)
AES_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"===fifandraisan-tanana===",
    backend=default_backend(),
).derive(shared_key)

public_key_bytes = public_key.public_bytes_raw()
client.send(public_key_bytes)


client.close()
