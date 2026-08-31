#!/usr/bin/env python3
"""Apply a manual pass/fail review to one droid-sim-12task episode."""

import argparse
from datetime import datetime
import json
from pathlib import Path


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path, help="Timestamped run directory containing manifest.json")
    parser.add_argument("task_id", help="Task identifier, for example task-01")
    parser.add_argument("episode", type=int)
    parser.add_argument("verdict", choices=("pass", "fail"))
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--notes")
    parser.add_argument("--replace", action="store_true", help="Replace an existing review")
    args = parser.parse_args()

    manifest_path = args.run_dir.resolve() / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("protocol_id") != "droid-sim-12task-v1":
        raise SystemExit(f"Not a droid-sim-12task-v1 run: {manifest_path}")

    matches = [
        task
        for task in manifest["tasks"]
        if task["task_id"] == args.task_id and task["episode"] == args.episode
    ]
    if len(matches) != 1:
        raise SystemExit(
            f"Expected one manifest entry for {args.task_id} episode {args.episode}, found {len(matches)}"
        )
    task = matches[0]
    review_path = Path(task["review_file"])
    metrics_path = Path(task["metrics"])
    review = json.loads(review_path.read_text())
    if review.get("status") == "reviewed" and not args.replace:
        raise SystemExit("Episode is already reviewed; pass --replace to change it")

    success = args.verdict == "pass"
    reviewed_at = datetime.now().isoformat()
    review.update(
        {
            "status": "reviewed",
            "verdict": args.verdict,
            "success": success,
            "notes": args.notes,
            "reviewer": args.reviewer,
            "reviewed_at": reviewed_at,
        }
    )
    write_json(review_path, review)

    metrics = json.loads(metrics_path.read_text())
    metrics.update(
        {
            "success": success,
            "failure_reason": None if success else "manual_review_failure",
            "scoring_status": "manually_reviewed",
            "reviewed_at": reviewed_at,
        }
    )
    write_json(metrics_path, metrics)

    task.update(
        {
            "success": success,
            "failure_reason": None if success else "manual_review_failure",
            "review_status": "reviewed",
        }
    )
    reviewed = [entry for entry in manifest["tasks"] if entry["success"] is not None]
    successes = sum(entry["success"] is True for entry in reviewed)
    manifest["summary"] = {
        "episodes": len(manifest["tasks"]),
        "reviewed": len(reviewed),
        "pending_review": len(manifest["tasks"]) - len(reviewed),
        "successes": successes,
        "failures": len(reviewed) - successes,
        "success_rate": successes / len(reviewed) if reviewed else None,
    }
    if len(reviewed) == len(manifest["tasks"]):
        manifest["status"] = "completed_reviewed"
        manifest["scoring_status"] = "manually_reviewed"
    write_json(manifest_path, manifest)
    print(f"Recorded {args.verdict} for {args.task_id} episode {args.episode}")
    print(f"Reviewed {len(reviewed)}/{len(manifest['tasks'])} episodes")


if __name__ == "__main__":
    main()
