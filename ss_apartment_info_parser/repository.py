import random
from abc import ABC
from abc import abstractmethod
from typing import List


class IProxyRepository(ABC):
    @abstractmethod
    def get(self) -> str:
        ...


class ProxyRepository(IProxyRepository):
    def __init__(self, proxies: List[str]):
        self.__proxies = proxies

    def get(self) -> str:
        return self.__proxies[random.Random().randint(0, len(self.__proxies) - 1)]
