#!/bin/bash
# macOS launcher for HIV Spatial Epidemiology Dashboard

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# URL for the dashboard
DASHBOARD_URL="http://127.0.0.1:8050"

# Open browser and start server
echo "Starting HIV Spatial Epidemiology Dashboard..."
echo "Opening browser at $DASHBOARD_URL"

# Open the URL in default browser
open "$DASHBOARD_URL" 2>/dev/null || echo "Could not open browser. Please navigate to $DASHBOARD_URL manually."

# Wait a moment for browser to start, then launch Python server
sleep 2

# Start the Dash app
python3 app.py
