FROM ubuntu:latest
ADD slave.py /
RUN apt-get -y update && apt-get install -y python3 
RUN apt-get install -y python3-pip
RUN pip3 install -U numpy
RUN pip3 install -U scipy
RUN pip3 install -U scikit-learn