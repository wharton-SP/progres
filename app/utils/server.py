import socket
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

IP_ADDRESS = "0.0.0.0"
PREFERRED_PORT = 5000
BUFFER_SIZE = 4096

KEY_HEADER = b"===fanala-hidy miankina==="
SEPARATOR = b"===fisarahana==="

# Private and public keys for secure communication
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()

def bind_server_socket() -> socket.socket:
    ''' Creates a server that will bind and listen to the default port and address '''

    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        server.bind((IP_ADDRESS, PREFERRED_PORT))
        print(f"[INFO] Server bound to preferred port {PREFERRED_PORT}")

    # If the default port is not available
    except OSError as e:
        print(f"[WARN] Preferred port {PREFERRED_PORT} unavailable: {e}")

        # Try using any available port
        try:
            server.bind((IP_ADDRESS, 0))
            print(f"[INFO] Server bound to random port {server.getsockname()[1]}")

        except OSError as another_e:
            print(f"[ERR] Unable to bind to any port: {another_e}")
            sys.exit(1)

    # If everything works, listen to the actual address
    server.listen()
    return server


def send_public_key(sock: socket.socket):
    ''' Sends public key to a connected client '''

    payload = KEY_HEADER + public_key.public_bytes_raw() + SEPARATOR
    sock.sendall(payload)
    print("[INFO] Sent public key to client")


def receive_peer_key(sock: socket.socket) -> bytes:
    ''' Receives the encoded peer key, sent from the client '''

    buffer = b""

    while True:
        chunk = sock.recv(BUFFER_SIZE)

        if not chunk:
            print("[ERR] Connection closed before key received")
            sys.exit(1)

        buffer += chunk

        if SEPARATOR in buffer:
            break

    # Should be just raw key wrapped
    if KEY_HEADER in buffer:
        print("[WARN] Unexpected header in peer response")
        # Strip it if present
        buffer = buffer.split(KEY_HEADER)[-1]

    try:
        peer_key_bytes, _ = buffer.split(SEPARATOR, 1)
        return peer_key_bytes

    except ValueError:
        print("[ERR] Malformed peer key")
        sys.exit(1)


def derive_shared_key(peer_key_bytes: bytes) -> bytes:
    ''' Creates an AES key from the received peer key '''

    peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_key_bytes)
    shared_secret = private_key.exchange(peer_public_key)

    AES_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"===fifandraisan-tanana===",
        backend=default_backend(),
    ).derive(shared_secret)

    return AES_key


def main():
    server = bind_server_socket()
    print(f"[INFO] Listening on {server.getsockname()}...")

    client_socket, addr = server.accept()
    print(f"[INFO] Connection from {addr}")

    send_public_key(client_socket)
    peer_key_bytes = receive_peer_key(client_socket)

    AES_key = derive_shared_key(peer_key_bytes)

    print("[SUCCESS] Shared AES key derived!")
    print(f"AES key (hex): {AES_key.hex()}")

    client_socket.close()
    server.close()


if __name__ == "__main__":
    main()
