FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential python3-dev default-libmysqlclient-dev pkg-config ffmpeg  \
    && pip3 install --no-cache-dir --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD [ "python3","consumer.py" ]