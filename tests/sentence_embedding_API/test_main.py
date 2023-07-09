import logging
from typing import Any, List
from unittest import mock

from fastapi.testclient import TestClient
from fastapi import Request
import pytest
from pytest_mock import MockerFixture
import requests
import requests_mock
import starlette

from src.sentence_embedding_API import main

JSON = main.JSON
test_client = TestClient(main.app)

# Set all needed global variables in sentence_embedding_API
main.FASTAPI_PORT = 8228
main.logger = logging.getLogger()
main.RETURN_ARRAY_SIZE = 500
main.ARRAY_LOWER_BOUND = 0
main.ARRAY_UPPER_BOUND = 10

@pytest.fixture
def fake_request() -> Request:
    return Request(scope = {"type": "http"})

def test_kubernetes_health_check() -> None:
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json().get("status") is not None
    assert response.json()["status"] == "healthy"

@pytest.mark.parametrize("data", ["", 1, None, [], ()])
async def test_get_valid_json_returns_None_if_json_is_invalid(
    data: Any, fake_request: Request
) -> None:
    fake_request._body = str(data)
    json = await main.get_valid_json(fake_request)
    assert json is None

def test_log_connection_url_logs_the_url_correctly(
    mocker: MockerFixture, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    mocker.patch("socket.gethostbyname", return_value = "host IP")

    main.log_connection_url()

    assert caplog.records[0].message == f"Connection URL: http://host IP:{main.FASTAPI_PORT}"

class TestGetRandomArray:

    @pytest.mark.parametrize(
            ["array_size", "lower_bound", "upper_bound"],
            [
                (500, 0, 10),
                (0, 0, 1),
            ],
        )

    def test_generare_random_array_returns_list(
            self,
            array_size: int,
            lower_bound: int,
            upper_bound: int,
        ) -> None:
        embeddings = main.generate_random_array(array_size, lower_bound, upper_bound)

        assert isinstance(embeddings, list)

    @pytest.mark.parametrize(
            ["array_size", "lower_bound", "upper_bound"],
            [
                (500, 0, 10),
                (10, 10, 30),
            ],
        )

    def test_generare_random_array_contains_floats(
            self,
            array_size: int,
            lower_bound: int,
            upper_bound: int,
        ) -> None:
        embeddings = main.generate_random_array(array_size, lower_bound, upper_bound)

        for embedding in embeddings:
            assert isinstance(embedding, float)

    @pytest.mark.parametrize(
            ["array_size", "lower_bound", "upper_bound"],
            [
                (500, 0, 10),
                (0, 0, 1),
            ],
        )

    def test_generare_random_array_returns_correct_size(
            self,
            array_size: int,
            lower_bound: int,
            upper_bound: int,
        ) -> None:
        embeddings = main.generate_random_array(array_size, lower_bound, upper_bound)

        assert len(embeddings) == array_size

    @pytest.mark.parametrize(
            ["array_size", "lower_bound", "upper_bound"],
            [
                (500, 0, 10),
                (10, -1, 1)
            ],
        )

    def test_generate_random_array__returns_between_low_and_high_bounds(
            self,
            array_size: int,
            lower_bound: int,
            upper_bound: int,
        ) -> None:
        embeddings = main.generate_random_array(array_size, lower_bound, upper_bound)

        for embedding in embeddings:
            assert lower_bound <= embedding <= upper_bound

class TestGetEmbeddings:
    request_path = "/get_embeddings"

    def test_get_embeddings_fails_with_invalid_json(self) -> None:
        response = test_client.post(self.request_path, json = "invalid_json")

        assert response.status_code == 400
        assert response.text == "Please use JSON content type\n"

    def test_get_embeddings_returns_embeddings_as_expected(self) -> None:

        response = test_client.post(self.request_path, json = {"sentence": "Tamil is the oldest language"},)

        assert response.status_code == 200
        assert response.json().get("embeddings") is not None

    def test_get_embeddings_fails_when_input_sentence_is_not_provided(self) -> None:

        response = test_client.post(self.request_path, json = {},)

        assert response.status_code == 400
        assert response.text == "Please provide an input sentence to embed\n"

    def test_get_embeddings_fails_when_input_sentence_is_not_string(self) -> None:

        response = test_client.post(self.request_path, json = {"sentence": 8},)

        assert response.status_code == 400
        assert response.text == "Please use String data type for 'sentence' parameter\n"

    def test_get_embeddings_gracefully_fails_when_some_exception_occurs(self) -> None:

        main.RETURN_ARRAY_SIZE = "test"

        response = test_client.post(self.request_path, json = {"sentence": "Peace"},)

        assert response.status_code == 500
        assert response.text == "Please retry again\n"
