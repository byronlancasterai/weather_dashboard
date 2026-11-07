#!/bin/bash
cd /config/byron/projects/weather_dashboard
nohup python3 main.py >> dashboard.log 2>&1 &
echo $! > dashboard.pid
