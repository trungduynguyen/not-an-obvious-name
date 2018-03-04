FROM python:3.6.4

WORKDIR /

COPY . ./

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "./main.py" ]