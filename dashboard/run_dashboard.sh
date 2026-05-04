#!/bin/bash
# Linux launcher for HIV Spatial Epidemiology Dashboard

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# URL for the dashboard
DASHBOARD_URL="http://127.0.0.1:8050"

# Open browser and start server
echo "Starting HIV Spatial Epidemiology Dashboard..."
echo "Opening browser at $DASHBOARD_URL"

# Try to open the URL in default browser
if command -v xdg-open &> /dev/null; then
    xdg-open "$DASHBOARD_URL" 2>/dev/null &
elif command -v gnome-open &> /dev/null; then
    gnome-open "$DASHBOARD_URL" 2>/dev/null &
elif command -v kde-open &> /dev/null; then
    kde-open "$DASHBOARD_URL" 2>/dev/null &
else
    echo "Could not open browser. Please navigate to $DASHBOARD_URL manually."
fi

# Wait a moment for browser to start, then launch Python server
sleep 2

# Start the Dash app
python3 app.py
