#!/bin/bash
# Create a UDP input on the CTB Broker (port 2056)

CTB_MANAGER="${CTB_MANAGER_IP:-10.0.54.30}"
CTB_USER="${CTB_USERNAME:-admin}"
CTB_PASS="${CTB_PASSWORD:-changeme}"

echo "Creating IPFIX input on port 2056..."
echo ""

curl -sk -u ${CTB_USER}:${CTB_PASS} -X POST \
  https://${CTB_MANAGER}/api-v1/inputs/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "API Demo IPFIX Input",
    "node": 2,
    "input_type": "udp_listener",
    "port": 2056,
    "track_exporter_disabled": false
  }' | python3 -m json.tool

echo ""
echo "Done - input listening on broker telemetry IP port 2056"
