#!/bin/bash

echo ""
echo "=== entry point ==="
echo "Pass 'start' to start production code"
# echo "Pass 'start' '<service>' to start specific Granola2 Core Services"
echo ""

if [ -z "$1" ]; then
    echo "Not enough arguments passed";
    exit 0
elif [ $1 == "start" ]; then
    # This is were you'd actually run your production ready code.
    sleep 99999999;
elif [ $1 == "hold" ]; then
    sleep 99999999;
else
    echo "Argument not recognized";
fi
