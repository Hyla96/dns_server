class Header:
    def __init__(
        self,
        packet_identifier: int,
        packet_query_response_indicator: int,
        operation_code: int,
        authoritative_answer: int,
        truncation: int,
        recursion_desired: int,
        recursion_available: int,
        reserved: int,
        response_code: int,
        question_count: int,
        answer_record_count: int,
        authority_record_count: int,
        additional_record_count: int,
    ):
        self.packet_identifier = packet_identifier
        self.packet_query_response_indicator = packet_query_response_indicator
        self.operation_code = operation_code
        self.authoritative_answer = authoritative_answer
        self.truncation = truncation
        self.recursion_desired = recursion_desired
        self.recursion_available = recursion_available
        self.reserved = reserved
        self.response_code = response_code
        self.question_count = question_count
        self.answer_record_count = answer_record_count
        self.authority_record_count = authority_record_count
        self.additional_record_count = additional_record_count

    @staticmethod
    def from_bytes(data: bytes):
        packet_identifier = int.from_bytes(data[0:2], byteorder="big")

        byte3 = int.from_bytes(data[2:3], byteorder="big")
        packet_qr_indicator = byte3 >> 7
        operation_code = (byte3 & 0x78) >> 3
        authoritative_answer = (byte3 & 0x04) >> 2
        truncation = (byte3 & 0x02) >> 1
        recursion_desired = byte3 & 0x01

        byte4 = int.from_bytes(data[3:4], byteorder="big")
        recursion_available = byte4 >> 7
        reserved = (byte4 & 0x70) >> 4
        response_code = byte4 & 0x0F

        question_count = int.from_bytes(data[4:6], byteorder="big")
        answer_record_count = int.from_bytes(data[6:8], byteorder="big")
        authority_record_count = int.from_bytes(data[8:10], byteorder="big")
        additional_record_count = int.from_bytes(data[10:12], byteorder="big")

        return Header(
            packet_identifier=packet_identifier,
            packet_query_response_indicator=packet_qr_indicator,
            operation_code=operation_code,
            authoritative_answer=authoritative_answer,
            truncation=truncation,
            recursion_desired=recursion_desired,
            recursion_available=recursion_available,
            reserved=reserved,
            response_code=response_code,
            question_count=question_count,
            answer_record_count=answer_record_count,
            authority_record_count=authority_record_count,
            additional_record_count=additional_record_count,
        )
