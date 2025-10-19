FROM nicolaka/netshoot:latest

WORKDIR /app

RUN apk add --no-cache iproute2

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
