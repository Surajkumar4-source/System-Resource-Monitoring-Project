from flask import Flask, render_template
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

app = Flask(__name__)

def generate_pie_charts():
    log_file = '/var/log/monitoring_project/resource_monitor.log'
    
    # Parse the log file
    data = {
        'cpu_usage': [],
        'memory_usage': [],
        'disk_usage': []
    }
    logs_to_display = []

    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(minutes=10)  # Change to 10 minutes
            
            for line in file:
                parts = line.split(': ')
                if len(parts) > 1:
                    # Parse the timestamp
                    timestamp_str = parts[0]
                    log_time = datetime.strptime(timestamp_str, '%A %d %B %Y %I:%M:%S %p IST')

                    # Check if the log entry is within the last 10 minutes
                    if log_time >= cutoff_time:
                        logs_to_display.append(line)
                        usage_info = parts[1].split(',')
                        if len(usage_info) == 3:
                            cpu = float(usage_info[0].split(' ')[-1][:-1])  # CPU usage without the %
                            memory = float(usage_info[1].split(' ')[-1][:-1])  # Memory usage without the %
                            disk = float(usage_info[2].split(' ')[-1][:-1].replace('%', ''))  # Disk usage
                            data['cpu_usage'].append(cpu)
                            data['memory_usage'].append(memory)
                            data['disk_usage'].append(disk)

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Function to create pie charts and return as base64 string
        def plot_pie_chart(usage, title):
            plt.figure(figsize=(4, 4))
            plt.pie(usage, labels=['Used', 'Remaining'], autopct='%1.1f%%', startangle=90)
            plt.title(title)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            return base64.b64encode(img.getvalue()).decode('utf-8')

        # Generate pie charts
        cpu_used = df['cpu_usage'].iloc[-1] if not df['cpu_usage'].empty else 0
        cpu_remaining = 100 - cpu_used

        memory_used = df['memory_usage'].iloc[-1] if not df['memory_usage'].empty else 0
        memory_remaining = 100 - memory_used

        disk_used = df['disk_usage'].iloc[-1] if not df['disk_usage'].empty else 0
        disk_remaining = 100 - disk_used

        cpu_chart = plot_pie_chart([cpu_used, cpu_remaining], 'CPU Usage')
        memory_chart = plot_pie_chart([memory_used, memory_remaining], 'Memory Usage')
        disk_chart = plot_pie_chart([disk_used, disk_remaining], 'Disk Usage')

        return cpu_chart, memory_chart, disk_chart, logs_to_display
    else:
        return None, None, None, []

@app.route('/')
def index():
    # Generate pie charts
    cpu_chart, memory_chart, disk_chart, logs = generate_pie_charts()

    return render_template('index.html', logs=logs, cpu_chart=cpu_chart, memory_chart=memory_chart, disk_chart=disk_chart)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
