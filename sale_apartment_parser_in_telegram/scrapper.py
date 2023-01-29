import re
from abc import ABC
from abc import abstractmethod
from typing import Type
from typing import List

from entity import Category


class IMessageChecker(ABC):
    @abstractmethod
    def check(self, message: str) -> bool:
        ...


class MessageChecker(IMessageChecker):
    @staticmethod
    def check_owner_contains(message: str) -> bool:
        for word in ("собственник", "собственника", "собственница", "собственницы", "owner", "landlord"):
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
