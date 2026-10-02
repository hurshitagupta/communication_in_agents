import json
from pathlib import Path
from message_schema import make_message

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

DEAD_LETTERS = []

MAX_ATTEMPTS = 2

def add_to_dead_letter(message, reason: str, attempts: int) -> dict:
    if not reason:
        raise ValueError("dead letter reason is required")

    if attempts > MAX_ATTEMPTS:
        raise ValueError("attempt limit exceeded")

    record = {
        "recipient": message.recipient,
        "correlation_id": message.correlation_id,
        "reason": reason,
        "attempts": attempts,
    }

    DEAD_LETTERS.append(record)

    return record

if __name__ == "__main__":
    trace = []

    message = make_message("planner", "unknown_agent", "task", {"action": "lookup"})

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        attempts += 1

        trace.append(
            {
                "status": "delivery_failed",
                "attempt": attempts,
                "recipient": message.recipient,
            }
        )

    record = add_to_dead_letter(message, "delivery failed after retries", attempts)

    trace.append({"status": "dead_lettered", "record": record})

    try:
        add_to_dead_letter(message, "", attempts)

    except ValueError as error:
        trace.append({"status": "rejected", "error": str(error)})

    output = json.dumps(trace, indent=2)

    print(output)

    (OUTPUT_DIR / "dead_letter.txt").write_text(output, encoding="utf-8")