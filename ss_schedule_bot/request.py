import json
from abc import ABC
from abc import abstractmethod

import requests
from aiohttp import ClientSession


class IRequest(ABC):
    @abstractmethod
    async def send(self, url: str, proxy: str) -> str:
        ...


class BrowserRequest(IRequest):

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
        await sleep(200);
        const modalDialog = await agent.querySelector('#WarningPopUp > div > div > div.modal-footer > a');
        if (modalDialog) {
            await modalDialog.$click()
        };
        let selector = await agent.document.querySelector('#list > div:nth-child(5)');
        while (!selector) {
            await sleep(50);
            selector = await agent.document.querySelector('#list > div:nth-child(5)');
        };
        resolve(await agent.document.documentElement.innerHTML);
})();""" % url

    async def send(self, url: str, proxy: str) -> str:
        payload = json.dumps({
            "options": {
                "upstreamProxyUrl": proxy
            },
            "script": self.__get_script(url)
        })
        headers = {
            'Authorization': self.__auth_password,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(url, proxies={"socks": proxy})
            if response.status_code > 220:
                raise
            return response.text
        except Exception as e:
            print(e)
            async with ClientSession() as session:
                response = await session.post(f"{self.__browser_url}/task", headers=headers, data=payload, )
                j = await response.json()
                task_status = j["status"]
                if task_status == "FAILED" or task_status == "INIT_ERROR" or task_status == "TIMEOUT" or "BAD_ARGS":
                    raise
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