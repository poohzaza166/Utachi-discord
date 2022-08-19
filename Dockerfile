FROM python:3.10.6-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# ARG DOCKER_USER=default_user

# RUN addgroup -S $DOCKER_USER && adduser -S $DOCKER_USER -G $DOCKER_USER

RUN apt update && apt install ffmpeg build-essential htop apt-file libffi-dev libnacl-dev python3-dev -y

WORKDIR /app

RUN mkdir bot

COPY ./bot /app/bot

RUN ls

COPY requirements.txt /app/

RUN mkdir /app/config

RUN pip install -r requirements.txt

# RUN mkdir /app/profile

# COPY ./config.ini /app/

# COPY ./profile /app/profile/

VOLUME [ "/app/config/" ]

# RUN python3 -m pip install -U "py-cord[voice]"

# RUN python3 -m pip install -U "py-cord[speed]"

# RUN python3 -m pip install -U py-cord

# RUN python3 -m pip install -U yt_dlp youtube-search-python scrapetube ytmusicapi pyyaml spotipy google-api-python-client


CMD [ "python","-u","-m","bot"]