#!/bin/sh
set -e

# Bridge name を自動取得
BRIDGE_IF=$(ip -o link show | awk -F': ' '/br-/{print $2; exit}')

echo "Disabling bridge forwarding shortcut with ebtables..."
ebtables -t broute -A BROUTING -p IPv4 -j RETURN

echo "Configuring traffic control on bridge interface: ${BRIDGE_IF}"
tc qdisc replace dev $BRIDGE_IF root netem delay 20ms