import os

from flask import Flask
from flask_ipfs import IPFS

app = Flask(__name__)
ipfs = IPFS(app)


@app.route('/')
def ipfs_version():
    return f'IPFS Version: {ipfs.version()["Version"]}'
