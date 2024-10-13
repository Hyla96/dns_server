from src.udp_server.header import Header
from src.udp_server.question import Question


class QueryPacket:
    def __init__(
        self,
        header: Header,
        question: Question,
    ):
        self.header = header
        self.question = question

    @staticmethod
    def from_bytes(data: bytearray):
        header = Header.from_bytes(data[:12])
        question, _ = Question.from_bytes(data[12:])

        return QueryPacket(header=header, question=question)

    def to_bytes(self) -> bytes:
        return self.header.to_bytes() + self.question.to_bytes()
