FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y --no-install-recommends install \
    postgresql-client \
    python-setuptools \
    python-dev \
    git-core \
    telnet \
    netcat \
    jq \
    libfontconfig \
    xfonts-utils \
    xfonts-75dpi \
    xfonts-base \
    libpng16-16 \
    libssl1.0.2

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app
EXPOSE 8000
