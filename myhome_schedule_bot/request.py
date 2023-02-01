import json
from abc import ABC
from abc import abstractmethod

from aiohttp import ClientSession


class IRequest(ABC):
    @abstractmethod
    async def send(self, url: str, proxy: str) -> str:
        ...


class Request(IRequest):

    def __init__(self, browser_url: str, auth_password: str):
        self.__browser_url = browser_url
        self.__auth_password = auth_password

    @staticmethod
    def __get_script(url: str) -> str:
        return """(async () => {
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        };

        await agent.goto('%s');

        await agent.waitForState({
            name: 'dlfLoaded',
            all(assert) {
                assert(agent.isPaintingStable);
            },
        });

        const cookieButton = await agent.querySelector('#CookieAgreement > button');

        if (cookieButton) {
            await cookieButton.$click()

        }
        resolve(await agent.document.documentElement.innerHTML);
})();""" % url

    async def send(self, url: str, proxy: str) -> str:
        payload = json.dumps({
            "options": {
                "upstreamProxyUrl": proxy,
                "upstreamProxyIpMask": {
                    "ipLookupService": "api.ipify.org",
                    "proxyIp": "185.127.165.192",
                    "publicIp": "146.190.124.200"
                },
                "timezoneId": "Asia/Tbilisi",
                "viewport": {
                    "width": 1920,
                    "height": 1080,
                    "deviceScaleFactor": 1
                },
                "geolocation": {
                    "latitude": 41.6941,
                    "longitude": 44.8337,
                    "accuracy": 45
                },
                "blockedResourceTypes": ["BlockCssAssets", "BlockImages", "BlockFonts", "BlockIcons", "BlockMedia"],
                "locale": "ru-GE"
            },
            "script": self.__get_script(url)
        })
        headers = {
            'Authorization': self.__auth_password,
            'Content-Type': 'application/json'
        }
        async with ClientSession() as session:
            response = await session.post(f"{self.__browser_url}/task", headers=headers,
                                          data=payload)
            j = await response.json()
            task_status = j["status"]
            if task_status == "FAILED" or task_status == "INIT_ERROR" or task_status == "TIMEOUT" or task_status =="BAD_ARGS":
                raise Exception(f"WRONG TASK STATUS IN GET CATALOGUE: {task_status}")
            return j["output"]
