from abc import (
    ABC,
    abstractmethod,
)
import json
from typing import (
    Dict,
    List,
    Union,
)
from cid import (
    CIDv0,
    CIDv1,
)

CID = Union[str, CIDv0, CIDv1]


class BaseAPI(ABC):
    @abstractmethod
    def add_bytes(self, raw_bytes: bytes) -> CID:
        pass

    @abstractmethod
    def add(self, raw_str: str) -> CID:
        pass

    @abstractmethod
    def get_bytes(self, cid: CID) -> bytes:
        pass

    @abstractmethod
    def get(self, cid: CID) -> str:
        pass

    def add_json(self, obj: Dict) -> CID:
        return self.add(json.dumps(obj, sort_keys=True, separators=(",", ":")))

    def get_json(self, cid: CID) -> Dict:
        return json.loads(self.get(cid))

    @abstractmethod
    def ls_pins(self) -> List[CID]:
        pass

    @abstractmethod
    def add_pin(self, cid: CID):
        pass

    @abstractmethod
    def rm_pin(self, cid: CID):
        pass

    def update_pin(self, old_cid: CID, new_cid: CID):
        self.add_pin(new_cid)
        self.rm_pin(old_cid)
