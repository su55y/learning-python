from typing import Union
import uuid

from attrs import define, field

from utils import parse_uuid


@define
class User:
    name: str = field(order=True)
    id: uuid.UUID = field(factory=uuid.uuid4, converter=parse_uuid)
    rating: int = field(default=0, converter=int)

    @id.validator
    def id_validator(self, _, value: Union[str, uuid.UUID, bytes]):
        if (isinstance(value, bytes) and not len(value) == 16) or (
            isinstance(value, str) and not len(value) == 32
        ):
            raise ValueError("Invalid 'id' value '%s'" % value)
