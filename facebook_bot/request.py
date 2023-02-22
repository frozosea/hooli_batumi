import asyncio
import json
from abc import ABC
from abc import abstractmethod

import aiofiles
from selenium import webdriver
from selenium.webdriver.common.by import By


class IRequest(ABC):
    @abstractmethod
    async def get_cookies_filepath(self):
        ...


class Request(IRequest):
    def __init__(self, login, password, cookie_path, driver_path="/usr/lib/chromium-browser/chromedriver"):
        self.__login = login
        self.__password = password
        self.__driver_path = driver_path
        self.__cookie_path = cookie_path
        self.__driver = self.__init_webdriver()

    def __init_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("start-maximize")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.headless = True
        return webdriver.Chrome(self.__driver_path, chrome_options=chrome_options)

    async def get_cookies_filepath(self):
        self.__driver.get("https://www.facebook.com/login")
        self.__driver.find_element(By.CSS_SELECTOR, "#email").send_keys(self.__login)
        self.__driver.find_element(By.CSS_SELECTOR, "#pass").send_keys(self.__password)
        self.__driver.find_element(By.CSS_SELECTOR, "#loginbutton").click()
        await asyncio.sleep(90)
        async with aiofiles.open(self.__cookie_path, "w") as file:
            await file.write(json.dumps(self.__driver.get_cookies()))
        self.__driver.close()
        return self.__cookie_path
