FROM python:3.12-alpine3.17
RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR app/

EXPOSE 80

LABEL authors="Inncent"

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]