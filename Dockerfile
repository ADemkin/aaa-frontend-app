# FROM python:3.8-alpine
FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN python -m pip install --upgrade pip
RUN mkdir /app

COPY ./requirements.txt ./dev-requirements.txt /app/

WORKDIR /app

RUN python -m pip install --no-cache-dir -r requirements.txt -r dev-requirements.txt

# pre download model
RUN python -c "import easyocr; easyocr.Reader(['en', 'ru'])"

COPY . /app

EXPOSE 8080
CMD ["python", "run.py"]
