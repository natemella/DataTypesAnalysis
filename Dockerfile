FROM srp33/shinylearner:version515

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && git clone https://github.com/natemella/DataTypesAnalysis.git \
    && mkdir DataTypesAnalysis/InputData \
    && mkdir DataTypesAnalysis/Analysis_Results

#COPY InputData/ DataTypesAnalysis/InputData

