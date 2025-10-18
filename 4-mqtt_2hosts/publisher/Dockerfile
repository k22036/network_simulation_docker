FROM python:3.9-slim

WORKDIR /app

RUN pip install paho-mqtt
RUN apt-get update && apt-get install -y tcpdump

COPY . .

RUN chmod +x publish.sh

CMD ["tail", "-f", "/dev/null"]