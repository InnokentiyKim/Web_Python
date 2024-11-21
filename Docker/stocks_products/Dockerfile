FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR app/

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENV DB_NAME='stocks_db.sqlite3'

RUN ["python3", "manage.py", "migrate"]

CMD ["python3", "manage.py", "runserver"]