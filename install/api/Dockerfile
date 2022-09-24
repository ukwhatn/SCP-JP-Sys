FROM python:3.10-alpine

WORKDIR /app

# upgrade pip/setuptools
RUN apk update

RUN apk add \
   alpine-sdk \
   build-base \
   postgresql-dev \
   postgresql-client \
   tzdata \
   git


RUN pip install --upgrade pip setuptools

# install packages from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
