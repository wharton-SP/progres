import os
import socket
import sys
import time
from tqdm import tqdm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import secrets

# L'IP sera déterminée dynamiquement
PREFERRED_PORT = 5000
BUFFER_SIZE = 4096
BROADCAST_PORT = 2222 

KEY_HEADER = b"===fanala-hidy miankina==="
SEPARATOR = b"===fisarahana==="

# Private and public keys for secure communication
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()


# Nouvelle fonction pour découvrir les serveurs sur le réseau
def discover_servers(timeout=3) -> list:
    """Recherche des serveurs sur le réseau via un broadcast UDP."""
    servers = []
    print(f"[*] Recherche de serveurs pendant {timeout} secondes...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.settimeout(timeout)
        try:
            s.sendto(b"DISCOVER", ("255.255.255.255", BROADCAST_PORT))
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    data, addr = s.recvfrom(1024)
                    if data.decode() == "SERVER_ACK" and addr[0] not in servers:
                        servers.append(addr[0])
                        print(f"    -> Serveur trouvé à l'adresse : {addr[0]}")
                except socket.timeout:
                    # Le timeout est normal, on continue juste d'attendre
                    pass
        except OSError as e:
            print(f"[WARN] Erreur lors de la diffusion réseau : {e}")
            print("       Assurez-vous d'être connecté à un réseau.")

    return servers


def connect_to_server(ip: str, port: int) -> socket.socket | None:
    """Initializes a connection to the server"""

    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        client.connect((ip, port))
        print(f"[INFO] Connecté à {ip}:{port}")
        return client

    except OSError as e:
        print(f"[WARN] Impossible de se connecter à {ip}:{port}: {e}")
        return None


def receive_peer_key(sock: socket.socket) -> bytes:
    """Receives the encoded peer key, sent from the server"""

    print("[INFO] En attente de la clé publique du pair...")
    buffer = b""

    while True:
        chunk = sock.recv(BUFFER_SIZE)

        if not chunk:
            print("[ERR] Connexion fermée par le serveur avant la réception de la clé")
            sys.exit(1)
        buffer += chunk

        if SEPARATOR in buffer:
            break

    # Parse received message
    if KEY_HEADER not in buffer:
        print("[ERR] KEY_HEADER non trouvé")
        sys.exit(1)

    try:
        _, key_block = buffer.split(KEY_HEADER, 1)
        peer_key_bytes, _ = key_block.split(SEPARATOR, 1)
        return peer_key_bytes

    except ValueError:
        print("[ERR] Message d'échange de clés malformé")
        sys.exit(1)


def send_own_key(sock: socket.socket, public_key_bytes: bytes):
    """Sends public key to a the server"""

    print("[INFO] Envoi de notre clé publique...")
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
    file_path = input("Entrez le chemin du fichier à envoyer : ").strip()

    if not os.path.exists(file_path):
        print("[ERR] Fichier non trouvé.")
        return

    encrypted_data, nonce, filename = encrypt_file(file_path, key)
    metadata = f"{filename.decode()}|{len(encrypted_data)}".encode()

    print("[INFO] Envoi des métadonnées...")
    sock.sendall(metadata + SEPARATOR)

    print("[INFO] Envoi du nonce...")
    sock.sendall(nonce)

    print("[INFO] Envoi des données chiffrées du fichier...")

    total_size = len(encrypted_data)
    sent = 0
    with tqdm(total=total_size, unit="o", unit_scale=True, desc="Envoi") as pbar:
        for i in range(0, total_size, BUFFER_SIZE):
            chunk = encrypted_data[i:i+BUFFER_SIZE]
            sock.sendall(chunk)
            sent += len(chunk)
            pbar.update(len(chunk))

    print("[SUCCESS] Fichier envoyé avec succès.")


def main():
    # --- MODIFICATION START ---
    # Étape 1: Découvrir les serveurs
    available_servers = discover_servers()

    if not available_servers:
        print("\n[INFO] Aucun serveur trouvé. Assurez-vous que le script receiver.py est en cours d'exécution sur le réseau.")
        sys.exit(0)

    # Étape 2: Laisser l'utilisateur choisir un serveur
    print("\n--- Serveurs Disponibles ---")
    for i, server_ip in enumerate(available_servers, 1):
        print(f"{i}. {server_ip}")
    
    chosen_ip = ""
    while not chosen_ip:
        try:
            choice = int(input(f"\nChoisissez un serveur (1-{len(available_servers)}): "))
            if 1 <= choice <= len(available_servers):
                chosen_ip = available_servers[choice - 1]
            else:
                print("Choix invalide.")
        except (ValueError, IndexError):
            print("Veuillez entrer un numéro valide.")

    # Étape 3: Se connecter au serveur choisi
    client_socket = connect_to_server(chosen_ip, PREFERRED_PORT)
    # --- MODIFICATION END ---


    if not client_socket:
        print("[INFO] La connexion a échoué.")
        sys.exit(1)

    # La suite du code reste identique : échange de clés et envoi du fichier
    # ECDH (Elliptic Curve Diffie-Hellman) handshake
    peer_key_bytes = receive_peer_key(client_socket)
    send_own_key(client_socket, public_key.public_bytes_raw())

    AES_key = derive_shared_key(peer_key_bytes)

    print(f"[SUCCESS] Clé AES partagée dérivée : {AES_key.hex()}")

    send_file(client_socket, AES_key)

    client_socket.close()


if __name__ == "__main__":
    main()