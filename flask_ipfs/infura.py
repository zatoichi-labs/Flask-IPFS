import requests
import json

from .base import BaseAPI

class Infura(BaseAPI):
    def __init__(self, url: str, project_id: str=None, project_secret: str=None):
        self._url = url
        self._auth = (project_id, project_secret)
        self.pins = []  # Keep track of the pins we know about (temporary until Infura adds this)

    def url(self, endpoint='/'):
        return self._url + endpoint

    def add_bytes(self, raw_bytes):
        response = requests.post(self.url('/add?pin=true'), files={"fake": raw_bytes.encode("utf-8")})
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.json()['Hash']  # returns CID

    def add(self, raw_str):
        response = requests.post(self.url('/add?pin=true'), files={"fake": (None, raw_str)})
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.json()['Hash']  # returns CID

    def get_bytes(self, cid):
        response = requests.get(self.url(f'/cat?arg={cid}'))
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.content

    def get(self, cid):
        response = requests.get(self.url(f'/cat?arg={cid}'))
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        return response.text

    def ls_pins(self):
        return self.pins

    def add_pin(self, cid):
        response = requests.get(self.url(f'/pin/add?arg={cid}'))
        if response.status_code != 200:
            raise ValueError(f"Error processing request: {response.text}")
        self.pins.append(cid)

    def rm_pin(self, cid):
        # Cannot remove pins from IPFS
        self.pins.remove(cid)
