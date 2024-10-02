from src.header import Header


def test_parser():
    data = b"\x07\x65\x78\x61\x6d\x70\x6c\x65\x03\x63\x6f\x6d"
    header = Header.from_bytes(data)

    print(header.packet_query_response_indicator)

    assert (
        header.packet_identifier == 0x0765
    ), f"Expected 0x0765, got {header.packet_identifier}"

    assert (
        header.packet_query_response_indicator == 0
    ), f"Expected 0, got {header.packet_query_response_indicator}"
    assert header.operation_code == 15, f"Expected 15, got {header.operation_code}"
    assert (
        header.authoritative_answer == 0
    ), f"Expected 0, got {header.authoritative_answer}"
    assert header.truncation == 0, f"Expected 0, got {header.truncation}"
    assert header.recursion_desired == 0, f"Expected 0, got {header.recursion_desired}"

    assert (
        header.recursion_available == 0
    ), f"Expected 0, got {header.recursion_available}"
    assert header.reserved == 6, f"Expected 6, got {header.reserved}"
    assert header.response_code == 1, f"Expected 1, got {header.response_code}"

    assert (
        header.question_count == 0x6D70
    ), f"Expected 0x6d70, got {header.question_count}"
    assert (
        header.answer_record_count == 0x6C65
    ), f"Expected 0x6c65, got {header.answer_record_count}"
    assert (
        header.authority_record_count == 0x0363
    ), f"Expected 0x0363, got {header.authority_record_count}"
    assert (
        header.additional_record_count == 0x6F6D
    ), f"Expected 0x6f6d, got {header.additional_record_count}"


if __name__ == "__main__":
    test_parser()
    print("Everything passed")
