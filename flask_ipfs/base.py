from abc import (
    ABC,
    abstractmethod,
)
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
    def add(self, raw_str: str) -> CID:
        pass

    @abstractmethod
    def get(self, cid: CID) -> str:
        pass

    @abstractmethod
    def add_json(self, obj: Dict) -> CID:
        return self.add(json.dumps(obj))

    @abstractmethod
    def get_json(self, cid: CID) -> Dict:
        pass

    @abstractmethod
    def ls_pins(self) -> List[CID]:
        pass

    @abstractmethod
    def add_pin(self, cid: CID):
        pass

    @abstractmethod
    def rm_pin(self, cid: CID):
        pass

    @abstractmethod
    def update_pin(self, old_cid: CID, new_cid: CID):
        pass
