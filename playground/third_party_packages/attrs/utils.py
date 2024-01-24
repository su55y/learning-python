from typing import Union
import uuid


def parse_uuid(value: Union[str, bytes, uuid.UUID]) -> uuid.UUID:
    match value:
        case str():
            return uuid.UUID(hex=value)
        case bytes():
            return uuid.UUID(bytes=value)
        case uuid.UUID():
            return value
        case _:
            raise ValueError("Unexpcected 'id' type '%s'" % type(value))
