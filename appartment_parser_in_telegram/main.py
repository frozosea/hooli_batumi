import json
import logging
import os
from typing import List
from dotenv import load_dotenv
from entity import Category
from parser import NumberParser
from parser import MessageChecker
from parser import MessageParser
from transport import Transport


def get_categories() -> List[Category]:
    with open("config.json", "r") as file:
        return json.loads(file.read())


if __name__ == '__main__':
    try:
        load_dotenv()
    except:
        print("no .env file")
    categories = get_categories()



    number_parser = NumberParser()
    message_checker = MessageChecker()
    message_parser = MessageParser(message_checker, number_parser)


    transport = Transport(os.environ.get("API_ID"), os.environ.get("API_HASH"), message_checker, message_parser,
                          categories)

    transport.start()
