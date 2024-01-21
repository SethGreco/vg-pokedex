FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /fast_api .

EXPOSE 8000

CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "fast_api.main:app"]