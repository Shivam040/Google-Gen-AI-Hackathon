FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn[standard] google-cloud-firestore google-cloud-storage pydantic
COPY src /app/src
ENV PORT=8080
CMD ["uvicorn", "src.runner:app", "--host", "0.0.0.0", "--port", "8080"]
