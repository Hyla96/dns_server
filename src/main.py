import sys
import threading

from src.packet.udp_server import udp_server
from src.server.server import start_server


def main():
    udp_thread = threading.Thread(target=udp_server)
    tcp_thread = threading.Thread(target=start_server)

    udp_thread.start()
    tcp_thread.start()

    try:
        udp_thread.join()
        tcp_thread.join()
    except KeyboardInterrupt:
        print("Shutting down servers...")
        sys.exit(0)


if __name__ == "__main__":
    main()
