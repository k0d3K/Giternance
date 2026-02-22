FROM python:3.12-slim
RUN apt-get update && apt-get install -y git
RUN mkdir -p /app/logs
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]
