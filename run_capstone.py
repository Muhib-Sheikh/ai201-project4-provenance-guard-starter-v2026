import argparse
import json
import statistics
import time
import uuid
from pathlib import Path

import requests


URL = "http://127.0.0.1:5000/submit"
LOG_FILE = Path("logs/capstone_requests.jsonl")
RESULTS_DIR = Path("results")

CASES = {
    "punctuation": "!!!!!!!!!!!!!",
    "emoji_only": "😂😂😂😂😂😂😂😂",
    "numbers_only": "123456789012345",
    "control_characters": "Hello\x00this is a test.",
    "repetitive_characters": "a" * 200,
    "repetitive_words": "hello " * 80,
    "empty": "",
    "whitespace": "   ",
    "valid_plain": (
        "I went to the library after class today. "
        "It was quiet, so I finished my homework."
    ),
    "valid_emoji": ("I finally finished my project today! I'm glad it's over 😂"),
    "valid_multiline": ("Today was a busy day.\nI had two classes and a meeting."),
}


def submit_case(name, text, trial):
    payload = {
        "text": text,
        "creator_id": f"capstone_{uuid.uuid4().hex}",
    }

    start = time.perf_counter()

    response = requests.post(URL, json=payload, timeout=120)

    elapsed_ms = (time.perf_counter() - start) * 1000

    try:
        output = response.json()
    except ValueError:
        output = response.text

    return {
        "trial": trial,
        "case": name,
        "input": payload,
        "status_code": response.status_code,
        "output": output,
        "request_id": response.headers.get("X-Request-ID"),
        "client_duration_ms": round(elapsed_ms, 3),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--label",
        required=True,
        choices=["before", "after", "cost"],
    )
    args = parser.parse_args()

    # Warm up the model before measured runs.
    warmup = submit_case("warmup", CASES["valid_plain"], 0)

    if warmup["status_code"] != 200:
        raise RuntimeError(f"Warmup failed: {warmup}")

    rows = []

    if args.label == "cost":
        valid_cases = [
            (name, text) for name, text in CASES.items() if name.startswith("valid_")
        ]

        for i in range(10):
            name, text = valid_cases[i % len(valid_cases)]
            rows.append(submit_case(name, text, i + 1))

    else:
        for trial in range(1, 4):
            for name, text in CASES.items():
                rows.append(submit_case(name, text, trial))

    entries = {}

    if LOG_FILE.exists():
        for line in LOG_FILE.read_text().splitlines():
            entry = json.loads(line)
            entries[entry["request_id"]] = entry

    for row in rows:
        row["log"] = entries.get(row["request_id"])

        print(
            f"Trial {row['trial']} | "
            f"{row['case']} | "
            f"HTTP {row['status_code']} | "
            f"{row['client_duration_ms']} ms"
        )

    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / f"capstone_{args.label}.json"

    path.write_text(json.dumps(rows, indent=2))

    print(f"\nResults saved to {path}")

    if args.label == "cost":
        costs = [
            row["log"]["cpu_seconds"]
            for row in rows
            if row["status_code"] == 200 and row["log"]
        ]

        if len(costs) == 10:
            average = statistics.mean(costs)
            print(f"Average CPU seconds: {average:.6f}")
            print(f"100 runs: {average * 100:.6f} CPU seconds")
        else:
            print("Cost measurement incomplete.")


if __name__ == "__main__":
    main()
