FROM python:3.8-slim-buster
RUN mkdir myhome_schedule_bot
WORKDIR /myhome_schedule_bot
RUN pip3 install aiogram aiohttp lxml bs4 python-dotenv apscheduler SQLAlchemy aiohttp-socks
COPY . /myhome_schedule_bot
ENV PYTHONPATH "${PYTHONPATH}:/myhome_schedule_bot"
CMD ["python", "main.py"]
