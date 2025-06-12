FROM python:3.13

WORKDIR /app

COPY backend/pyproject.toml .
COPY backend/src/ocrchive/api api

RUN pip install .[api]

VOLUME /data
EXPOSE 8000

CMD ["fastapi", "run", "main.py"]

