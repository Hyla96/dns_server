from src.udp_server.query_packet import QueryPacket
from src.udp_server.record_class import RecordClass
from src.udp_server.record_type import RecordType


def test_parser():
    header_data = b"\x07\x65\x78\x61\x6d\x70\x6c\x65\x03\x63\x6f\x6d"
    question_data = b"\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"

    data = header_data + question_data

    packet = QueryPacket.from_bytes(bytearray(data))

    assert (
        packet.header.packet_identifier == 0x0765
    ), f"Expected 0x0765, got {packet.header.packet_identifier}"
    assert (
        packet.question.label.name == "google.com"
    ), f"Expected google.com, got {packet.question.label}"
    assert (
        packet.question.record_type == RecordType.A
    ), f"Expected Record Type A, got {packet.question.record_type}"
    assert (
        packet.question.record_class == RecordClass.IN
    ), f"Expected Record Class IN, got {packet.question.record_class}"


if __name__ == "__main__":
    test_parser()
    print("Everything passed")
