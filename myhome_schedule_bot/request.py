import json
import re
import requests
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
        headers = {
            'authority': 'www.myhome.ge',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4',
            'cache-control': 'max-age=0',
            # 'cookie': 'rent_vote_close=2; CookieAgreement=1; _hjSessionUser_506434=eyJpZCI6IjE4ODVjMjIyLTgxMGYtNTViOC04Mjg3LTJiZDUxMTUxOWI2YiIsImNyZWF0ZWQiOjE2NzQwMjc4MjQxMzcsImV4aXN0aW5nIjp0cnVlfQ==; split_test=v1; Lang=ru; _gid=GA1.2.1499120970.1675075938; OpenPhones=eyIxMzg5NjA0MSI6WzFdLCIxNDE3ODQwNyI6WzFdLCIxNDIwMDgyNiI6WzFdLCIxNDI0MjE4NiI6WzFdLCIxMTk2MjM0OCI6WzFdLCIxMjMwNDk0OSI6WzFdLCIxNDE1NjU0OSI6WzFdLCIxNDA1ODQ0NiI6WzFdLCIxNDE4MzExOCI6WzFdLCIxNDIyNjUxNyI6WzFdLCIxMDgzOTM1NiI6WzFdLCIxMzc0NjE1MiI6WzFdLCIxMzIwNjQxNSI6WzFdLCIxNDI3MDY5OSI6WzFdLCIxMzQ1NDE3MyI6WzFdLCIxMzQ1NDIxNCI6WzFdLCIxNDA0MjAzNyI6WzFdfQ%3D%3D; _pk_id.9.dc53=5a5280a8a20d09e8.1674027847.43.1675246838.1675246837.; _ga=GA1.1.1258386832.1674027808; _ga_B3H1RB8TBF=GS1.1.1675308360.58.0.1675308360.0.0.0; PHPSESSID=3n4qmretbhd5ac6aob4ip1ngpu; AccessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ2IjoiMSIsImlhdCI6MTY3NTMxNzMxMiwiZXhwaXJlc19hdCI6MTY3NTMxNzk3MiwiZGF0YSI6eyJ1c2VyX2lkIjo0NjM1OTMyLCJ1c2VybmFtZSI6ImhvbGxpYWdlbnRAZ21haWwuY29tIiwic2Vzc2lvbl9pZCI6ImIyNjJhMWZjY2E5MDIyY2M0OWUxNDI1ZWM2MGUxNTVjMmIxYWNjMjNmNWMyN2Q0Nzk1YzlmZDYzZTE2NDhjM2FiMzIxZWNlNTVlMDk1MjkyMThlNmEwODNiMGI3ZDg1YmExZjk4ZmE5NzYzY2Q3MDViZWZjMmU2MDYzZjEzYjBjIiwibGl2b191c2VyX2lkIjoxMDA0OTc2MiwiZ2VuZGVyX2lkIjoxLCJiaXJ0aF95ZWFyIjoyMDAzLCJiaXJ0aF9kYXRlIjoiMDAwMC0wMC0wMCIsInBob25lIjoiNTY4NjU0MTIxIiwidXNlcl9uYW1lIjoiIiwidXNlcl9zdXJuYW1lIjoiIiwidHlwZV9pZCI6MH19.sUibNf3ntqVsY4-HcW4V3dLJYQNvuSZcHSBHDRMlPgo44v4QuC77IicYPI3LkSKhEpRgmSTM1SeJ4VLWvG_jv4SKcct_TBxuWuJfCNh3Ph1dio2-Ly09YmtFCPRRa_pbkI-FyYakvjfUJfS6qqDxKBj_xjx9G3iJsUIzEbduEefwVZsfYOo7RKz-zQUK_p76b1KecORhz7_qsgCbigPX_Qm4FD94hZ6EytpXgUcbYdPZKDa6sMmoHrG6WtkCwBZUbvX-_e-Q_69Nb7OBjn4f8lFfd_zr5Zm7eVVIMtFQe-BwARK4XFmouVhlezHzkc_2AOQ5T_PXda6OzEEHwuG-rw; Visited=14106124.13226246.14042037.13454214.13454173.14270699.14236884.11975027.13206415.13746152.11962348.10839356.14226517.14183118.14058446.14156549.12304949.14216819.14242186.14085160.14200826.14123517.14215308.14081894.14138422.14177473.14214711.14181348.14043049.14213793.14178407.14186092.14202353.14020265.13896041.14198573.12368104.14214897.14191518.13373830.14186139.14185709.13630067.11870912',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
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
