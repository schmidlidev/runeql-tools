FROM python:3

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY item_transformer.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]