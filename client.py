import socket
import os
import sys

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 2222

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <fichier1> [<fichier2> ...]")
        sys.exit(1)

    s = socket.socket()
    print(f"[+] Connexion à {SERVER_HOST}:{SERVER_PORT}")
    s.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connecté.")

    for filename in sys.argv[1:]:
        if not os.path.isfile(filename):
            print(f"Erreur : fichier '{filename}' introuvable.")
            continue
        filesize = os.path.getsize(filename)
        # envoyer le header
        s.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}".encode())
        # envoyer le fichier
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
        print(f"[+] Fichier '{filename}' envoyé.")

    s.close()

if __name__ == "__main__":
    main()
