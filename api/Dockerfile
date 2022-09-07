FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin -y

COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/