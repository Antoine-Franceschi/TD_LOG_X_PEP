FROM python:3.9

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--config", "gunicorn.config.py" , "wsgi:my_app"]
