FROM python:3.9.0-slim

WORKDIR /transform

RUN apt-get update && apt-get install -y git

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY transformers/ transformers/
COPY transform.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/transform/entrypoint.sh" ]