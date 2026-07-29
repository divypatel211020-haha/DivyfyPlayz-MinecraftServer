#!/bin/bash
# Automatically checks and boots up the Paper server with max memory allocation
echo "Starting Minecraft Crossplay Server..."
while true
do
    java -Xms2G -Xmx3G -XX:+UseG1GC -jar paper.jar nogui
    echo "Server rebooting in 5 seconds... Press CTRL+C to stop."
    sleep 5
done
