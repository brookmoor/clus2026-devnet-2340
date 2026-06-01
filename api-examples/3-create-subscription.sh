#!/bin/bash
# Create a subscription linking the input to the output

CTB_MANAGER="${CTB_MANAGER_IP:-10.0.54.30}"
CTB_USER="${CTB_USERNAME:-admin}"
CTB_PASS="${CTB_PASSWORD:-changeme}"

# Get the IDs of the input and output we just created
INPUT_ID=$(curl -sk -u ${CTB_USER}:${CTB_PASS} \
  https://${CTB_MANAGER}/api-v1/inputs/ | \
  python3 -c "import sys,json; inputs=json.load(sys.stdin); print([i['id'] for i in inputs if i['name']=='API Demo IPFIX Input'][0])")

OUTPUT_ID=$(curl -sk -u ${CTB_USER}:${CTB_PASS} \
  https://${CTB_MANAGER}/api-v1/outputs/ | \
  python3 -c "import sys,json; outputs=json.load(sys.stdin); print([o['id'] for o in outputs if o['name']=='API Demo Collector'][0])")

echo "Subscribing input ${INPUT_ID} -> output ${OUTPUT_ID}..."
echo ""

curl -sk -u ${CTB_USER}:${CTB_PASS} -X POST \
  https://${CTB_MANAGER}/api-v1/subscriptions/ \
  -H 'Content-Type: application/json' \
  -d "{
    \"source\": ${INPUT_ID},
    \"destination\": ${OUTPUT_ID},
    \"subnets\": []
  }" | python3 -m json.tool

echo ""
echo "Done - traffic from input is now forwarded to output"
