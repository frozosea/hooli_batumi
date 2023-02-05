import datetime
import json
from abc import ABC
from abc import abstractmethod
from entity import Apartment
from models import Product
from typing import List


class IParser(ABC):
    @abstractmethod
    def parse(self, response: Product) -> Apartment:
        ...


class Parser(IParser):
    @staticmethod
    def __get_images_urls(response: Product) -> List[str]:
        try:
            object_id = response.product_id
            l = []
            for i in range(1, int(response.photos_count)):
                url = f"https://static.my.ge/myhome/photos/{response.photo}/large/{object_id}_{i}.jpg"
                l.append(url)
            return l
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def __get_address(response: Product):
        try:
            return f"{json.loads(response.name_json)['ru']}, {json.loads(response.pathway_json)['ru']}"
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def __get_usd_price(response: Product):
        try:
            return float(response.price)
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def __get_floor(response: Product):
        try:
            return int(response.floor)
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def __get_description(response: Product):
        try:
            return response.comment if response.comment else ""
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def __get_square(response: Product):
        try:
            return int(response.area_size_value)
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def __get_url(response: Product):
        try:
            return f"https://www.myhome.ge/ru/pr/{response.product_id}"
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def __get_add_date(response: Product):
        try:
            return response.order_date
        except Exception as e:
            print(e)
            return datetime.datetime.now()

    def parse(self, response: Product) -> Apartment:
        return Apartment(
            Id=response.product_id,
            AddDate=self.__get_add_date(response),
            Images=self.__get_images_urls(response),
            Address=self.__get_address(response),
            UsdPrice=self.__get_usd_price(response),
            Floor=self.__get_floor(response),
            Description=self.__get_description(response),
            Square=self.__get_square(response),
            Url=self.__get_url(response)
        )
