import os

from flask import Flask
from flask_ipfs import IPFS

app = Flask(__name__)
app.config.update(
    # IPFS integration (use to connect to your IPFS gateway node)
    IPFS_GATEWAY_URL=os.environ.get('IPFS_GATEWAY_URL') or "http://127.0.0.1",
    IPFS_GATEWAY_PORT=int(os.environ.get('IPFS_GATEWAY_PORT') or 5001),
)
ipfs = IPFS(app)


@app.route('/')
def ipfs_version():
    return f'IPFS Version: {ipfs.version()["Version"]}'
