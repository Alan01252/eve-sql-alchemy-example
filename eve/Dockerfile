FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
# PATCH Broken oplog in eve version 0.7
RUN sed -i 's#or resource in config.URLS#or resource not in config.URLS#g' /usr/local/lib/python3.6/site-packages/eve/methods/common.py
CMD python ./code/run.py
