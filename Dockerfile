FROM python:3.10-slim

WORKDIR /main

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts ./scripts
COPY src ./src

RUN chmod +x ./scripts/*.sh

EXPOSE 8080

CMD ["./scripts/run.sh"]