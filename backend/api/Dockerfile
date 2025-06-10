FROM python:3.13

WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt
COPY . .

VOLUME /data
EXPOSE 8000

CMD ["fastapi", "run", "main.py"]
