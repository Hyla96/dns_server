from src.packet.record_class import RecordClass
from src.packet.record_type import RecordType


class Question:
    def __init__(
        self,
        name: str,
        record_type: RecordType,
        record_class: RecordClass,
    ):
        self.name = name
        self.record_type = record_type
        self.record_class = record_class

    @staticmethod
    def from_bytes(data: bytearray):
        index = 0
        labels = []
        while data[index] != 0x00:
            length = int(data[index])
            index += 1
            labels.append(data[index : index + length].decode("ascii"))
            index += length

        name = ".".join(labels)

        record_type = RecordType.from_bytes(data[index : index + 2])
        index += 2
        record_class = RecordClass.from_bytes(data[index : index + 2])

        return Question(
            name=name,
            record_type=record_type,
            record_class=record_class,
        )

    def to_bytes(self) -> bytes:
        name = bytes(self.name, "ascii")
        record_type = self.record_type.to_bytes()
        record_class = self.record_class.to_bytes()
        return name + record_type + record_class
