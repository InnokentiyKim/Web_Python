FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR app/

COPY ./requirements.txt .

RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

# RUN ["python3", "manage.py", "migrate"]

CMD ["gunicorn", "-b", "0.0.0.0:8000", "stocks_products.wsgi"] 