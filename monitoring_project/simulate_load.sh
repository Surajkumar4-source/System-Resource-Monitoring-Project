#!/bin/bash

# Function to simulate CPU load using stress-ng
function cpu_load {
    echo "Simulating CPU load..."
    stress-ng --cpu 8 --timeout 60 &
}

# Function to simulate memory usage using stress-ng
function memory_usage {
    echo "Simulating memory usage..."
    stress-ng --vm 5 --vm-bytes 85% --timeout 60 &
}

# Function to simulate disk usage by creating large files
function disk_usage {
    echo "Simulating disk usage..."
    for i in {1..5}; do
        dd if=/dev/zero of=file$i.bin bs=1M count=100 &
    done
}

# Start the simulations
cpu_load
memory_usage
disk_usage

# Wait for 60 seconds
echo "Simulations running for 60 seconds..."
sleep 60

# Cleanup: remove created files
echo "Cleaning up..."
rm -f file*.bin

echo "Back to normal state."
