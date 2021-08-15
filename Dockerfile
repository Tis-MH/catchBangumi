FROM python
RUN mkdir /code
COPY ../kiss /code
WORKDIR /code
RUN pip3 install -r /code/requirements.txt
CMD "python3 /code/crawl24h.py"