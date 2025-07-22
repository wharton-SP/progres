import os
import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 2222          #! j'ai choisi ce port au pif

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def receive_file(client_socket):
    # Lire le header en bytes
    received = b""
    while SEPARATOR.encode() not in received:
        chunk = client_socket.recv(BUFFER_SIZE)
        if not chunk:
            return False  # Connexion fermée
        received += chunk
    header, rest = received.split(SEPARATOR.encode(), 1)
    filename = header.decode().strip()

    # Lire la taille du fichier
    while SEPARATOR.encode() not in rest:
        chunk = client_socket.recv(BUFFER_SIZE)
        if not chunk:
            return False
        rest += chunk
    filesize_str, filedata = rest.split(SEPARATOR.encode(), 1)
    filesize = int(filesize_str.decode().strip())

    # On le fout dans un putain de dossier
    received_dir = "Received"
    os.makedirs(received_dir, exist_ok=True)
    filepath = os.path.join(received_dir, os.path.basename(filename))

    with open(filepath, 'wb') as f:
        f.write(filedata)
        bytes_read_total = len(filedata)
        while bytes_read_total < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            bytes_read_total += len(bytes_read)
    print(f"[+] Successfully received the file: {filepath}")
    return True

def main():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    while True:
        try:
            if not receive_file(client_socket):
                break
        except Exception as e:
            print(f"Erreur lors de la réception : {e}")
            break

    client_socket.close()
    s.close()

if __name__ == "__main__":
    main()