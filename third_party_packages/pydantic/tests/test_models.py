from pydantic import ValidationError

from datetime import datetime
import unittest
import json

from models.http_models import HTTPMethod, HTTPRequest, HTTPResponse


class RequestTests(unittest.TestCase):
    def test_dict_request(self):
        get = {"method": HTTPMethod.GET, "path": "/api/items/fetch"}
        post = {
            "method": HTTPMethod.POST,
            "path": "/new",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"new": "data"}),
        }

        request_get = HTTPRequest(**get)
        self.assertEqual(
            request_get.path,
            "/api/items/fetch",
            f"unexpected path ({request_get})",
        )

        request_post = HTTPRequest(**post)
        self.assertEqual(
            request_post.path,
            "/new",
            f"unexpected path ({request_post})",
        )
        self.assertEqual(
            request_post.headers.get("Content-Type"),
            "application/json",
            f"unexpected headers: {request_post.headers}",
        )
        self.assertEqual(
            request_post.body,
            b'{"new": "data"}',
            f"unexpected body ({request_post.body})",
        )

    def test_json_requests(self):
        get, post = (
            """{
                "method": "GET",
                "path": "/api/items/fetch"
            }""",
            """{
                "method": "POST",
                "path": "/api/items/add",
                "body": "{\\"name\\": \\"item1\\"}"
            }""",
        )

        request_get = HTTPRequest(**json.loads(get))
        self.assertEqual(
            request_get.method.value,
            HTTPMethod.GET,
            f"method != GET ({request_get})",
        )
        self.assertEqual(
            request_get.path,
            "/api/items/fetch",
            f"unexpected path ({request_get})",
        )

        request_post = HTTPRequest.parse_raw(post)
        self.assertEqual(
            request_post.method,
            HTTPMethod.POST,
            f"method != POST ({request_post})",
        )
        self.assertEqual(
            request_post.path,
            "/api/items/add",
            f"unexpected path ({request_post})",
        )
        self.assertIsInstance(
            request_post.body,
            bytes,
            f"unexpected body type: {type(request_post.body).__name__}",
        )
        self.assertEqual(
            request_post.body,
            b"""{"name": "item1"}""",
            f"unexpected body content: {request_post.body}",
        )

    def test_broken_requests(self):
        requests = [
            """{
                "method": "RUN",
                "path": "/"
            }""",
            """{
                "method": "GET",
                "path": ""
            }""",
        ]

        for r in requests:
            with self.assertRaises(ValidationError):
                HTTPRequest.parse_raw(r)


class ResponseTests(unittest.TestCase):
    def test_response_with_date(self):
        response_obj = HTTPResponse.with_date({"status": 204})
        self.assertEqual(
            response_obj.date,
            datetime.now().date(),
            f"unexpected date {response_obj}",
        )

    def test_broken_responses(self):
        responses = [
            """{
                "status": 69
            }""",
            """{
                "status": 200,
                "headers": "Invalid headers format"
            }""",
        ]

        for r in responses:
            with self.assertRaises(ValidationError):
                HTTPResponse.parse_raw(r)


if __name__ == "__main__":
    unittest.main()
