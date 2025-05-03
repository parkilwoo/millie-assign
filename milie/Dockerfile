FROM python:3.12-slim

WORKDIR /app

COPY milie/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY milie ./milie

EXPOSE 8000

ENV PYTHONPATH=/app:/app/milie

# Start the FastAPI application
CMD ["uvicorn", "milie.main:app", "--host", "0.0.0.0", "--port", "8000"]