FROM python:3

COPY requirements.txt stats.py  /
WORKDIR /
RUN pip3 install -r requirements.txt
CMD [ "python3", "stats.py" ]
