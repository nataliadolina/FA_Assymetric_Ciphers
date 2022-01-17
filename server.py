import pickle
import socket

from utils import DiffieHellman, encrypt

HOST = '127.0.0.1'
PORT = 8080
private_key = 0


def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()

        msg = conn.recv(4096)
        # Получаем данные от клиента
        data = pickle.loads(msg)

        print(type(data))
        if type(data) == tuple:
            p, g, A = data

            diffie_hellman = DiffieHellman(a=A, p=p, g=g)
            server_mixed_key = diffie_hellman.mixed_key
            private_key = diffie_hellman.generate_key(server_mixed_key)
            print(f"Server mixed key - {server_mixed_key}")
            print(f"Server private key  - {private_key}")

        try:
            result = encrypt(data, private_key)
            print(result)

        except Exception as e:
            print(f"Возникло исключение {e}")


if __name__ == "__main__":
    main()
