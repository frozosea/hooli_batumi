from abc import ABC
from abc import abstractmethod
from aiohttp import ClientSession


class IRequest(ABC):
    @abstractmethod
    async def send(self, url: str, proxy: str) -> str:
        ...


class Request:

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
        async with ClientSession() as session:
            response = await session.get(url, proxy=proxy)
        return await response.text()
