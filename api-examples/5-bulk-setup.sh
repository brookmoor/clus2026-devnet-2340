#!/bin/bash
# Bulk API setup: 10 inputs, 10 outputs, 9 subscriptions
# Deliberately skips subscription for port 3005 -> 5005
# (used in the MCP demo to show AI-driven gap detection)

CTB_MANAGER="${CTB_MANAGER_IP:-10.0.54.30}"
CTB_USER="${CTB_USERNAME:-admin}"
CTB_PASS="${CTB_PASSWORD:-changeme}"
NODE_ID=2
DEST_IP="${DEST_IP:-10.0.54.110}"

AUTH="-u ${CTB_USER}:${CTB_PASS}"
API="https://${CTB_MANAGER}/api-v1"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  CTB Bulk API Demo                                          ║"
echo "║  Creating 10 inputs, 10 outputs, 9 subscriptions...        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

declare -a INPUT_IDS
declare -a OUTPUT_IDS

# Create 10 Inputs (ports 3001-3010)
echo "Creating 10 inputs (ports 3001-3010)..."
for i in $(seq 1 10); do
  PORT=$((3000 + i))
  RESULT=$(curl -sk $AUTH -X POST "${API}/inputs/" \
    -H 'Content-Type: application/json' \
    -d "{\"name\": \"Sensor-${i} [port ${PORT}]\", \"node\": ${NODE_ID}, \"input_type\": \"udp_listener\", \"port\": ${PORT}, \"track_exporter_disabled\": false}" 2>/dev/null)
  ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','ERR'))" 2>/dev/null)
  INPUT_IDS+=("$ID")
  echo "  + Input ${i}: port ${PORT} (id=${ID})"
done

echo ""

# Create 10 Outputs (-> DEST_IP ports 5001-5010)
echo "Creating 10 outputs (-> ${DEST_IP} ports 5001-5010)..."
for i in $(seq 1 10); do
  PORT=$((5000 + i))
  RESULT=$(curl -sk $AUTH -X POST "${API}/outputs/" \
    -H 'Content-Type: application/json' \
    -d "{\"name\": \"Collector-${i} [${DEST_IP}:${PORT}]\", \"node\": ${NODE_ID}, \"output_type\": \"udp\", \"address\": \"${DEST_IP}\", \"port\": ${PORT}, \"dcd_enabled\": false}" 2>/dev/null)
  ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','ERR'))" 2>/dev/null)
  OUTPUT_IDS+=("$ID")
  echo "  + Output ${i}: ${DEST_IP}:${PORT} (id=${ID})"
done

echo ""

# Create 9 Subscriptions (skip #5 for MCP demo)
echo "Creating 9 subscriptions (skipping Sensor-5 -> Collector-5)..."
for i in $(seq 0 9); do
  SEQ=$((i + 1))
  if [ $SEQ -eq 5 ]; then
    echo "  ~ Skipping subscription for Sensor-5 (port 3005)"
    continue
  fi
  INPUT_ID="${INPUT_IDS[$i]}"
  OUTPUT_ID="${OUTPUT_IDS[$i]}"
  RESULT=$(curl -sk $AUTH -X POST "${API}/subscriptions/" \
    -H 'Content-Type: application/json' \
    -d "{\"source\": ${INPUT_ID}, \"destination\": ${OUTPUT_ID}, \"subnets\": []}" 2>/dev/null)
  SUB_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','ERR'))" 2>/dev/null)
  echo "  + Subscription: Sensor-${SEQ} -> Collector-${SEQ} (id=${SUB_ID})"
done

echo ""
echo "Done! 10 inputs + 10 outputs + 9 subscriptions created."
echo ""
echo "  NOTE: Sensor-5 (port 3005) has NO subscription."
echo "  The MCP-connected AI can discover and fix this gap."
echo ""
