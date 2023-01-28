FROM python:3.8-slim-buster
WORKDIR /myhome_schedule_bot
RUN pip3 install aiogram aiohttp lxml bs4 python-dotenv apscheduler
COPY . /usr/src/app
ENV PYTHONPATH "${PYTHONPATH}:/myhome_schedule_bot"
CMD ["python", "app/main.py"]
