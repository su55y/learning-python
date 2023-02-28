from datetime import datetime
from pydantic import BaseModel, validator
from pydantic.types import OptionalDate

from enum import Enum, auto
from http import HTTPStatus
from typing import Dict, Optional
from urllib.parse import urlparse

from .consts import HTTP_STATUS_CODES


class HTTPMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


class HTTPResponse(BaseModel):
    status: HTTPStatus
    body: Optional[bytes] = None
    headers: Optional[Dict[str, str]] = None
    date: OptionalDate

    @validator("status")
    def check_status(cls, v):
        if v not in HTTP_STATUS_CODES:
            raise ValueError(f"invalid status code {v}")
        return v

    @validator("headers")
    def check_headers(cls, d):
        if not d:
            return d

        if not isinstance(d, dict):
            raise ValueError(f"invalid headers type {type(d).__name__}")

        for k, v in d.items():
            if not isinstance(k, str):
                raise ValueError(f"invalid header key type {type(k).__name__}")
            if not isinstance(v, str):
                raise ValueError(f"invalid header value type {type(v).__name__}")

    @classmethod
    def with_date(cls, obj):
        obj["date"] = obj.get("date") or datetime.now()
        return super().parse_obj(obj)


class HTTPRequest(BaseModel):
    method: HTTPMethod
    path: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[bytes] = None

    @validator("path")
    def check_path(cls, v):
        if not v or ((url := urlparse(v)) and not url.path):
            raise ValueError(f"invalid path {v}")
        return v

    @validator("headers")
    def check_headers(cls, d):
        if not d:
            return d

        if not isinstance(d, dict):
            raise ValueError(f"invalid headers type {type(d).__name__}")

        for k, v in d.items():
            if not isinstance(k, str):
                raise ValueError(f"invalid header key type {type(k).__name__}")
            if not isinstance(v, str):
                raise ValueError(f"invalid header value type {type(v).__name__}")
