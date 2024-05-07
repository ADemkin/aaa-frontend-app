FROM python:3.12-slim

# to use uv without virtualenv
ENV VIRTUAL_ENV=/usr/local
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app

COPY ./requirements.txt ./requirements-dev.txt /app

WORKDIR /app

RUN pip install --upgrade pip uv
RUN uv pip install --no-cache -r requirements.txt -r requirements-dev.txt
# pre download model
RUN python -c "import easyocr; easyocr.Reader(['en'], verbose=False)"

COPY . /app

EXPOSE 8080
CMD ["python", "run.py"]
