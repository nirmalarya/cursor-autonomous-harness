#!/bin/bash
#
# Monitor Cursor Agent Progress
# ==============================
#
# Run this in a separate terminal while cursor_autonomous_agent.py is running
# to see real-time progress.

PROJECT_DIR="${1:-./test_app}"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Project directory not found: $PROJECT_DIR"
    echo "Usage: $0 [project_dir]"
    exit 1
fi

echo "==================================================================="
echo "  Monitoring: $PROJECT_DIR"
echo "==================================================================="
echo ""
echo "Press Ctrl+C to stop monitoring"
echo ""

while true; do
    clear
    echo "==================================================================="
    echo "  CURSOR AGENT PROGRESS MONITOR"
    echo "==================================================================="
    echo ""
    echo "Time: $(date '+%H:%M:%S')"
    echo ""
    
    # Check if cursor agent is running
    if pgrep -f "cursor agent" > /dev/null; then
        echo "✅ Cursor agent process: RUNNING"
    else
        echo "⚠️  Cursor agent process: NOT RUNNING"
    fi
    echo ""
    
    echo "-------------------------------------------------------------------"
    echo "  Files in Project"
    echo "-------------------------------------------------------------------"
    ls -lhrt "$PROJECT_DIR/" 2>/dev/null | tail -15
    echo ""
    
    echo "-------------------------------------------------------------------"
    echo "  Feature Progress"
    echo "-------------------------------------------------------------------"
    if [ -f "$PROJECT_DIR/feature_list.json" ]; then
        TOTAL=$(cat "$PROJECT_DIR/feature_list.json" | grep -c '"id":' || echo "0")
        PASSING=$(cat "$PROJECT_DIR/feature_list.json" | grep -c '"status": "passing"' || echo "0")
        PENDING=$(cat "$PROJECT_DIR/feature_list.json" | grep -c '"status": "pending"' || echo "0")
        
        echo "Total features: $TOTAL"
        echo "Passing: $PASSING"
        echo "Pending: $PENDING"
        
        if [ "$TOTAL" -gt 0 ]; then
            PERCENT=$((PASSING * 100 / TOTAL))
            echo "Progress: $PERCENT%"
            
            # Progress bar
            BAR_WIDTH=50
            FILLED=$((PERCENT * BAR_WIDTH / 100))
            printf "["
            for ((i=0; i<FILLED; i++)); do printf "="; done
            for ((i=FILLED; i<BAR_WIDTH; i++)); do printf " "; done
            printf "] $PERCENT%%\n"
        fi
    else
        echo "feature_list.json not found yet"
    fi
    echo ""
    
    echo "-------------------------------------------------------------------"
    echo "  Recent Git Activity"
    echo "-------------------------------------------------------------------"
    if [ -d "$PROJECT_DIR/.git" ]; then
        cd "$PROJECT_DIR" && git log --oneline -5 2>/dev/null || echo "No commits yet"
        cd - > /dev/null
    else
        echo "Git not initialized yet"
    fi
    echo ""
    
    echo "-------------------------------------------------------------------"
    echo "  Latest Progress Notes"
    echo "-------------------------------------------------------------------"
    if [ -f "$PROJECT_DIR/cursor-progress.txt" ]; then
        tail -10 "$PROJECT_DIR/cursor-progress.txt"
    else
        echo "cursor-progress.txt not found yet"
    fi
    echo ""
    
    echo "==================================================================="
    echo "  Refreshing in 5 seconds... (Ctrl+C to stop)"
    echo "==================================================================="
    
    sleep 5
done



