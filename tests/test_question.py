from src.packet.question import Question
from src.packet.record_class import RecordClass
from src.packet.record_type import RecordType


def test_parser():
    data = b"\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x01\x00\x01\x00"
    question = Question.from_bytes(bytearray(data))

    assert question.name == "google.com", f"Expected google.com, got {question.name}"
    assert (
        question.record_type == RecordType.A
    ), f"Expected Record Type A, got {question.record_type}"
    assert (
        question.record_class == RecordClass.IN
    ), f"Expected Record Class IN, got {question.record_class}"


if __name__ == "__main__":
    test_parser()
