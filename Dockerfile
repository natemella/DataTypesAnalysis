FROM python:3.6-slim-stretch

LABEL maintainer="Nate <nathanmell@gmail.com>"
LABEL version="0.1"

WORKDIR /DataTypesAnalysis

RUN pip install pandas
RUN pip install numpy
RUN pip install roman


CMD python ./DataTypesAnalysis/cutter.py OS -c True

