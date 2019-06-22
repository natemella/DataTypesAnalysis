FROM python:3.6-slim-stretch

WORKDIR /usr/src/DataTypesAnalysis

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python"]

