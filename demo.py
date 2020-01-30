import os

from flask import Flask
from flask_ipfs import IPFS

app = Flask(__name__)
app.config.update(
    # IPFS integration (use to connect to your IPFS gateway node)
    IPFS_GATEWAY_URL=os.environ.get('IPFS_GATEWAY_URL') or "http://127.0.0.1",
    IPFS_GATEWAY_PORT=int(os.environ.get('IPFS_GATEWAY_PORT') or 5001),
    # Interplanentary Fission integration (overrides IPFS integration for Heroku)
    # Add-on: https://elements.heroku.com/addons/interplanetary-fission
    # Just add these config params (only overrides if all variables have value):
    INTERPLANETARY_FISSION_URL=os.environ.get('INTERPLANETARY_FISSION_URL'),
    INTERPLANETARY_FISSION_USERNAME=os.environ.get('INTERPLANETARY_FISSION_USERNAME'),
    INTERPLANETARY_FISSION_PASSWORD=os.environ.get('INTERPLANETARY_FISSION_PASSWORD'),
)
ipfs = IPFS(app)


@app.route('/')
@app.route('/version')
def version():
    return f'IPFS Version: {ipfs.version()["Version"]}'

@app.route('/add')
def add():
    response = ipfs.add("key")
    return f'{response}'

@app.route('/get/<cid>')
def get(cid):
    response = ipfs.get(cid)
    return f'{response}'

@app.route('/add_json')
def add_json():
    response = ipfs.add_json({"key": "value"})
    return f'{response}'

@app.route('/get_json/<cid>')
def get_json(cid):
    response = ipfs.get_json(cid)
    return f'{response}'

@app.route('/ls_pins')
def ls_pins():
    response = ipfs.ls_pins()
    return f'{response}'

@app.route('/add_pin/<cid>')
def add_pin(cid):
    response = ipfs.add_pin(cid)
    return f'{response}'

@app.route('/rm_pin/<cid>')
def rm_pin(cid):
    response = ipfs.rm_pin(cid)
    return f'{response}'
