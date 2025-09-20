FROM python:3.9.13


# installing the Python dependencies
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir celery[redis]

# copying the contents of our app' inside the container
RUN mkdir /backend
COPY ./backend ./backend
WORKDIR /backend
