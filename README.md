# data-engineering-twitter



by Romane Thoirey and Jeremy Trullier

This project is a small web application.

Its purpose is to find tweets that are similar from the user's input tweet.

The application can be easily deployable thanks to a Docker image.

The web app can be monitored with Prometheus and stats can be viewed with Grafana.

The model we use to find similar tweets is glove and we use cosine distance inspired by this repo : https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
