from __future__ import annotations
from facebook_scraper import get_posts
import json
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Type
from entity import Message
from request import IRequest


class IFacebookMessageProvider(ABC):
    @abstractmethod
    def get(self, cookie_path: str) -> List[Message]:
        ...


class FacebookMessageProvider(IFacebookMessageProvider):
    def __init__(self, limit: int, group_id: str | int):
        self.__limit = limit
        self.__group_id = group_id

    def __convert(self, messages: List[dict]):
        l = []
        for item in messages:
            text = item.get("post_text") if item.get("post_text") else item.get("text")
            c = Message(message=text, url=item.get("post_url"),
                        user_url=f"https://www.facebook.com/groups/{self.__group_id}/user/{item.get('user_id')}",
                        date=item.get("time"), images=item.get('images') if item.get('images') else [])
            l.append(c)
        return l

    def get(self, cookie_path: str) -> List[Message]:
        messages = []
        for post in get_posts(self.__group_id, cookies=cookie_path, timeout=10000):
            print(post)
            messages.append(post)
            if len(messages) == self.__limit:
                break
        return self.__convert(messages)
