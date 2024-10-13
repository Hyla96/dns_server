from typing import Optional

from src.packet.answer import Answer
from src.packet.header import Header
from src.packet.question import Question


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
        return (
            self.header.to_bytes()
            + self.question.to_bytes()
            + (self.answer.to_bytes() if self.answer else b"")
        )
