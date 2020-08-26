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

    def add_bytes(self, raw_bytes: bytes) -> CID:
        cid = self._get_multihash(raw_bytes)
        self._db[cid] = raw_bytes
        return cid

    def add(self, raw_str: str) -> CID:
        data = raw_str.encode('utf-8')
        cid = self._get_multihash(data)
        self._db[cid] = data
        return cid

    def get_bytes(self, cid: CID) -> bytes:
        return self._db[cid]

    def get(self, cid: CID) -> str:
        return self._db[cid].decode('utf-8')

    def ls_pins(self) -> List[CID]:
        return self._pins

    def add_pin(self, cid: CID):
        assert cid in self._db.keys(), "Cannot test this without adding object first!"
        self._pins.append(cid)

    def rm_pin(self, cid: CID):
        self._pins.remove(cid)
