from abc import ABC
from abc import abstractmethod
from aiohttp import ClientSession


class HeadersGenerator:

    def generate(self) -> dict:
        return {
            'authority': 'www.myhome_appartment_info_parser.ge',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4',
            'cache-control': 'max-age=0',
            'referer': 'https://www.myhome.ge/ru/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }


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
            response = await session.post(self.__browser_url, headers={"Authorization": self.__auth_password},
                                          data={"script": self.__get_script(url)})
            j = await response.json()
        return j["output"]
