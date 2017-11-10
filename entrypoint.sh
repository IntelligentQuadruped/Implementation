#!/bin/bash

echo ""
echo "=== entry point ==="
echo "Pass 'start' to start production code"
echo ""

if [ -z "$1" ]; then
    echo "Not enough arguments passed";
    exit 0
elif [ $1 == "start" ]; then
    # Add some code here later
    sleep 99999999;
elif [ $1 == "hold" ]; then
    sleep 99999999;
else
    echo "Argument not recognized";
fi