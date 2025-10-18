# Docker
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_UP = $(DOCKER_COMPOSE) up -d
DOCKER_EXEC = docker exec -it

# tshark
TSHARK_R = tshark -r
TSHARK_OPTIONS = -q -z conv,tcp
# pcap directory
SUB_CAP_DIR = ./subscriber/output/tcp_dump
PUB_CAP_DIR = ./publisher/output/tcp_dump
# pcap files
SUB_FILE = $(SUB_CAP_DIR)/172.28.1.2.pcap
PUB_FILE = $(PUB_CAP_DIR)/172.28.1.1.pcap

CLUC_AVG_LATENCY_SCRIPT = ./cluc_avg_latency.sh
CLUC_TOTAL_BYTES_SCRIPT = ./cluc_total_bytes.sh


publish:
	$(DOCKER_EXEC) mqtt_publisher bash publish.sh

collect_pcks/subscriber:
	$(TSHARK_R) $(SUB_FILE) $(TSHARK_OPTIONS)
collect_pcks/publisher:
	$(TSHARK_R) $(PUB_FILE) $(TSHARK_OPTIONS)

cluc_avg_latency:
	$(CLUC_AVG_LATENCY_SCRIPT)
cluc_total_bytes/subscriber:
	$(CLUC_TOTAL_BYTES_SCRIPT) $(SUB_CAP_DIR)
cluc_total_bytes/publisher:
	$(CLUC_TOTAL_BYTES_SCRIPT) $(PUB_CAP_DIR)

up:
	$(DOCKER_COMPOSE_UP)
up/build:
	$(DOCKER_COMPOSE_UP) --build
stop:
	$(DOCKER_COMPOSE) stop
down:
	$(DOCKER_COMPOSE) down