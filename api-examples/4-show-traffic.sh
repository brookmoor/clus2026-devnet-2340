#!/bin/bash
# Show live traffic stats from the API

CTB_MANAGER="${CTB_MANAGER_IP:-10.0.54.30}"
CTB_USER="${CTB_USERNAME:-admin}"
CTB_PASS="${CTB_PASSWORD:-changeme}"

echo "=== Input Stats ==="
curl -sk -u ${CTB_USER}:${CTB_PASS} \
  https://${CTB_MANAGER}/api-v1/inputs/ | \
  python3 -c "
import sys, json
inputs = json.load(sys.stdin)
for i in inputs:
    print(f\"  Name:      {i['name']}\")
    print(f\"  Status:    {i['status']}\")
    m = i.get('metrics', {})
    print(f\"  RX pkts:   {m.get('rx_pkts', 'N/A')}\")
    print(f\"  RX bps:    {m.get('rx_bps', 'N/A')}\")
    print()
"

echo "=== Output Stats ==="
curl -sk -u ${CTB_USER}:${CTB_PASS} \
  https://${CTB_MANAGER}/api-v1/outputs/ | \
  python3 -c "
import sys, json
outputs = json.load(sys.stdin)
for o in outputs:
    print(f\"  Name:      {o['name']}\")
    print(f\"  Status:    {o['status']}\")
    m = o.get('metrics', {})
    print(f\"  TX pkts:   {m.get('tx_pkts', 'N/A')}\")
    print(f\"  TX bps:    {m.get('tx_bps', 'N/A')}\")
    print(f\"  Dropped:   {m.get('dropped_pkts', 0)}\")
    print()
"
