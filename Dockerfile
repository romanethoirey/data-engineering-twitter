FROM python:3.7

USER root
WORKDIR /home

COPY requirements.txt .

ENV FLASK_APP=webapp.py
ENV FLASK_ENV=development
ENV TEMPLATES_AUTO_RELOAD = True

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

RUN python *.py

CMD [ "python", "webapp.py" ]
