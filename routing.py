import json
from pathlib import Path

from message_schema import Message, make_message

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

ROUTES = {"executor": "executor_queue", "reviewer": "reviewer_queue"}

def route_message(message: Message) -> str:
    if message.recipient not in ROUTES:
        raise ValueError("unknown recipient")

    return ROUTES[message.recipient]

if __name__ == "__main__":
    trace = []

    try:
        message = make_message("planner", "executor", "task", {"action": "lookup"})

        destination = route_message(message)

        trace.append({
                "status": "routed",
                "recipient": message.recipient,
                "destination": destination,
                "correlation_id": message.correlation_id,
            })

    except ValueError as error:
        trace.append({"status": "failed", "error": str(error)})

    try:
        invalid_message = make_message("planner", "unknown_agent", "task", {"action": "lookup"})

        route_message(invalid_message)

    except ValueError as error:
        trace.append({"status": "rejected", "error": str(error)})

    output = json.dumps(trace, indent=2)

    print(output)

    (OUTPUT_DIR / "routing.txt").write_text(output, encoding="utf-8")