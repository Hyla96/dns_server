import socket

from src.packet.answer import Answer
from src.packet.header import Header
from src.packet.label_sequence import LabelSequence
from src.packet.query_packet import QueryPacket
from src.packet.reply_packet import ReplyPacket
from src.dns_manager.database import get_record


def create_response_packet(query_packet):
    response_question = query_packet.question

    record = get_record(
        response_question.label.name,
        response_question.record_type,
        response_question.record_class,
    )

    print(f"Record: {record}")

    if record is None:
        return ReplyPacket(
            header=Header(
                packet_identifier=query_packet.header.packet_identifier,
                query_response_indicator=1,
                operation_code=0,
                authoritative_answer=0,
                truncation=0,
                recursion_desired=query_packet.header.recursion_desired,
                recursion_available=0,
                reserved=0,
                response_code=3,
                question_count=1,
                answer_record_count=0,
                authority_record_count=0,
                additional_record_count=0,
            ),
            question=response_question,
            answer=None,
        )

    response_header = Header(
        packet_identifier=query_packet.header.packet_identifier,
        query_response_indicator=1,
        operation_code=0,
        authoritative_answer=1,  # Set to 1 if you're authoritative for the zone
        truncation=0,
        recursion_desired=query_packet.header.recursion_desired,
        recursion_available=1,
        reserved=0,
        response_code=0,
        question_count=1,
        answer_record_count=1,
        authority_record_count=0,
        additional_record_count=0,
    )

    print(f"Record length {len(record.value)}")
    print(f"Record value {record.value}")
    response_answer = Answer(
        label=LabelSequence(name=record.label),
        record_type=record.record_type,
        record_class=record.record_class,
        ttl=record.ttl,
        rd_length=len(record.value),
        rdata=record.value,
    )

    # Create the response packet
    response_packet = ReplyPacket(
        header=response_header, question=response_question, answer=response_answer
    )

    return response_packet


def start_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 2053))

    print("UDP DNS dns_manager listening on localhost:2053")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received UDP data from {addr}")

        query_packet = QueryPacket.from_bytes(bytearray(data))

        print(
            f"UDP Query for: {query_packet.question.label.name}, Type: {query_packet.question.record_type}, Class: {query_packet.question.record_class}"
        )
        print(f"UDP Query data {data}")

        response_packet = create_response_packet(query_packet)

        response_data = response_packet.to_bytes()
        print(f"UDP Response data {response_data}")
        sock.sendto(response_data, addr)
        print(f"Sent UDP response to {addr}")
