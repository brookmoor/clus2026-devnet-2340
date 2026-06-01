#!/bin/bash
# Create a UDP output destination on the CTB Broker

CTB_MANAGER="${CTB_MANAGER_IP:-10.0.54.30}"
CTB_USER="${CTB_USERNAME:-admin}"
CTB_PASS="${CTB_PASSWORD:-changeme}"
DEST_IP="${DEST_IP:-10.0.54.110}"

echo "Creating UDP output -> ${DEST_IP}:4740..."
echo ""

curl -sk -u ${CTB_USER}:${CTB_PASS} -X POST \
  https://${CTB_MANAGER}/api-v1/outputs/ \
  -H 'Content-Type: application/json' \
  -d "{
    \"name\": \"API Demo Collector\",
    \"node\": 2,
    \"output_type\": \"udp\",
    \"address\": \"${DEST_IP}\",
    \"port\": 4740,
    \"dcd_enabled\": false
  }" | python3 -m json.tool

echo ""
echo "Done - output will forward telemetry to ${DEST_IP}:4740"
