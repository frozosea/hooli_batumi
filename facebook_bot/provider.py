from abc import ABC
from abc import abstractmethod
from typing import Type
from typing import List
from delivery import ClientMessageDelivery
from delivery import SaleObjectDelivery
from delivery import RentObjectDelivery
from scrapper import ClientOnRentParser
from scrapper import ClientOnBuyParser
from scrapper import SaleObjectParser
from scrapper import RentObjectParser
from scrapper import CategoryParser
from scrapper import INumberParser
from repository import IRepository
from entity import Message
from entity import Category


class IProvider(ABC):
    @abstractmethod
    async def provide(self, message: Message) -> None:
        ...


class ClientOnRentProvider(IProvider):
    def __init__(self, repository: Type[IRepository], bot, chat_id: int):
        self._repository = repository
        self._parser = ClientOnRentParser()
        self._delivery = ClientMessageDelivery(bot, chat_id)

    async def provide(self, message: Message) -> None:
        try:
            if self._parser.check(message.message):
                if not self._repository.exists(message.message):
                    print(message)
                    self._repository.add(message.message)
                    await self._delivery.send(message)
        except Exception as e:
            print(f"CLIENT PROVIDER EXCEPTION: {e}")


class ClientOnBuyProvider(ClientOnRentProvider):
    def __init__(self, repository: Type[IRepository], bot, chat_id: int):
        super().__init__(repository, bot, chat_id)
        self._parser = ClientOnBuyParser()


class PropertySaleObjectProvider(IProvider):
    def __init__(self, repository: Type[IRepository], bot, chat_id: int):
        self.__repository = repository
        self.__parser = SaleObjectParser()
        self.__delivery = SaleObjectDelivery(bot, chat_id)

    async def provide(self, message: Message) -> None:
        try:
            if self.__parser.check(message.message):
                if not self.__repository.exists(message.message):
                    print(message)
                    await self.__delivery.send(message)
                    self.__repository.add(message.message)

        except Exception as e:
            print(f"SALE OBJECT PROVIDER EXCEPTION: {e}")


class PropertyRentObjectProvider(IProvider):
    def __init__(self, repository: Type[IRepository], bot, number_parser: Type[INumberParser],
                 categories: List[Category]):
        self.__repository = repository
        self.__parser = RentObjectParser()
        self.__delivery = RentObjectDelivery(bot, 1)
        self.__category_parser = CategoryParser(number_parser)
        self.__categories = categories

    async def provide(self, message: Message) -> None:
        try:
            if self.__parser.check(message.message):
                if not self.__repository.exists(message.message):
                    try:
                        category = self.__category_parser.get_category(self.__categories, message.message)
                        print(category)
                        await self.__delivery.send(message, category.GroupId)
                        self.__repository.add(message.message)
                    except Exception as e:
                        print(f"GET CATEGORY ERROR: {e}")
                        await self.__delivery.send(message, self.__categories[0].GroupId)
        except Exception as e:
            print(f"SALE OBJECT PROVIDER EXCEPTION: {e}")
