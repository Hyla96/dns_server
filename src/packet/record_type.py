from enum import Enum


class RecordType(Enum):
    A = 1  # Host Address
    NS = 2  # Authoritative Name Server
    MD = 3  # Mail Destination (Obsolete - Use MX)
    MF = 4  # Mail Forwarder (Obsolete - Use MX)
    CNAME = 5  # Canonical name for an alias
    SOA = 6  # Marks the start of a zone of authority
    MB = 7  # Mailbox domain name (EXPERIMENTAL)
    MG = 8  # Mail group member (EXPERIMENTAL)
    MR = 9  # Mail rename domain name (EXPERIMENTAL)
    NULL = 10  # Null RR (EXPERIMENTAL)
    WKS = 11  # Well known service description
    PTR = 12  # Domain name pointer
    HINFO = 13  # Host information
    MINFO = 14  # Mailbox or mail list information
    MX = 15  # Mail exchange
    TXT = 16  # Text strings

    @staticmethod
    def from_bytes(data: bytes):
        value = int.from_bytes(data, byteorder="big")
        return RecordType.from_int(value)

    @classmethod
    def from_int(cls, value):
        for record in cls:
            if record.value == value:
                return record
        raise ValueError(f"{value} is not a valid Record Type")

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(2, "big")
