class LabelSequence:
    def __init__(
        self,
        name: str,
    ):
        self.name = name

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
        index += 1

        return LabelSequence(
            name=name,
        ), index

    def to_bytes(self) -> bytes:
        name_bytes = b""

        for name in self.name.split("."):
            name_bytes += len(name).to_bytes(1, "big")
            name_bytes += bytes(name, "ascii")

        name_bytes += b"\x00"

        return name_bytes
