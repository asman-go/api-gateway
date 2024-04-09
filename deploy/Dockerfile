FROM python:3.10-alpine

LABEL maintainer="Olep Petrakov <murami.ike@gmail.com>"

WORKDIR /code

COPY . .

RUN pip install "."

CMD ["python", "src/gateway/app.py"]
