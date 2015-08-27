FROM gliderlabs/alpine:3.2

RUN apk add --update \
    python3 \
    python3-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

CMD ["/env/bin/python", "genisysconnector.py"]
