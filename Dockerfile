FROM python:3-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY requirements.txt /code/
RUN apt-get update && apt-get -y install libpq-dev gcc netcat-openbsd
RUN pip install -r requirements.txt
COPY startup.sh /code/
COPY ./src/ /code/
ENTRYPOINT exec "/code/startup.sh"