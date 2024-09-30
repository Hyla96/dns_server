import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "localhost"
port = 2053

address = (host, port)


def test_server():
    sock.sendto(b"HELLO", address)


if __name__ == "__main__":
    test_server()
    print("Everything passed")
