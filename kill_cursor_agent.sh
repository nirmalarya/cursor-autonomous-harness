#!/bin/bash
#
# Kill Cursor Agent Processes
# ============================
#
# Use this if cursor agent processes get stuck in the background

echo "==================================================================="
echo "  Searching for cursor agent processes..."
echo "==================================================================="

# Find cursor agent processes
PIDS=$(ps aux | grep "cursor agent" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "✅ No cursor agent processes found"
    exit 0
fi

echo "Found cursor agent processes:"
ps aux | grep "cursor agent" | grep -v grep
echo ""

# Kill each process
for PID in $PIDS; do
    echo "Killing process $PID..."
    kill $PID 2>/dev/null
done

# Wait a bit
sleep 2

# Check if any are still running
REMAINING=$(ps aux | grep "cursor agent" | grep -v grep | awk '{print $2}')

if [ -z "$REMAINING" ]; then
    echo ""
    echo "✅ All cursor agent processes terminated successfully"
else
    echo ""
    echo "⚠️  Some processes still running. Force killing..."
    for PID in $REMAINING; do
        echo "Force killing process $PID..."
        kill -9 $PID 2>/dev/null
    done
    sleep 1
    echo "✅ Done"
fi

echo ""
echo "==================================================================="
echo "  Cleanup complete"
echo "==================================================================="



