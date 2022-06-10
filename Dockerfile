
#syntax=docker/dockerfile:1.2

####################################################################################################
# Python base

FROM ubuntu:20.04 as py-base
WORKDIR /usr/src/app

# Pre-install requirements
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY requirements.txt requirements.txt ./
RUN pip3 install -r requirements.txt

####################################################################################################
# Build file-collect app

FROM py-base as file-collect-app
COPY ./file-collect /usr/src/app
RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh

####################################################################################################
# Build file-upload app

FROM py-base as file-upload-app
COPY ./file-upload /usr/src/app
RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh
