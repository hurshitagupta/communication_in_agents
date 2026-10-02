import json
from pathlib import Path

from message_schema import Message, make_message

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def create_acknowledgement(message: Message) -> Message:
    if message.kind == "ack":
        raise ValueError("cannot acknowledge an acknowledgement")

    return make_message(sender=message.recipient, recipient=message.sender, kind="ack",
        payload={"status": "received", "correlation_id": message.correlation_id,})

if __name__ == "__main__":
    trace = []

    try:
        task_message = make_message("planner", "executor", "task", {"action": "lookup"})

        ack = create_acknowledgement(task_message)

        trace.append({
                "status": "acknowledged",
                "sender": ack.sender,
                "recipient": ack.recipient,
                "kind": ack.kind,
                "payload": ack.payload,
            })

    except ValueError as error:
        trace.append({"status": "failed", "error": str(error)})

    try:
        existing_ack = make_message("executor", "planner", "ack", {"status": "received"})

        create_acknowledgement(existing_ack)

    except ValueError as error:
        trace.append({"status": "rejected", "error": str(error)})

    output = json.dumps(trace, indent=2)

    print(output)

    (OUTPUT_DIR / "acknowledgement.txt").write_text(output, encoding="utf-8")