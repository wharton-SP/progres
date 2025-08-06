import os
import socket
import sys
import threading
from tqdm import tqdm  # <-- Ajout de l'import
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

IP_ADDRESS = "0.0.0.0"
PREFERRED_PORT = 5000
BUFFER_SIZE = 4096
BROADCAST_PORT = 2222

KEY_HEADER = b"===fanala-hidy miankina==="
SEPARATOR = b"===fisarahana==="

# Private and public keys for secure communication
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()


def handle_discovery():
    """Cette fonction écoute les messages de découverte sur le réseau."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(("", BROADCAST_PORT))
        print(f"[*] Le service de découverte est actif sur le port {BROADCAST_PORT}")
        while True:
            data, addr = s.recvfrom(1024)
            if data.decode() == "DISCOVER":
                print(f"[*] Requête de découverte reçue de {addr}")
                s.sendto(b"SERVER_ACK", addr)

def bind_server_socket() -> socket.socket:
    """Creates a server that will bind and listen to the default port and address"""

    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        server.bind((IP_ADDRESS, PREFERRED_PORT))
        print(f"[INFO] Serveur lié au port {PREFERRED_PORT}")

    # If the default port is not available
    except OSError as e:
        print(f"[WARN] Port {PREFERRED_PORT} indisponible: {e}")

        # Try using any available port
        try:
            server.bind((IP_ADDRESS, 0))
            print(f"[INFO] Serveur lié à un port aléatoire {server.getsockname()[1]}")

        except OSError as another_e:
            print(f"[ERR] Impossible de se lier à un port: {another_e}")
            sys.exit(1)

    # If everything works, listen to the actual address
    server.listen()
    return server


def send_public_key(sock: socket.socket):
    """Sends public key to a connected client"""

    payload = KEY_HEADER + public_key.public_bytes_raw() + SEPARATOR
    sock.sendall(payload)
    print("[INFO] Clé publique envoyée au client")


def receive_peer_key(sock: socket.socket) -> tuple[bytes, bytes]:
    """Receives the encoded peer key, sent from the client"""

    buffer = b""

    while True:
        chunk = sock.recv(BUFFER_SIZE)

        if not chunk:
            print("[ERR] Connexion fermée avant la réception de la clé")
            sys.exit(1)

        buffer += chunk

        if SEPARATOR in buffer:
            break

    # Should be just raw key wrapped
    if KEY_HEADER in buffer:
        print("[WARN] En-tête inattendu dans la réponse du pair")
        # Strip it if present
        buffer = buffer.split(KEY_HEADER)[-1]

    try:
        peer_key_bytes, rest = buffer.split(SEPARATOR, 1)
        return peer_key_bytes, rest

    except ValueError:
        print("[ERR] Clé du pair malformée")
        sys.exit(1)


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

def receive_file(sock, aes_key: bytes, initial_buffer: bytes):

    # First, receive the metadata
    buffer = initial_buffer

    while SEPARATOR not in buffer:
        chunk = sock.recv(BUFFER_SIZE)

        if not chunk:
            print("[ERR] Connexion fermée avant la réception des métadonnées.")
            return

        buffer += chunk

    metadata, leftover = buffer.split(SEPARATOR, 1)

    try:
        filename_str, file_size_str = metadata.decode().split("|")
        file_size = int(file_size_str)

    except Exception as e:
        print(f"[ERR] Format des métadonnées invalide: {e}")
        return

    print(f"[INFO] Réception du fichier : {filename_str} ({file_size} octets)")

    # Now receive the nonce (12 bytes for AES-GCM)
    nonce = sock.recv(12)

    if len(nonce) < 12:
        print("[ERR] Échec de la réception du nonce complet.")
        return

    ciphertext = leftover

    received = len(ciphertext)
    with tqdm(total=file_size, unit="o", unit_scale=True, desc="Réception") as pbar:
        pbar.update(received)
        while received < file_size:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                break
            ciphertext += chunk
            received += len(chunk)
            pbar.update(len(chunk))

    try:
        aesgcm = AESGCM(aes_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        # Save to folder
        folder = "received_files"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename_str)

        with open(file_path, "wb") as f:
            f.write(plaintext)

        print(f"[SUCCESS] Fichier sauvegardé ici : {file_path}")

    except Exception as e:
        print(f"[ERR] Le déchiffrement a échoué : {e}")


def main():
    # --- MODIFICATION START ---
    # Lancer le service de découverte dans un thread séparé (en arrière-plan)
    discovery_thread = threading.Thread(target=handle_discovery, daemon=True)
    discovery_thread.start()
    # --- MODIFICATION END ---

    server = bind_server_socket()
    print(f"[INFO] En écoute sur {server.getsockname()}...")

    # Le serveur attendra maintenant une connexion TCP tout en répondant aux pings de découverte
    client_socket, addr = server.accept()
    print(f"[INFO] Connexion de {addr}")

    send_public_key(client_socket)
    peer_key_bytes, leftover = receive_peer_key(client_socket)

    AES_key = derive_shared_key(peer_key_bytes)

    print("[SUCCESS] Clé AES partagée dérivée !")
    print(f"Clé AES (hex): {AES_key.hex()}")

    print("[INFO] Clé AES dérivée. Prêt à recevoir un fichier chiffré...")
    receive_file(client_socket, AES_key, leftover)

    client_socket.close()
    server.close()


if __name__ == "__main__":
    main()