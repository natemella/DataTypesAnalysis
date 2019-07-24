FROM srp33/shinylearner_gpu:version520
COPY Algorithms.txt ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && git clone https://github.com/natemella/DataTypesAnalysis.git \
    && mkdir DataTypesAnalysis/InputData \
    && mkdir DataTypesAnalysis/Analysis_Results \
    && mkdir DataTypesAnalysis/Permanent_Results \
    && mkdir OutputData \
    && export LANG=C.UTF-8 \
    && mv Algorithms.txt DataTypesAnalysis \
    && find DataTypesAnalysis/ -type d -exec chmod 755 {} \;

#COPY InputData/ DataTypesAnalysis/InputData

