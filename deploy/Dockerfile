FROM python:3.10
# -alpine

LABEL maintainer="Olep Petrakov <murami.ike@gmail.com>"

# RUN apk add --no-cache gcc libcurl libstdc++ curl-dev
# install git
# RUN apk add --no-cache git
RUN apt install git


WORKDIR /code

COPY . .

RUN pip install -r requirements.git.txt
RUN pip install "."

CMD ["python", "src/gateway/app.py"]
