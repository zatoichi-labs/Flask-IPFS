from hashlib import sha256
import json

from cid import (
    CIDv0,
    CIDv1,
)

from multihash import (
    encode as mh_encode,
    to_b58_string,
)

from typing import (
    Dict,
    List,
    Union,
)

CID = Union[str, CIDv0, CIDv1]

from .base import BaseAPI

class TestClient(BaseAPI):
    def __init__(self, init_db: Dict[str, bytes]=None):
        self._db = {}
        if init_db:
            self._db.update(init_db)

        self._pins = list(self._db.keys())

    def _get_multihash(self, data: bytes) -> CID:
        hasher = sha256()
        hasher.update(data)
        h = hasher.digest()
        return to_b58_string(mh_encode(h, 'sha2-256'))

    def add(self, raw_str: str) -> CID:
        data = raw_str.encode('utf-8')
        cid = self._get_multihash(data)
        self._db[cid] = data
        return cid

    def get(self, cid: CID) -> str:
        return self._db[cid].decode('utf-8')

    def add_json(self, obj: Dict) -> CID:
        encoded_obj = json.dumps(obj)
        return self.add(encoded_obj)  # returns CID

    def get_json(self, cid: CID) -> Dict:
        return json.loads(self.get(cid))

    def ls_pins(self) -> List[CID]:
        return self._pins

    def add_pin(self, cid: CID):
        assert cid in self._db.keys(), "Cannot test this without adding object first!"
        self._pins.append(cid)

    def rm_pin(self, cid: CID):
        self._pins.remove(cid)

    def update_pin(self, old_cid: CID, new_cid: CID):
        self.rm_pin(old_cid)
        self.add_pin(new_cid)
