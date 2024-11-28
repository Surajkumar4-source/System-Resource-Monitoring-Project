#!/bin/bash

# Thresholds
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
DISK_THRESHOLD=90

# Log file
LOG_FILE="/var/log/monitoring_project/resource_monitor.log"

# Function to log resource usage
log_resources() {
    # Get current resource usage
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    MEMORY_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    DISK_USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')

    # Log the resource usage
    echo "$(date): CPU usage is at ${CPU_USAGE}%, Memory usage is at ${MEMORY_USAGE}%, Disk usage is at ${DISK_USAGE}%" >> $LOG_FILE

    # Check thresholds and log alerts
    if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
        echo "$(date): CPU usage is at ${CPU_USAGE}%" >> $LOG_FILE
    fi

    if (( $(echo "$MEMORY_USAGE > $MEMORY_THRESHOLD" | bc -l) )); then
        echo "$(date): Memory usage is at ${MEMORY_USAGE}%" >> $LOG_FILE
    fi

    if (( DISK_USAGE > DISK_THRESHOLD )); then
        echo "$(date): Disk usage is at ${DISK_USAGE}%" >> $LOG_FILE
    fi

    # Remove logs older than 24 hours
    find $LOG_FILE -mtime +1 -exec rm {} \;
}

# Function to display logs from the last 10 minutes
display_recent_logs() {
    echo "Displaying logs from the last 10 minutes:"
    awk -vDate="$(date --date='10 minutes ago' '+%Y-%m-%d %H:%M:%S')" '$0 >= Date' $LOG_FILE
}

# Main script logic
if [[ "$1" == "display" ]]; then
    display_recent_logs
else
    log_resources
fi
