# Docker
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_UP = $(DOCKER_COMPOSE) up -d
DOCKER_COMPOSE_WITH_CLOUD = $(DOCKER_COMPOSE) -f docker-compose.with_cloud.yml
DOCKER_COMPOSE_UP_WITH_CLOUD = $(DOCKER_COMPOSE_WITH_CLOUD) up -d

DOCKER_EXEC = docker exec -i
DOCKER_EXEC_PUB = $(DOCKER_EXEC) mqtt_publisher
DOCKER_EXEC_SUB = $(DOCKER_EXEC) mqtt_subscriber

# tshark
TSHARK_R = tshark -r
TSHARK_COLLECT_OPTIONS = -q -z conv,tcp
TSHARK_SHOW_OPTIONS = -T fields -e frame.time -e ip.src -e ip.dst -e _ws.col.Info
# pcap directory
SUB_CAP_DIR = ./subscriber/output/tcp_dump
SUB_DEBUG_DIR = ./subscriber/output/debug
PUB_CAP_DIR = ./publisher/output/tcp_dump
# pcap files
SUB_FILE = $(SUB_CAP_DIR)/172.28.2.1.pcap
SUB_DEBUG_FILE = $(SUB_DEBUG_DIR)/172.28.2.1.pcap
PUB_FILE = $(PUB_CAP_DIR)/172.28.1.1.pcap
BROKER_FILE = ./broker/log/capture.pcap

CLUC_AVG_LATENCY_SCRIPT = ./cluc_avg_latency.sh
CLUC_TOTAL_BYTES_SCRIPT = ./cluc_total_bytes.sh

APPLY_DELAY_SCRIPT = ./apply_delay.sh

chmod:
	chmod +x ${CLUC_AVG_LATENCY_SCRIPT}
	chmod +x ${CLUC_TOTAL_BYTES_SCRIPT}

sleep:
	sleep 2

apply_delay:
	chmod +x ${APPLY_DELAY_SCRIPT}
	sudo ${APPLY_DELAY_SCRIPT}


publish:
	chmod +x ./publish.sh
	./publish.sh

capture/broker:
	chmod +x ./broker/capture.sh
	./broker/capture.sh

collect_pcks/subscriber:
	$(TSHARK_R) $(SUB_FILE) $(TSHARK_COLLECT_OPTIONS)
collect_pcks/publisher:
	$(TSHARK_R) $(PUB_FILE) $(TSHARK_COLLECT_OPTIONS)

show_pcks/subscriber:
	$(TSHARK_R) $(SUB_FILE) $(TSHARK_SHOW_OPTIONS)
show_pcks/subscriber/debug:
	$(TSHARK_R) $(SUB_DEBUG_FILE) $(TSHARK_SHOW_OPTIONS)
show_pcks/publisher:
	$(TSHARK_R) $(PUB_FILE) $(TSHARK_SHOW_OPTIONS)
show_pcks/broker:
	$(TSHARK_R) $(BROKER_FILE) $(TSHARK_SHOW_OPTIONS)

cluc_avg_latency:
	$(CLUC_AVG_LATENCY_SCRIPT)
cluc_total_bytes/subscriber:
	$(CLUC_TOTAL_BYTES_SCRIPT) $(SUB_CAP_DIR)
cluc_total_bytes/publisher:
	$(CLUC_TOTAL_BYTES_SCRIPT) $(PUB_CAP_DIR)

run/with_cloud:
	set -e; \
	$(MAKE) apply_delay; \
	$(MAKE) sleep; \
	$(MAKE) publish; \
	$(MAKE) chmod; \
	$(MAKE) sleep; \
	$(MAKE) stop/with_cloud; \
	$(MAKE) cluc_avg_latency; \
	$(MAKE) cluc_total_bytes/subscriber; \
	$(MAKE) cluc_total_bytes/publisher; \
	echo "Run with cloud completed."

# Debugging
send_tcp:
	set -e; \
	$(MAKE) apply_delay; \
	$(MAKE) sleep; \
	$(DOCKER_EXEC_SUB) bash receive_tcp.sh & \
	$(MAKE) sleep; \
	$(DOCKER_EXEC_PUB) bash send_tcp.sh

# Docker Compose
up:
	$(DOCKER_COMPOSE_UP)
up/with_cloud:
	$(DOCKER_COMPOSE_UP_WITH_CLOUD)

up/build:
	$(DOCKER_COMPOSE_UP) --build
up/build/with_cloud:
	$(DOCKER_COMPOSE_UP_WITH_CLOUD) --build

stop:
	$(DOCKER_COMPOSE) stop
stop/with_cloud:
	$(DOCKER_COMPOSE_WITH_CLOUD) stop

down:
	$(DOCKER_COMPOSE) down
down/with_cloud:
	$(DOCKER_COMPOSE_WITH_CLOUD) down