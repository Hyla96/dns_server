import socket
import sys

from src.packet.header import Header
from src.packet.query_packet import QueryPacket
from src.packet.answer import Answer
from src.packet.reply_packet import ReplyPacket


def create_response_packet(query_packet):
    response_header = Header(
        packet_identifier=query_packet.header.packet_identifier,
        query_response_indicator=1,
        operation_code=0,
        authoritative_answer=1,  # Set to 1 if you're authoritative for the zone
        truncation=0,
        recursion_desired=query_packet.header.recursion_desired,
        recursion_available=0,
        reserved=0,
        response_code=0,
        question_count=1,
        answer_record_count=1,
        authority_record_count=0,
        additional_record_count=0,
    )

    response_question = query_packet.question
    rdata = b"\x01\x02\x03\x04"  # Example IPv4 address 1.2.3.4
    print(f"Length data {sys.getsizeof(rdata)}")
    response_answer = Answer(
        label=response_question.label,
        record_type=response_question.record_type,
        record_class=response_question.record_class,
        ttl=3600,  # Time-to-live in seconds (e.g., 1 hour)
        rd_length=len(rdata),
        rdata=rdata,
    )

    # Create the response packet
    response_packet = ReplyPacket(
        header=response_header, question=response_question, answer=response_answer
    )

    return response_packet


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 2053))

    print("DNS server listening on localhost:2053")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received data from {addr}")

        query_packet = QueryPacket.from_bytes(bytearray(data))
        print(
            f"Query for: {query_packet.question.label.name}, Type: {query_packet.question.record_type}, Class: {query_packet.question.record_class}"
        )

        response_packet = create_response_packet(query_packet)

        response_data = response_packet.to_bytes()
        print(f"Response data {response_data}")
        sock.sendto(response_data, addr)
        print(f"Sent response to {addr}")


if __name__ == "__main__":
    main()
