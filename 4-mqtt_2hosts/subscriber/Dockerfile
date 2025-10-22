FROM python:3.14-slim

WORKDIR /app

RUN pip install paho-mqtt
RUN apt-get update && apt-get install -y tcpdump iproute2 netcat-openbsd mosquitto

COPY . .

RUN chmod +x subscribe.sh && chmod +x delay.sh && \
    chmod +x receive_tcp.sh

CMD ["sh", "-c", "set -e; ./delay.sh && ./subscribe.sh"]