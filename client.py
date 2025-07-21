import socket
import os

SERVER_HOST = '0.0.0.0'  #* IP du serveur
SERVER_PORT = 2222       #* port du serveur

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def main():
    filename = "testfile.txt"  #! le fichier à envoyer
    filesize = os.path.getsize(filename)

    s = socket.socket()
    print(f"[+] Connexion à {SERVER_HOST}:{SERVER_PORT}")
    s.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connecté.")

    # envoyer le header
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # envoyer le fichier
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

    print("[+] Fichier envoyé.")
    s.close()

if __name__ == "__main__":
    main()
