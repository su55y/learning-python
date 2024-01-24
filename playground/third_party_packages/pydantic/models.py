from http import HTTPStatus, HTTPMethod
import re
from typing import Dict, Optional, Union

from pydantic import BaseModel, validator


class HTTPRequest(BaseModel):
    body: Optional[bytes] = None
    headers: Dict[str, str] = {}
    method: HTTPMethod
    path: str

    @validator("path")
    def check_path(cls, v):
        if not re.match(r"^/[\w/\-.]*$", v):
            raise ValueError(f"invalid path '{v}'")
        return v


class HTTPResponse(BaseModel):
    body: Optional[bytes] = None
    headers: Dict[str, str] = {}
    status: HTTPStatus

    @validator("status")
    def check_status(cls, status: Union[int, HTTPStatus]):
        if isinstance(status, int):
            return HTTPStatus(status)
        return status
