FROM python:3.8-slim-buster
RUN mkdir app
WORKDIR /app
RUN pip3 install aiogram aiohttp lxml bs4 python-dotenv apscheduler random_user_agent playwright
RUN playwright install
COPY . .
CMD [ "python3","main.py"]