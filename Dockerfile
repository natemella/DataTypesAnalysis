FROM srp33/shinylearner:version515

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt \
    && git clone https://github.com/natemella/DataTypesAnalysis.git \
    && mkdir /DataTypesAnalysis/InputData \

#COPY InputData/ DataTypesAnalysis/InputData

