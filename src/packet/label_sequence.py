class LabelSequence:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def from_bytes(data: bytearray, start: int = 0):
        index = start
        labels = []
        while True:
            length = data[index]
            if length == 0:
                index += 1
                break
            if length & 0xC0 == 0xC0:
                # This is a compression pointer
                pointer = (
                    int.from_bytes(data[index : index + 2], byteorder="big") & 0x3FFF
                )
                if start == 0:  # Only follow the pointer if we're at the start
                    rest, _ = LabelSequence.from_bytes(data, pointer)
                    labels.extend(rest.name.split("."))
                index += 2
                break
            index += 1
            labels.append(data[index : index + length].decode("ascii"))
            index += length

        name = ".".join(labels)
        return LabelSequence(name=name), index - start

    def to_bytes(self, compression: bool = False, offset: int = 0) -> bytes:
        if not compression:
            return self._to_bytes_uncompressed()

        result = bytearray()
        labels = self.name.split(".")
        for label in labels:
            if offset > 0:
                # Use compression pointer
                pointer = 0xC000 | offset
                result.extend(pointer.to_bytes(2, byteorder="big"))
                break
            result.append(len(label))
            result.extend(label.encode("ascii"))
            offset += len(label) + 1
        if offset == 0:
            result.append(0)  # Terminating zero length octet
        return bytes(result)

    def _to_bytes_uncompressed(self) -> bytes:
        name_bytes = b""
        for name in self.name.split("."):
            name_bytes += len(name).to_bytes(1, "big")
            name_bytes += bytes(name, "ascii")
        name_bytes += b"\x00"
        return name_bytes


# Helper function to find compression offsets
def find_name_offsets(packet: bytes) -> dict:
    offsets = {}
    index = 12  # Start after the header
    while index < len(packet):
        if packet[index] == 0:
            index += 1
            continue
        if packet[index] & 0xC0 == 0xC0:
            index += 2
            continue
        name, length = LabelSequence.from_bytes(packet, index)
        offsets[name.name] = index
        index += length
    return offsets
