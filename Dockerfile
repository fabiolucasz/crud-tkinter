FROM python:3.12

WORKDIR  /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=host.docker.internal:0.0
ENV XDG_RUNTIME_DIR=/tmp/runtime-docker

COPY . .


CMD ["python3", "main.py"]