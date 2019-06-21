FROM python:3.6-slim-stretch

ADD DataStandardization /

RUN pip install pandas
RUN pip install numpy
RUN pip install roman




