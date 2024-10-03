from src.packet.label_sequence import LabelSequence
from src.packet.record_class import RecordClass
from src.packet.record_type import RecordType


class Answer:
    def __init__(
        self,
        label: LabelSequence,
        record_type: RecordType,
        record_class: RecordClass,
        ttl: int,
        rd_length: int,
        rdata: bytes,
    ):
        self.label = label
        self.record_type = record_type
        self.record_class = record_class
        self.ttl = ttl
        self.rd_length = rd_length
        self.rdata = rdata

    @staticmethod
    def from_bytes(data: bytearray):
        index = 0
        label, offset = LabelSequence.from_bytes(data)
        index += offset
        record_type = RecordType.from_bytes(data[index : index + 2])
        index += 2
        record_class = RecordClass.from_bytes(data[index : index + 2])
        index += 2
        ttl = int.from_bytes(data[index : index + 4], byteorder="big")
        index += 4
        rd_length = int.from_bytes(data[index : index + 2], byteorder="big")
        index += 2
        rdata = data[index:]

        return Answer(
            label=label,
            record_type=record_type,
            record_class=record_class,
            ttl=ttl,
            rd_length=rd_length,
            rdata=rdata,
        )

    def to_bytes(self) -> bytes:
        result = b""
        result += self.label.to_bytes()
        result += self.record_type.to_bytes()
        result += self.record_class.to_bytes()
        result += self.ttl.to_bytes(4, byteorder="big")
        result += self.rd_length.to_bytes(2, byteorder="big")
        result += self.rdata
        return result
