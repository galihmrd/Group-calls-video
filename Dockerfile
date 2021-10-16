FROM python:3.9.7-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt-get install npm -y
RUN apt-get install git curl python3-pip ffmpeg -y
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g npm@7.22.0
RUN npm i -g npm
COPY . /workspace
WORKDIR /workspace
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD python3 -m lib
