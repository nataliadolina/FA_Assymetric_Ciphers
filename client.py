import configparser
import pickle
import socket

from utils import DiffieHellman, encrypt

HOST = '127.0.0.1'
PORT = 8080
private_key = 0


def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))

    config = configparser.ConfigParser()
    config.read('config.ini')
    p = int(config["Settings"]["p"])
    g = int(config["Settings"]["g"])
    a = int(config["Settings"]["a"])

    diffie_hellman = DiffieHellman(a=a, p=p, g=g)
    client_mixed_key = diffie_hellman.mixed_key
    private_key = diffie_hellman.generate_key(client_mixed_key)
    print(client_mixed_key)
    print(private_key)

    sock.send(pickle.dumps((p, g, client_mixed_key)))
    sock.close()

    sock = socket.socket()
    sock.connect((HOST, PORT))

    msg = input("Enter msg: ")
    result = encrypt(msg, private_key)
    print(result)
    sock.send(pickle.dumps(result))

    result = encrypt(result, private_key)
    print(result)

    sock.close()


if __name__ == "__main__":
    main()
