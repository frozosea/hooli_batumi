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
        await sleep(200)
        const modalDialog = await agent.querySelector("#WarningPopUp > div > div > div.modal-footer > a")
        if (modalDialog) {
            await modalDialog.$click()
        }
        let selector = await agent.document.querySelector('#list > div:nth-child(5)')
        while (!selector) {
            await sleep(50)
            selector = await agent.document.querySelector('#list > div:nth-child(5)')
        }
        resolve(await agent.document.documentElement.innerHTML);
})();""" % url

    async def send(self, url: str) -> str:
        return open("ss catalog from browser.html", "r").read()
        # async with ClientSession() as session:
        #     response = await session.post(f"{self.__browser_url}/task", headers={"Authorization": self.__auth_password},
        #                                   data={"script": self.__get_script(url)})
        #     print(response.status)
        #     j = await response.json()
        # with open("ss catalog from browser.html","w") as file:
        #     file.write(j["output"])
        # return j["output"]
