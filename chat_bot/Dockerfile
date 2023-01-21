FROM python:3.8-slim-buster
RUN mkdir app
WORKDIR /app
RUN pip3 install telethon python-dotenv
COPY . .
CMD [ "python3","main.py"]