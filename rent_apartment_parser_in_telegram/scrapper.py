import re
from abc import ABC
from abc import abstractmethod
from typing import Type
from typing import List

from entity import Category


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
        return None


class IMessageChecker(ABC):
    @abstractmethod
    def check(self, message: str) -> bool:
        ...


class MessageChecker(IMessageChecker):
    @staticmethod
    def check_owner_contains(message: str) -> bool:
        for word in ("собственник", "собственника", "собственница","собственницы", "owner", "landlord"):
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


class IMessageParser(ABC):

    @abstractmethod
    def get_category(self, categories: List[Category], message: str) -> Category:
        ...


class MessageParser(IMessageParser):
    def __init__(self, message_checker: Type[IMessageChecker], number_parser: Type[INumberParser]):
        self.message_checker = message_checker
        self.number_parser = number_parser

    def get_category(self, categories: List[Category], message: str) -> Category:
        number = self.number_parser.parse(message=message)
        for category in categories:
            if eval(category.Eval.format(number)):
                return category
        raise
