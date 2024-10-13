from src.udp_server.answer import Answer
from src.udp_server.record_class import RecordClass
from src.udp_server.record_type import RecordType


def test_answer_parser():
    # Sample data for an A record answer
    data = (
        b"\x06google\x03com\x00\x00\x01\x00\x01\x00\x00\x0e\x10\x00\x04\xd8\x3a\xd3\x8e"
    )

    answer = Answer.from_bytes(bytearray(data))
    reversed_data = answer.to_bytes()

    assert (
        answer.label.name == "google.com"
    ), f"Expected google.com, got {answer.label.name}"
    assert (
        answer.record_type == RecordType.A
    ), f"Expected Record Type A, got {answer.record_type}"
    assert (
        answer.record_class == RecordClass.IN
    ), f"Expected Record Class IN, got {answer.record_class}"
    assert answer.ttl == 3600, f"Expected TTL 3600, got {answer.ttl}"
    assert answer.rd_length == 4, f"Expected RD Length 4, got {answer.rd_length}"
    assert (
        answer.rdata == b"\xd8\x3a\xd3\x8e"
    ), f"Expected RDATA d83ad38e, got {answer.rdata.hex()}"

    assert (
        data == reversed_data
    ), f"Expected reversed data {data.hex()}, got {reversed_data.hex()}"


if __name__ == "__main__":
    test_answer_parser()
