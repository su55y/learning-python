from pydantic import BaseModel, validator
from pydantic.types import OptionalDate

from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from urllib.parse import urlparse

from .consts import HTTP_STATUS_CODES


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HTTPResponse(BaseModel):
    body: Optional[bytes] = None
    date: OptionalDate
    headers: Dict[str, str] = {}
    status: int

    @validator("headers", pre=True)
    def check_headers(cls, v):
        return v or {}

    @validator("status")
    def check_status(cls, v):
        if v not in HTTP_STATUS_CODES:
            raise ValueError(f"invalid status code {v}")
        return v

    @classmethod
    def with_date(cls, obj):
        obj["date"] = obj.get("date") or datetime.now().date()
        return super().parse_obj(obj)


class HTTPRequest(BaseModel):
    body: Optional[bytes] = None
    headers: Dict[str, str] = {}
    method: HTTPMethod
    path: str

    @validator("headers", pre=True)
    def check_headers(cls, v):
        return v or {}

    @validator("method")
    def check_method(cls, v):
        if not isinstance(v, HTTPMethod):
            raise ValueError(f"invalid method {v}")
        return v

    @validator("path")
    def check_path(cls, v):
        if not v or ((url := urlparse(v)) and not url.path):
            raise ValueError(f"invalid path {v}")
        return v
