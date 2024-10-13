import socket

from src.udp_server.header import Header
from src.udp_server.label_sequence import LabelSequence
from src.udp_server.query_packet import QueryPacket
from src.udp_server.question import Question
from src.udp_server.record_class import RecordClass
from src.udp_server.record_type import RecordType
from src.udp_server.reply_packet import ReplyPacket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 2053

address = (host, port)


def test_server():
    header = Header(
        packet_identifier=1234,  # A random 16-bit identifier
        query_response_indicator=0,  # 0 for query, 1 for response
        operation_code=0,  # 0 for standard query
        authoritative_answer=0,  # 0 for non-authoritative
        truncation=0,  # 0 for not truncated
        recursion_desired=1,  # 1 to request recursive query
        recursion_available=0,  # 0 since this is a query
        reserved=0,  # Always 0
        response_code=0,  # 0 for no error
        question_count=1,  # Typically 1 for a single query
        answer_record_count=0,  # 0 for a query
        authority_record_count=0,  # 0 for a query
        additional_record_count=0,  # 0 for a query
    )

    question = Question(
        label=LabelSequence("test.test.com"),
        record_type=RecordType.A,
        record_class=RecordClass.IN,
    )

    query = QueryPacket(
        header=header,
        question=question,
    )

    sock.sendto(query.to_bytes(), address)
    data, addr = sock.recvfrom(1024)

    print(f"Received data from {addr}")

    reply_packet = ReplyPacket.from_bytes(bytearray(data))

    print(f"IP Received is {reply_packet.answer.rdata}")


if __name__ == "__main__":
    test_server()
    print("Everything passed")
