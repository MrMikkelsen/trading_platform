FROM python:3.9-slim-buster


COPY ./time/requirements.txt .

RUN pip install -r requirements.txt

RUN pip install --no-cache-dir gunicorn

RUN mkdir /time
COPY ./time ./time
WORKDIR /time

CMD ["gunicorn", "-b", "0.0.0.0:5004", "app:app"]
