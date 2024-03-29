FROM python:3.10

COPY . /worker
WORKDIR /worker

RUN apt update -qqy \
    && apt install --no-install-recommends git curl ffmpeg -qqy \
    && pip install -U -r requirements.txt \
    && git clone --depth=1 https://github.com/galihmrd/addon-vc etc \
    && rm -rf /var/lib/apt/lists/*

CMD python3 -m lib
