from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import List
from entity import Message


class IFacebookMessageProvider(ABC):
    @abstractmethod
    def get(self) -> List[Message]:
        ...


class FacebookMessageProvider(IFacebookMessageProvider):
    def __init__(self, cookies, limit: int,group_id: str | int):
        self.__cookies = cookies
        self.__limit = limit
        self.__group_id =group_id
    def get(self) -> List[Message]:
        pass
