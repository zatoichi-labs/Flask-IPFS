from flask_ipfs import IpfsHttpClient, TestClient

import pytest

@pytest.fixture
def http_client():
    http = IpfsHttpClient()
    # Start on a fresh slate
    for pin in http.ls_pins():
        http.rm_pin(pin)
    yield http


@pytest.fixture
def test_client():
    yield TestClient()
