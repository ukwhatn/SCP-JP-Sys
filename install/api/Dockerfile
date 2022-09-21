FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

# requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
