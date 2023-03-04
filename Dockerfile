FROM python:3.10

RUN apt update && apt-get install ffmpeg libsm6 libxext6 -y

RUN mkdir /HexOceanTask

WORKDIR /HexOceanTask

COPY / ./src
COPY /requirements.txt ./requirements.txt
COPY /.env ./.env
COPY /commands ./commands
COPY /db.json ./db.json

RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt

CMD ["sh", "-c", "python src/manage.py makemigrations && \
                  python src/manage.py migrate && \
                  python src/manage.py collectstatic --noinput && \
                  python src/manage.py loaddata db.json && \
                  python src/manage.py runserver 0:$WSGI_PORT"]
