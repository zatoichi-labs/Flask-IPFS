import ipaddress
import json
from multiaddr import Multiaddr
import requests

import ipfshttpclient

from flask import current_app


class InterplanetaryFission:
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


class IpfsHttpClient:
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

    def add(self, raw_str):
        return self._client.add_str(raw_str)

    def get(self, cid):
        return self._client.object.get(cid)["Data"]

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


class IPFS:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.config.get('INTERPLANETARY_FISSION_URL', None):
            client = InterplanetaryFission(
                    url=app.config.get('INTERPLANETARY_FISSION_URL'),
                    username=app.config.get('INTERPLANETARY_FISSION_USERNAME'),
                    password=app.config.get('INTERPLANETARY_FISSION_PASSWORD'),
                )
        else:
            client = IpfsHttpClient(
                    url=app.config.get('IPFS_GATEWAY_URL', "http://localhost"),
                    port=app.config.get('IPFS_GATEWAY_PORT', 5001),
                )

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ipfs'] = client
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return { 'ipfs': current_app.extensions['ipfs'] }

    def __getattr__(self, name):
        return getattr(current_app.extensions['ipfs'], name)
