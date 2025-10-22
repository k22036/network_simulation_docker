#!/bin/bash
set -e

# python
# python send_tcp.py

# nc
( for i in $(seq 1 5); do printf "Hello from client! Message %d\n" "$i"; sleep 1; done ) | nc 172.28.1.2 5000
