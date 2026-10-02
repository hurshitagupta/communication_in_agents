import json
from dataclasses import dataclass, asdict
from pathlib import Path
from uuid import uuid4

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

@dataclass
class Message:
    kind: str
    sender: str
    recipient: str
    payload: dict
    correlation_id: str

def make_message(sender: str, recipient: str, kind: str, payload: dict) -> Message:
    if not sender:
        raise ValueError("sender is required")

    if not recipient:
        raise ValueError("recipient is required")

    if kind not in {"task", "result", "ack"}:
        raise ValueError("unsupported message kind")

    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary")

    return Message(kind=kind,
        sender=sender,
        recipient=recipient,
        payload=payload,
        correlation_id=str(uuid4()))

if __name__ == "__main__":
    trace = []

    try:
        message = make_message("planner", "executor", "task", {"action": "lookup"})

        trace.append({"status": "success", "message": asdict(message)})

    except ValueError as error:
        trace.append({"status": "failed", "error": str(error)})

    try:
        make_message("planner", "executor", "invalid", {"action": "lookup"})

    except ValueError as error:
        trace.append({"status": "rejected", "error": str(error)})

    output = json.dumps(trace, indent=2)
    print(output)

    (OUTPUT_DIR / "message_schema.txt").write_text(output, encoding="utf-8")