FROM python:3

WORKDIR /

ADD . /

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python", "./bitcoin_price.py" ]