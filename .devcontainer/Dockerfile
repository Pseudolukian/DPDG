FROM python:3.10.12-slim

WORKDIR /workspace

COPY . /home/ivan/dpdg


RUN if ! command -v pip3 &> /dev/null; then \
        apt-get update && apt-get install -y python3-pip && \
        pip3 install --upgrade pip; \
    else \
        pip3 install --upgrade pip; \
    fi


WORKDIR /home/ivan/dpdg
RUN pip3 install --no-cache-dir -r requirements.txt

