import pytest

from tests import AssertRequest, AssertResponse, assert_request

ROUTE = "/fruit"

GET_INPUT = {
    "ok": AssertRequest({}, {"name": "apple"}),
    "bad_request": AssertRequest({}, {"name": "banana"}),
    "internal_server_error": AssertRequest({}, {"name": "error"}),
}

GET_OUTPUT = {
    "ok": AssertResponse({"name": "apple", "count": 1}, 200),
    "bad_request": AssertResponse("Bad Request", 400),
    "internal_server_error": AssertResponse("Internal Server Error", 500),
}


@pytest.mark.parametrize("test_type", GET_INPUT.keys())
def test_get(test_type):
    assert_request("GET", ROUTE, GET_INPUT[test_type], GET_OUTPUT[test_type])


HEADERS = {"Content-Type": "Application/json"}

POST_INPUT = {
    "success": AssertRequest(HEADERS, {"name": "banana"}),
    "fail": AssertRequest(HEADERS, {"name": "apple"}),
}

POST_OUTPUT = {
    "success": AssertResponse("OK", 200),
    "fail": AssertResponse("Bad Request", 400),
}


@pytest.mark.parametrize("test_type", POST_INPUT.keys())
def test_post(test_type):
    assert_request("POST", ROUTE, POST_INPUT[test_type], POST_OUTPUT[test_type])
