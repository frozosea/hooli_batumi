import re
from typing import List
from typing import Type
from abc import ABC
from abc import abstractmethod
from entity import Category


class IParser(ABC):
    @abstractmethod
    def check(self, message: str) -> bool:
        ...


class ClientParser(IParser):
    @staticmethod
    def __check_contains_give_rent_messages(message: str) -> bool:
        for word in ["сдам", "сдается", "сдадим", "сдаётся"]:
            if word in message.lower():
                return True
        return False

    def check(self, message: str) -> bool:
        for word in ["сниму", "снимем", "снять", "снимаем", "арендовать", "аренда", "арендуем",
                     "арендую",
                     "rent", "arenduem", "snimem", "snimu", "sniat'", "sniat"]:
            if word in message.lower() and not self.__check_contains_give_rent_messages(message):
                return True
        return False


class SaleObjectParser(IParser):
    @staticmethod
    def check_owner_contains(message: str) -> bool:
        for word in (
                "собственник", "собственника", "собственница", "собственницы", "собственнице", "собственнику", "owner",
                "landlord", "sobstvennik", "sobstvenik", "sobstvenic", "sobstvenica", "sobstvenicy", "sobstvenicu",
                "sobstveniky", "sobstveniku"):
            if word in message.lower():
                return True
        return False

    @staticmethod
    def check_message_type(message: str) -> bool:
        for word in ["продам", "продаю", "продается", "продадим", "продажа", "продажу", "продаже", "sale", "sales",
                     "prodam", "prodayu", "prodau", "proday", "prodaetsya", "prodaetsa", "prodaeza", "prodadim",
                     "prodazha", "prodaza", "prodazhu", "prodazhy", "prodazhe", "prodazh"]:
            if word in message.lower():
                return True
        return False

    def check(self, message: str) -> bool:
        return self.check_owner_contains(message) and self.check_message_type(message)


class RentObjectParser(IParser):
    @staticmethod
    def check_owner_contains(message: str) -> bool:
        for word in (
                "собственник", "собственника", "собственница", "собственницы", "собственнице", "собственнику", "owner",
                "landlord", "sobstvennik", "sobstvenik", "sobstvenic", "sobstvenica", "sobstvenicy", "sobstvenicu",
                "sobstveniky", "sobstveniku"):
            if word in message.lower():
                return True
        return False

    @staticmethod
    def check_message_type(message: str) -> bool:
        for word in ["сдаю", "сдам", "сдадим", "сдается", "здам", "здадим", "здается", "zdaiotsya", "zdaetsya",
                     "zdadim", "zdam", "zdadu", "сдаду"]:
            if word in message.lower():
                return True
        return False

    def check(self, message: str) -> bool:
        return self.check_owner_contains(message) and self.check_message_type(message)


class INumberParser(ABC):
    @abstractmethod
    def parse(self, message: str) -> int:
        ...


class NumberParser(INumberParser):
    def parse(self, message: str) -> int:
        raw = [item.group() for item in re.finditer(
            r"\d+\s*(долларов|\$|usd|dollar|dollars|баксов|у\.е|д\.|уе)|(долларов|\$|usd|dollar|dollars|баксов|у\.е|д\.|уе)\s*\d+",
            message)][0]
        number = int(re.findall(r"\d{3,5}", raw)[0])
        if number > 200:
            return number
        return 0


class CategoryParser:
    def __init__(self, number_parser: Type[INumberParser]):
        self.number_parser = number_parser

    def get_category(self, categories: List[Category], message: str) -> Category:
        number = self.number_parser.parse(message=message)
        for category in categories:
            if eval(category.Eval.format(number)):
                return category
        raise Exception("No category")
