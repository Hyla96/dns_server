from src.packet.label_sequence import LabelSequence
from src.packet.record_class import RecordClass
from src.packet.record_type import RecordType


class Question:
    def __init__(
        self,
        label: LabelSequence,
        record_type: RecordType,
        record_class: RecordClass,
    ):
        self.label = label
        self.record_type = record_type
        self.record_class = record_class

    @staticmethod
    def from_bytes(data: bytearray):
        index = 0
        label, offset = LabelSequence.from_bytes(data)
        index += offset
        record_type = RecordType.from_bytes(data[index : index + 2])
        index += 2
        record_class = RecordClass.from_bytes(data[index : index + 2])
        index += 2

        return Question(
            label=label,
            record_type=record_type,
            record_class=record_class,
        ), index

    def to_bytes(self) -> bytes:
        label = self.label.to_bytes()
        record_type = self.record_type.to_bytes()
        record_class = self.record_class.to_bytes()
        return label + record_type + record_class
