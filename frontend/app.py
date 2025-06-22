from flask import Flask, render_template
import requests
import os
from prometheus_client import Counter, generate_latest, Histogram, CONTENT_TYPE_LATEST, start_http_server

app = Flask(__name__)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5001')

REQUEST_COUNT = Counter('request_count', 'Total number of requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

start_http_server(8000) 

@app.route('/')
def index():
    try:
        REQUEST_COUNT.inc()  # Increment request counter
        with REQUEST_LATENCY.time():  # Measure latency
            response = requests.get(f'{BACKEND_URL}/data')
            data = response.json()
            return render_template('index.html', message=data.get('message', 'No data'))
    except Exception as e:
        return render_template('index.html', message=f'Error: {str(e)}')

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)