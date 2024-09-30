import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 2053))

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received data: {data} from {addr}")


if __name__ == "__main__":
    main()
