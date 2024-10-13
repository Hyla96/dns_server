import sys
import threading

from src.dns_manager.http_server import start_http_server
from src.packet.udp_server import start_udp_server


def main():
    udp_thread = threading.Thread(target=start_udp_server)
    http_server = threading.Thread(target=start_http_server)

    udp_thread.start()
    http_server.start()

    try:
        udp_thread.join()
        http_server.join()
    except KeyboardInterrupt:
        print("Shutting down servers...")
        sys.exit(0)


if __name__ == "__main__":
    main()
