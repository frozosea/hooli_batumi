import os
from dotenv import load_dotenv
from request import BrowserRequest
from request import SimpleRequest
from scrapper import Parser
from service import Service
from transport import Transport
from repository import ProxyRepository

if __name__ == '__main__':
    try:
        load_dotenv()
    except Exception:
        print("No .env file")

    proxies = os.environ.get("PROXIES")
    if not proxies:
        proxies = ""

    proxy_repository = ProxyRepository([proxy for proxy in proxies.split(";")])

    allowed_users = [int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]

    USE_BROWSER = int(os.environ.get("USE_BROWSER"))
    if USE_BROWSER == 1:
        request = BrowserRequest(os.environ.get("BROWSER_URL"), os.environ.get("AUTH_PASSWORD"),
                                 os.environ.get("MACHINE_IP"))
    else:
        requests = SimpleRequest()

    parser = Parser()
    service = Service(request=request, parser=parser,
                      repository=proxy_repository)
    Transport(token=os.environ.get("BOT_TOKEN"), allowed_users=allowed_users, service=service).start()
