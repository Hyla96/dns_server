from src.udp_server.question import Question
from src.udp_server.record_class import RecordClass
from src.udp_server.record_type import RecordType


def test_parser():
    data = b"\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"
    question, offset = Question.from_bytes(bytearray(data))
    reversed_data = question.to_bytes()

    assert offset == 16, f"Expected 16, got {offset}"
    assert (
        question.label.name == "google.com"
    ), f"Expected google.com, got {question.label}"
    assert (
        question.record_type == RecordType.A
    ), f"Expected Record Type A, got {question.record_type}"
    assert (
        question.record_class == RecordClass.IN
    ), f"Expected Record Class IN, got {question.record_class}"

    assert data == reversed_data, f"Expected reversed data {data}, got {reversed_data}"


if __name__ == "__main__":
    test_parser()
