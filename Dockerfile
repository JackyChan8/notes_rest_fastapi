FROM python:3.11.8-slim

WORKDIR /opt/app
ENV PYTHONPATH="/opt/app/src"
ENV PYTHONWARNINGS=ignore

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]
