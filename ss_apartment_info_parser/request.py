from abc import ABC
from abc import abstractmethod
from aiohttp import ClientSession


class IRequest(ABC):
    @abstractmethod
    async def send(self, url: str) -> str:
        ...


class Request(IRequest):

    def __init__(self, browser_url: str, auth_password: str):
        self.__browser_url = browser_url
        self.__auth_password = auth_password

    @staticmethod
    def __get_script(url: str) -> str:
        return open("script.js", "r").read() % url

    async def send(self, url: str) -> str:
        async with ClientSession() as session:
            response = await session.post(f"{self.__browser_url}/task", headers={"Authorization": self.__auth_password},
                                          data={"script": self.__get_script(url)})
            j = await response.json()
        return j["output"]
