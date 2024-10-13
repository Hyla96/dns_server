from enum import Enum


class RecordClass(Enum):
    IN = 1  # Internet
    CS = 2  # CSNET
    CH = 3  # CHAOS class
    HS = 4  # Hesiod (Dryer 87)

    @staticmethod
    def from_str(value: str):
        return RecordClass[value.upper()]

    @staticmethod
    def from_bytes(data: bytes):
        value = int.from_bytes(data, byteorder="big")
        return RecordClass.from_int(value)

    @classmethod
    def from_int(cls, value):
        for color in cls:
            if color.value == value:
                return color
        raise ValueError(f"{value} is not a valid Record Type")

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(2, "big")
