FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin -y

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

RUN chmod +x /code/bin/wait-for-it.sh
CMD /code/bin/wait-for-it.sh db:5432 -s -t 5 -- python manage.py migrate \
    && python manage.py runserver 0.0.0.0:8000