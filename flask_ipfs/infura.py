import requests
import json

from .base import BaseAPI

class Infura(BaseAPI):
    def __init__(self, url: str, project_id: str=None, project_secret: str=None):
        self._url = lambda endpoint: url + endpoint
        self._auth = (project_id, project_secret)

    def add(self, raw_str):
        response = requests.post(self._url('/add?pin=true'), files={"fake": (None, raw_str)})
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.json()['Hash']  # returns CID

    def get(self, cid):
        response = requests.get(self._url(f'/get?arg={cid}'))
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.text

    def add_json(self, obj):
        return self.add(json.dumps(obj))

    def get_json(self, cid):
        return json.loads(self.get(cid))

    def ls_pins(self):
        print(self._url(f'/pin/ls'))
        response = requests.get(self._url(f'/pin/ls'))
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.json()

    def add_pin(self, cid):
        response = requests.get(self._url(f'/pin/add?arg={cid}'))
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")

    def rm_pin(self, cid):
        # Cannot remove pins
        pass

    def update_pin(self, old_cid, new_cid):
        self.add_pin(new_cid)
        # Cannot remove pins
