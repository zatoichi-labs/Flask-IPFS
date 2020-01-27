import ipfshttpclient

from flask import current_app


class IPFS:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        cnx_multiaddr = ipfshttpclient.DEFAULT_ADDR
        # TODO Use app.config.IPFS_GATEWAY_URL and app.config.IPFS_GATEWAY_PORT
        #      https://github.com/ipfs/go-ipfs/blob/master/docs/config.md#addresses
        client = ipfshttpclient.connect(cnx_multiaddr)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ipfs'] = client
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return { 'ipfs': current_app.extensions['ipfs'] }

    def __getattr__(self, name):
        return getattr(current_app.extensions['ipfs'], name)
