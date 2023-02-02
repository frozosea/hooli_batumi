import json
import re
from abc import ABC
from abc import abstractmethod

import requests
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
        headers = {
            'authority': 'ss.ge',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4',
            # 'cookie': 'modal_shown_landing_realestate=0; screenResolution2=true; wallindex=6; __zlcmid=1E3lXokgBejqm2h; _hjSessionUser_550566=eyJpZCI6IjBlZTE3MTBjLTRlZTItNTk3MC05MDU4LWRiNzJlMmY3ZTc5MCIsImNyZWF0ZWQiOjE2NzQzNjc5MDM2NzQsImV4aXN0aW5nIjp0cnVlfQ==; RealEstateType=Flat; viewed-application-ids=%5B6167275%2C6120686%2C3232163%2C5710876%2C6168693%2C5253181%2C5746789%2C6178540%2C6172355%2C6159087%2C6049980%2C6214507%2C6195952%2C6189460%2C6214425%2C5304996%2C4964932%2C4238485%2C6183717%2C5903560%2C4429856%2C6215258%2C6162647%2C6181154%2C3745633%2C2960253%2C6204266%2C6195915%2C6211692%2C5798420%2C6182952%2C6117100%2C6140818%2C3225758%2C6224548%2C6232208%5D; _gid=GA1.2.747596871.1675244663; RealEstateDealType=For%20Rent; ListingLink=https%3A%2F%2Fss.ge%2Fru%2F%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C%2Fl%2F%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0%2F%D0%90%D1%80%D0%B5%D0%BD%D0%B4%D0%B0; .AspNetCore.Antiforgery.ZQZ9-5TPDZ8=CfDJ8BVgksY10KhBgxIHE4YE-KR7MTQqa7nhyubvKHPR6NsSGrjuJ8qM1NzoDNNCbzW_zuOe576rijSah1ObuUrVVrnFp6QUkHqmSZwG2Y98ux8Y-OWomtKWI9dwTs6gGP-LK-erYmyjQItnxlxMalsZvss; _hjIncludedInSessionSample=0; _hjSession_550566=eyJpZCI6ImJlZmEyZjA4LWZiNTMtNGMwYy05OTJiLWI2MGYyOTAyMjcxNiIsImNyZWF0ZWQiOjE2NzUzMTc1MDAwNzYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga=GA1.1.83976452.1674367903; _ga_6TNNPZXX61=GS1.1.1675317502.24.1.1675317511.51.0.0',
            'referer': 'https://ss.ge/ru/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        if proxy:
            if "http" in proxy:
                response = requests.get(url, headers=headers, proxies={"http": proxy})
            elif "https" in proxy:
                response = requests.get(url, headers=headers, proxies={"https": proxy})
            else:
                raise Exception("wrong proxy url")
        else:
            response = requests.get(url, headers=headers)
        print(response.status_code)
        return response.text
