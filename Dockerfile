FROM python:3.10-slim-buster

RUN apt update && apt install ffmpeg build-essential -y

WORKDIR /app

COPY ./pythonbot.py /app/

# RUN mkdir /app/profile

# COPY ./config.ini /app/

# COPY ./profile /app/profile/

VOLUME [ "/app/config" ]

RUN python3 -m pip install -U "py-cord[voice]"

RUN python3 -m pip install -U py-cord --pre

RUN python3 -m pip install -U yt_dlp youtube-search-python scrapetube

CMD [ "python", "pythonbot.py" ]