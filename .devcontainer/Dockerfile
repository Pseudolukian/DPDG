FROM python:3.10.12-slim

WORKDIR /workspace

RUN mkdir -p /home/ivan/dpdg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
