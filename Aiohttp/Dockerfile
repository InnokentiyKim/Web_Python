FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR app/

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

ENTRYPOINT ["python3", "server.py", "run"]