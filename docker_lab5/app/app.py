from flask import Flask, Response
from prometheus_client import generate_latest, Counter
import socket

app = Flask(__name__)
REQUEST_COUNT = Counter("app_requests_total", "Total app HTTP requests")

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return f"Hello from container: {socket.gethostname()}\n"

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)