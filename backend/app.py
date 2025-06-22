from flask import Flask, jsonify
import os
import psutil
from prometheus_client import Counter, Gauge, generate_latest, Histogram, CONTENT_TYPE_LATEST, start_http_server

app = Flask(__name__)

REQUEST_COUNT = Counter('request_count', 'Total number of requests')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU Usage Percentage')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory Usage Percentage')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

start_http_server(8000)

@app.route('/data')
def get_data():
    REQUEST_COUNT.inc()  
    with REQUEST_LATENCY.time():  
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        CPU_USAGE.set(cpu_usage) 
        MEMORY_USAGE.set(memory_usage) 
        return jsonify({
            'message': 'Backend is running!',
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage
        })

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)