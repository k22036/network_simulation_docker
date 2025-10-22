#!/bin/bash
set -euo pipefail

# ---- Configuration ----
BASE_CONTAINER_NAME="mqtt_publisher_"
NUM_PUBLISHERS=50

# ---- Main Script ----
for i in $(seq 1 $NUM_PUBLISHERS); do
    CONTAINER_NAME="${BASE_CONTAINER_NAME}${i}"
    echo "Publishing messages from container: ${CONTAINER_NAME}"
    docker exec -i "${CONTAINER_NAME}" bash publish.sh &
done
wait