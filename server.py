import os
import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 2222          #! j'ai choisi ce port au pif

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def main():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    # Lecture du header de façon sûre 
    received = ""
    while SEPARATOR not in received:
        received += client_socket.recv(BUFFER_SIZE).decode()
    header, rest = received.split(SEPARATOR, 1)
    filename = header.strip()

    if "<SEPARATOR>" in rest:
        filesize_str, filedata = rest.split(SEPARATOR, 1)
    else:
        filesize_str = ""
        for c in rest:
            if c.isdigit():
                filesize_str += c
            else:
                break
        filedata = rest[len(filesize_str):]
    filesize = int(filesize_str.strip())

    # On le fout dans un putain de dossier
    received_dir = "Received"
    os.makedirs(received_dir, exist_ok=True)
    filepath = os.path.join(received_dir, os.path.basename(filename))

    with open(filepath, 'wb') as f:
        f.write(filedata.encode())
        bytes_read_total = len(filedata)
        while bytes_read_total < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            bytes_read_total += len(bytes_read)
    
    print(f"[+] Successfully received the file: {filepath}")
    client_socket.close()
    s.close()

if __name__ == "__main__":
    main()