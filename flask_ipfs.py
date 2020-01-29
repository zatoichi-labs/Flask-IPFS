import ipaddress
from multiaddr import Multiaddr

import ipfshttpclient

from flask import current_app


def construct_multiaddr(
    url: str="http://localhost",
    port: int=5001,
) -> Multiaddr:
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
    return addr


class IPFS:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        addr = construct_multiaddr(
                url=app.config.get('IPFS_GATEWAY_URL', "http://localhost"),
                port=app.config.get('IPFS_GATEWAY_PORT', 5001),
            )
        client = ipfshttpclient.connect(addr)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ipfs'] = client
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return { 'ipfs': current_app.extensions['ipfs'] }

    def __getattr__(self, name):
        return getattr(current_app.extensions['ipfs'], name)
