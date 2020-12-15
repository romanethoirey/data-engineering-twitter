FROM python:3.7

USER root
WORKDIR /home

COPY requirements.txt .

ENV FLASK_APP=webapp.py
ENV FLASK_ENV=production
ENV TEMPLATES_AUTO_RELOAD=True

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 8000

# Preprocess python script before launching the app (only do it once)
RUN python tweets.py

# RUN python webapp.py
CMD [ "python", "webapp.py" ]
