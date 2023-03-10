import json
import os
from typing import List
from dotenv import load_dotenv
from scrapper import MessageChecker

from transport import Transport
from repository import Repository

if __name__ == '__main__':
    try:
        load_dotenv()
    except:
        print("no .env file")
    message_checker = MessageChecker()

    transport = Transport(os.environ.get("API_ID"), os.environ.get("API_HASH"), message_checker,
                          int(os.environ.get("SEND_GROUP_ID")),
                          [int(item) for item in os.environ.get("STOP_LIST_IDS").split(";")], Repository().migrate())

    transport.start()
