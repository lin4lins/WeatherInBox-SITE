FROM python:3.10-alpine3.16
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /site
COPY requirements.txt /site/
RUN pip install -r requirements.txt
COPY . /site/