FROM python:3.8-slim-buster
RUN mkdir app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install aiogram aiohttp lxml bs4
COPY . .
CMD [ "python3","main.py"]