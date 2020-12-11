FROM python:3

WORKDIR /transform

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY item_transformer.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/transform/entrypoint.sh" ]