FROM python:3.9.0-slim

WORKDIR /load_data

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY load_data.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/load_data/entrypoint.sh" ]