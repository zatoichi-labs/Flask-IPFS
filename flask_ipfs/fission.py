import requests
import json

from .base import BaseAPI

class InterplanetaryFission(BaseAPI):
    def __init__(self, url: str, username: str, password: str):
        self._url = lambda endpoint: url + endpoint
        self._auth = (username, password)

    def add(self, raw_str):
        response = requests.post(self._url(f'/ipfs'), data=raw_str, auth=self._auth)
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.text  # returns CID

    def get(self, cid):
        response = requests.get(self._url(f'/ipfs/{cid}'), auth=self._auth)
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.text

    def add_json(self, obj):
        return self.add(json.dumps(obj))

    def get_json(self, cid):
        return json.loads(self.get(cid))

    def ls_pins(self):
        response = requests.get(self._url(f'/ipfs/cids'), auth=self._auth)
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.json()

    def add_pin(self, cid):
        response = requests.put(self._url(f'/ipfs/{cid}'), auth=self._auth)
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")

    def rm_pin(self, cid):
        response = requests.delete(self._url(f'/ipfs/{cid}'), auth=self._auth)
        if response.status_code != 202:
            raise ValueError(f"Error processing request: {response.text}")

    def update_pin(self, old_cid, new_cid):
        self.rm_pin(old_cid)
        self.add_pin(new_cid)
