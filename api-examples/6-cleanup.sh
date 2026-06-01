#!/bin/bash
# Cleanup: removes all demo objects from CTB Manager

CTB_MANAGER="${CTB_MANAGER_IP:-10.0.54.30}"
CTB_USER="${CTB_USERNAME:-admin}"
CTB_PASS="${CTB_PASSWORD:-changeme}"

AUTH="-u ${CTB_USER}:${CTB_PASS}"
API="https://${CTB_MANAGER}/api-v1"

echo ""
echo "Cleaning up all objects from CTB Manager..."
echo ""

# Delete all subscriptions
echo "Deleting subscriptions..."
SUBS=$(curl -sk $AUTH "${API}/subscriptions/" 2>/dev/null | python3 -c "import sys,json; [print(s['id']) for s in json.load(sys.stdin)]" 2>/dev/null)
for id in $SUBS; do
  curl -sk $AUTH -X DELETE "${API}/subscriptions/${id}/" > /dev/null 2>&1
  echo "  Deleted subscription $id"
done

# Delete all inputs
echo "Deleting inputs..."
INPUTS=$(curl -sk $AUTH "${API}/inputs/" 2>/dev/null | python3 -c "import sys,json; [print(i['id']) for i in json.load(sys.stdin)]" 2>/dev/null)
for id in $INPUTS; do
  curl -sk $AUTH -X DELETE "${API}/inputs/${id}/" > /dev/null 2>&1
  echo "  Deleted input $id"
done

# Delete all outputs
echo "Deleting outputs..."
OUTPUTS=$(curl -sk $AUTH "${API}/outputs/" 2>/dev/null | python3 -c "import sys,json; [print(o['id']) for o in json.load(sys.stdin)]" 2>/dev/null)
for id in $OUTPUTS; do
  curl -sk $AUTH -X DELETE "${API}/outputs/${id}/" > /dev/null 2>&1
  echo "  Deleted output $id"
done

echo ""
echo "Done. CTB Manager is clean."
echo ""
