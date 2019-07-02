
# FROM alpine:latest
FROM python:3.7-alpine
LABEL maintainer="Shabalkov Iakov <shabalkov92@gmail.com>"

RUN adduser -D gh_wrapper

ENV TERM=xterm

ARG TZ=Asia/Yekaterinburg

ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_CTYPE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    SETTINGS=settings \
    PYTHONPATH=.
# RUN apk add --update --no-cache socat curl tzdata findutils
RUN apk add --update --no-cache tzdata

RUN apk add --virtual .build-deps --no-cache --update gettext-dev git && \
    pip install colorlog PGen && \
    apk del .build-deps

# COPY requirements.txt requirements.txt
COPY . .

RUN pip install -r requirements.txt

ARG APP_PATH=/opt/graphhopper_wrapper

ADD ./ ${APP_PATH}
WORKDIR ${APP_PATH}

ENV FLASK_APP app.py

RUN chown -R gh_wrapper:gh_wrapper ./

USER gh_wrapper

EXPOSE 9990

CMD ["python", "app.py"]
