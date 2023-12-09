FROM python:3.9-alpine

COPY ./requirements.txt /requirements.txt
COPY ./invite /invite
WORKDIR /invite

# RUN python -m venv /py && \
RUN apk add python3 python3-dev python3-venv && \
    /py/bin/pip install --upgrade pip && \
    adduser --disabled-password --no-create-home django-user 

RUN /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"

USER django-user