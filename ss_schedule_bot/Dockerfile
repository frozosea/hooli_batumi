FROM python:3.8-slim-buster
RUN mkdir ss_schedule_bot
WORKDIR /ss_schedule_bot
RUN pip3 install --upgarde pip3
RUN pip3 install aiogram aiohttp lxml bs4 python-dotenv apscheduler SQLAlchemy
COPY . /ss_schedule_bot
ENV PYTHONPATH "${PYTHONPATH}:/ss_schedule_bot"
CMD ["python", "main.py"]
