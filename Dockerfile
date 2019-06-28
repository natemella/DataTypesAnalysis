FROM srp33/shinylearner_gpu:version515
ADD Algorithms.txt /DataTypesAnalysis/Algorithms.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && git clone https://github.com/natemella/DataTypesAnalysis.git \
    && mkdir DataTypesAnalysis/InputData \
    && mkdir DataTypesAnalysis/Analysis_Results \
    && mkdir DataTypesAnalysis/Permanent_Results \
    && find DataTypesAnalysis/ -type d -exec chmod 755 {} \;

#COPY InputData/ DataTypesAnalysis/InputData

