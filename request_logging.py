import json
import time
import uuid
from datetime import datetime, timezone

from flask import g, request

import config

LOG_FILE = config.LOG_DIR / "capstone_requests.jsonl"


def init_app(app):

    @app.before_request
    def start_request():
        if request.path not in ("/submit", "/appeal"):
            return

        g.request_id = uuid.uuid4().hex
        g.start_time = time.perf_counter()
        g.start_cpu = time.process_time()
        g.timestamp = datetime.now(timezone.utc).isoformat()
        g.detector_called = False

        body = request.get_data(cache=True, as_text=True)

        g.request_input = body[:1000]
        g.input_truncated = len(body) > 1000

    @app.after_request
    def log_request(response):
        if not hasattr(g, "start_time"):
            return response

        entry = {
            "timestamp": g.timestamp,
            "request_id": g.request_id,
            "endpoint": request.path,
            "input": g.request_input,
            "input_truncated": g.input_truncated,
            "output": response.get_json(silent=True),
            "status_code": response.status_code,
            "duration_ms": round((time.perf_counter() - g.start_time) * 1000, 3),
            "cpu_seconds": round(time.process_time() - g.start_cpu, 6),
            "detector_called": g.detector_called,
        }

        if entry["output"] is None:
            entry["output"] = {"status": response.status}

        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")

        response.headers["X-Request-ID"] = g.request_id

        return response
