from http import HTTPMethod, HTTPStatus
from pydantic import ValidationError

import unittest
import json

from models import HTTPRequest, HTTPResponse


class RequestTests(unittest.TestCase):
    def test_dict_request(self):
        get = {"method": HTTPMethod.GET, "path": "/api/items/fetch"}
        request_get = HTTPRequest(**get)
        self.assertEqual(request_get.path, "/api/items/fetch")

        post = {
            "method": HTTPMethod.POST,
            "path": "/new",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"new": "data"}).encode(),
        }
        request_post = HTTPRequest(**post)
        self.assertEqual(request_post.path, "/new")
        self.assertEqual(request_post.headers.get("Content-Type"), "application/json")
        self.assertEqual(request_post.body, b'{"new": "data"}')

    def test_raw_requests(self):
        get = '{"method":"GET","path":"/api/items/fetch"}'
        request_get = HTTPRequest(**json.loads(get))
        self.assertEqual(request_get.method.value, HTTPMethod.GET)
        self.assertEqual(request_get.path, "/api/items/fetch")

        post = '{"method":"POST","path":"/api/items/add","body":"{\\"name\\": \\"item1\\"}"}'
        request_post = HTTPRequest.parse_raw(post)
        self.assertEqual(request_post.method, HTTPMethod.POST)
        self.assertEqual(request_post.path, "/api/items/add")
        self.assertIsInstance(request_post.body, bytes)
        self.assertEqual(request_post.body, b"""{"name": "item1"}""")

    def test_broken_requests(self):
        broken_requests = [
            '{"method":"RUN","path":"/"}',
            r'{"method":"GET","path":"\"}',
        ]

        for r in broken_requests:
            self.assertRaises(ValidationError, HTTPRequest.parse_raw, r)


class ResponseTests(unittest.TestCase):
    def test_dict_response(self):
        request_get = HTTPResponse(**{"status": 204})
        self.assertIsInstance(request_get.status, HTTPStatus)
        self.assertEqual(request_get.status, HTTPStatus.NO_CONTENT)

        HTTPResponse(
            **{
                "headers": {"Content-Type": "application/json"},
                "body": b'{"some": "data"}',
                "status": 200,
            }
        )

    def test_broken_responses(self):
        broken_responses = [
            '{"headers":{"Content-Type":"application/json"}}',
            '{"status":69}',
            '{"status":200,"headers":"Invalid headers format"}',
        ]

        for r in broken_responses:
            self.assertRaises(ValidationError, HTTPResponse.parse_raw, r)
