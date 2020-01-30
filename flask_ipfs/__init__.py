from flask import current_app

from .fission import InterplanetaryFission
from .http import IpfsHttpClient

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
