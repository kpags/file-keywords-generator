FROM python:3.12.6

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get clean

RUN pip install --upgrade pip
COPY ./app/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

COPY ./app/entrypoint.sh /usr/src/app/entrypoint.sh

COPY ./app /usr/src/app

ENTRYPOINT ["/bin/bash", "/usr/src/app/entrypoint.sh"]
CMD ["gunicorn", "keywords_generator.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "30", "--workers", "2"]
