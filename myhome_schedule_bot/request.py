import json
import re
from abc import ABC
from abc import abstractmethod

from aiohttp import ClientSession


class IRequest(ABC):
    @abstractmethod
    async def send(self, url: str, proxy: str) -> str:
        ...


class BrowserRequest(IRequest):

    def __init__(self, browser_url: str, auth_password: str, machine_ip: str = None):
        self.__browser_url = browser_url
        self.__auth_password = auth_password
        self.__machine_ip = machine_ip

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
        p = {
            "options": {
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
        }
        if proxy:
            p["options"]["upstreamProxyUrl"] = proxy
            if self.__machine_ip:
                p["options"]["upstreamProxyIpMask"] = {
                    "ipLookupService": "api.ipify.org",
                    "proxyIp": re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", proxy)[0],
                    "publicIp": self.__machine_ip
                }
        payload = json.dumps(p)
        headers = {
            'Authorization': self.__auth_password,
            'Content-Type': 'application/json'
        }
        async with ClientSession() as session:
            response = await session.post(f"{self.__browser_url}/task", headers=headers,
                                          data=payload)
            j = await response.json()
            task_status = j["status"]
            if task_status == "FAILED" or task_status == "INIT_ERROR" or task_status == "TIMEOUT" or task_status == "BAD_ARGS":
                raise Exception(f"WRONG TASK STATUS IN GET APARTMENT INFO: {task_status}")
            return j["output"]


class SimpleRequest(IRequest):
    async def send(self, url: str, proxy: str) -> str:
        if proxy:
            if "socks" in proxy:
                connector = aiohttp_socks.ProxyConnector.from_url(proxy)
                async with ClientSession(connector=connector) as session:
                    response = await session.get(url, proxy=proxy)
            elif "http" in proxy or "https" in proxy:
                async with ClientSession() as session:
                    response = await session.get(url, proxy=proxy)
            else:
                raise Exception("wrong proxy url")
        else:
            async with ClientSession() as session:
                response = await session.get(url)
        return await response.text()
