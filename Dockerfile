FROM python

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=soccer_player.settings

CMD [ "python3","manage.py","runserver","0.0.0.0:8000" ]

