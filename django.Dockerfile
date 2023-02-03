FROM python:3.10.9-slim-buster

COPY ./setup/django-env/requirements.txt ./setup/gunicorn/entrypoint.sh /

RUN apt update && apt-get upgrade -y && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx gcc default-libmysqlclient-dev

RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["sh", "/entrypoint.sh"]