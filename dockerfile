FROM python:3.10.12-slim-bookworm

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TORBOX_API_KEY=
ENV MOUNT_METHOD=strm
ENV MOUNT_PATH=/torbox

CMD ["python", "main.py"]