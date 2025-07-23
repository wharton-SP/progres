import os
import socket
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import secrets

IP_ADDRESS = "0.0.0.0"
PREFERRED_PORT = 5000
BUFFER_SIZE = 4096

KEY_HEADER = b"===fanala-hidy miankina==="
SEPARATOR = b"===fisarahana==="

# Private and public keys for secure communication
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()


def connect_to_server(ip: str, port: int) -> socket.socket | None:
    """Initializes a connection to the server"""

    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        client.connect((ip, port))
        print(f"[INFO] Connected to {ip}:{port}")
        return client

    except OSError as e:
        print(f"[WARN] Could not connect to {ip}:{port}: {e}")
        return None


def receive_peer_key(sock: socket.socket) -> bytes:
    """Receives the encoded peer key, sent from the server"""

    print("[INFO] Waiting for peer's public key...")
    buffer = b""

    while True:
        chunk = sock.recv(BUFFER_SIZE)

        if not chunk:
            print("[ERR] Connection closed by server before receiving key")
            sys.exit(1)
        buffer += chunk

        if SEPARATOR in buffer:
            break

    # Parse received message
    if KEY_HEADER not in buffer:
        print("[ERR] KEY_HEADER not found")
        sys.exit(1)

    try:
        _, key_block = buffer.split(KEY_HEADER, 1)
        peer_key_bytes, _ = key_block.split(SEPARATOR, 1)
        return peer_key_bytes

    except ValueError:
        print("[ERR] Malformed key exchange message")
        sys.exit(1)


def send_own_key(sock: socket.socket, public_key_bytes: bytes):
    """Sends public key to a the server"""

    print("[INFO] Sending our public key...")
    payload = KEY_HEADER + public_key_bytes + SEPARATOR
    sock.sendall(payload)


def derive_shared_key(peer_key_bytes: bytes) -> bytes:
    """Creates an AES key from the received peer key"""

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


def encrypt_file(file_path: str, key: bytes) -> tuple[bytes, bytes, bytes]:
    with open(file_path, "rb") as f:
        data = f.read()

    AESgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    encrypted = AESgcm.encrypt(nonce, data, associated_data=None)

    return encrypted, nonce, os.path.basename(file_path).encode()


def send_file(sock: socket.socket, key: bytes):
    file_path = input("Enter path to file to send: ").strip()

    if not os.path.exists(file_path):
        print("[ERR] File not found.")
        return

    encrypted_data, nonce, filename = encrypt_file(file_path, key)
    metadata = f"{filename.decode()}|{len(encrypted_data)}".encode()

    print("[INFO] Sending metadata...")
    sock.sendall(metadata + SEPARATOR)

    print("[INFO] Sending nonce...")
    sock.sendall(nonce)

    print("[INFO] Sending encrypted file data...")
    sock.sendall(encrypted_data)

    print("[SUCCESS] File sent successfully.")


def main():
    client_socket = connect_to_server(IP_ADDRESS, PREFERRED_PORT)

    if not client_socket:
        print("[INFO] Could not connect on preferred port.")
        sys.exit(1)

    # ECDH (Elliptic Curve Diffie-Hellman) handshake
    peer_key_bytes = receive_peer_key(client_socket)
    send_own_key(client_socket, public_key.public_bytes_raw())

    AES_key = derive_shared_key(peer_key_bytes)

    print(f"[SUCCESS] Shared AES key derived: {AES_key.hex()}")

    send_file(client_socket, AES_key)

    client_socket.close()


if __name__ == "__main__":
    main()
