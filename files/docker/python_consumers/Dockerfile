FROM python:3.7-buster

### -------------------------------------------------
### METADATA INFORMATION
### -------------------------------------------------
LABEL name="Kafka consumer container"
LABEL maintainer="Calvin Remsburg"
LABEL description="apache kafka consumer container image"
LABEL url="https://github.com/packetferret/ELK-Kafka"
LABEL build-date="20200524"

### -------------------------------------------------
### Set environment
### -------------------------------------------------
ENV LANG C.UTF-8
ENV PYTHON_VERSION 3.7

### -------------------------------------------------
### Install packages
### -------------------------------------------------
RUN apt install -y gcc

### -------------------------------------------------
### Working directory
### -------------------------------------------------
WORKDIR /home/tmp

### -------------------------------------------------
### Add and install python packages
### -------------------------------------------------
ADD config/requirements.txt requirements.txt
RUN pip install -r requirements.txt

### -------------------------------------------------
### Working directory
### -------------------------------------------------
WORKDIR /home/python

### -------------------------------------------------
### run python3
### -------------------------------------------------
CMD ["python3"]