import ipaddress
from multiaddr import Multiaddr

import ipfshttpclient

from .base import BaseAPI

class IpfsHttpClient(BaseAPI):
    def __init__(self, url: str="http://localhost", port: int=5001):
        http_protocol, host = url.split('://')

        if http_protocol not in ('http', 'https'):
            raise ValueError(f"Invalid protocol: {http_protocol}")
        if not isinstance(host, str):
            ValueError(f"Invalid url: {url}")

        try:
            # method returns either IPv4Address or IPv6Address (or raises ValueError)
            addr = ipaddress.ip_address(host)
            ip_protocol = 'ip4' if isinstance(addr, ipaddress.IPv4Address) else 'ip6'
        except ValueError:
            ip_protocol = 'dns'

        addr = Multiaddr(f"/{ip_protocol}/{host}/tcp/{port}/{http_protocol}")
        self._client = ipfshttpclient.connect(addr)

    def add_bytes(self, raw_bytes):
        return self._client.add(raw_bytes)

    def add(self, raw_str):
        return self._client.add_str(raw_str)

    def get_bytes(self, cid):
        return self._client.cat(cid)

    def get(self, cid):
        return self.get_bytes(cid).decode('utf-8')

    def add_json(self, obj):
        return self._client.add_json(obj)  # returns CID

    def get_json(self, cid):
        return self._client.get_json(cid)

    def ls_pins(self):
        response = self._client.pin.ls()
        return list(response['Keys'].keys())

    def add_pin(self, cid):
        self._client.pin.add(cid)

    def rm_pin(self, cid):
        self._client.pin.rm(cid)

    def update_pin(self, old_cid, new_cid):
        self._client.pin.update(old_cid, new_cid)
