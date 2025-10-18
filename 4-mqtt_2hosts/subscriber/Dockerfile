FROM python:3.9-slim

WORKDIR /app

RUN pip install paho-mqtt
RUN apt-get update && apt-get install -y tcpdump iproute2

COPY . .

RUN chmod +x subscribe.sh && chmod +x delay.sh

CMD ["sh", "-c", "set -e; ./delay.sh && ./subscribe.sh"]