"""
Test that our mock TestClient matches the behavior of the real IpfsHttpClient
"""

def test_add(http_client, test_client):
    data = "Something"
    http_cid = http_client.add(data)
    test_cid = test_client.add(data)
    assert http_client.get(http_cid) == test_client.get(test_cid)
    #assert http_cid == test_cid  # TODO Does not produce the same hash

def test_add(http_client, test_client):
    data = b"Something"
    http_cid = http_client.add_bytes(data)
    test_cid = test_client.add_bytes(data)
    assert http_client.get_bytes(http_cid) == test_client.get_bytes(test_cid)
    #assert http_cid == test_cid  # TODO Does not produce the same hash


def test_add_json(http_client, test_client):
    data = {"key": "Something"}
    http_cid = http_client.add_json(data)
    test_cid = test_client.add_json(data)
    assert http_client.get_json(http_cid) == test_client.get_json(test_cid)
    #assert http_cid == test_cid  # TODO Does not produce the same hash


def test_add_pin(http_client, test_client):
    # Ensure the data is in there
    data = "Something"
    http_cid = http_client.add(data)
    test_cid = test_client.add(data)
    # Add the pin
    http_client.add_pin(http_cid)
    assert http_cid in http_client.ls_pins()
    test_client.add_pin(test_cid)
    assert test_cid in test_client.ls_pins()
    http_client.rm_pin(http_cid)
    # Then remove it
    assert http_cid not in http_client.ls_pins()
    test_client.rm_pin(test_cid)
    assert test_cid not in test_client.ls_pins()
