FROM --platform=linux/amd64 python:3.10.12-bookworm

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TORBOX_API_KEY=

CMD ["python", "main.py"]