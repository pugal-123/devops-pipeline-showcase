from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# ── Prometheus Metrics ──────────────────────────────────────────
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['endpoint']
)
ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)
APP_INFO = Gauge(
    'app_info',
    'Application info',
    ['version', 'environment']
)

# Set app info
APP_INFO.labels(version='1.0.0', environment='production').set(1)


@app.before_request
def start_timer():
    from flask import g
    g.start = time.time()


@app.after_request
def record_metrics(response):
    from flask import g, request
    latency = time.time() - g.start
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    return response


# ── Routes ──────────────────────────────────────────────────────
@app.route('/')
def home():
    return jsonify({
        "app": "DevOps Showcase API",
        "version": "1.0.0",
        "status": "running",
        "message": "End-to-end DevOps pipeline by Pugazhenthi Muthu"
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": "ok"}), 200


@app.route('/readyz')
def readyz():
    return jsonify({"status": "ready"}), 200


@app.route('/api/stats')
def stats():
    # Simulate active users metric
    users = random.randint(10, 100)
    ACTIVE_USERS.set(users)
    return jsonify({
        "active_users": users,
        "requests_served": "see /metrics for full stats"
    })


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
