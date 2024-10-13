from typing import Optional

from src.udp_server.answer import Answer
from src.udp_server.header import Header
from src.udp_server.question import Question


class ReplyPacket:
    def __init__(
        self,
        header: Header,
        question: Question,
        answer: Optional[Answer],
    ):
        self.header = header
        self.question = question
        self.answer = answer

    @staticmethod
    def from_bytes(data: bytearray):
        header = Header.from_bytes(data[:12])
        question, offset = Question.from_bytes(data[12:])
        answer = Answer.from_bytes(data[offset:])

        return ReplyPacket(
            header=header,
            question=question,
            answer=answer,
        )

    def to_bytes(self) -> bytes:
        header_bytes = self.header.to_bytes()
        question_bytes = self.question.to_bytes()
        answer_bytes = self.answer.to_bytes() if self.answer else b""

        print(f"Header bytes: {header_bytes.hex()}")
        print(f"Question bytes: {question_bytes.hex()}")
        print(f"Answer bytes: {answer_bytes.hex()}")

        return header_bytes + question_bytes + answer_bytes
