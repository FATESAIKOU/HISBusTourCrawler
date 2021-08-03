FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y apt-utils ssh netcat jq psmisc && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y chromium-browser udev chromium-chromedriver

RUN pip3 install --upgrade pip && pip3 install beautifulsoup4 requests selenium ipython boto3

# Set Lang
ENV LANG C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /project
