#!/bin/bash
echo "🚀 Starting SmartThings-like TV Control Interface..."
echo "=================================================="
echo "TV IP: 192.168.23.25"
echo "Token: 78091086"
echo ""
echo "Point your browser to:"
echo "  http://localhost:8080"
echo "  http://192.168.23.20:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="

python3 /workspace/rccli_bridge.py