import json
from pathlib import Path
from uuid import uuid4

from message_schema import make_message

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_TRACE_STEPS = 5

def add_trace(trace: list, event: str, correlation_id: str, causation_id: str | None = None) -> str:

    if not correlation_id:
        raise ValueError("correlation id is required")

    if len(trace) >= MAX_TRACE_STEPS:
        raise ValueError("trace step limit reached")

    event_id = str(uuid4())

    trace.append({
            "event_id": event_id,
            "event": event,
            "correlation_id": correlation_id,
            "causation_id": causation_id,
        })

    return event_id

if __name__ == "__main__":
    trace = []
    task_message = make_message("planner", "executor", "task", {"action": "lookup"})

    task_event_id = add_trace(trace, event="task_sent", correlation_id=task_message.correlation_id)

    result_event_id = add_trace(trace, event="result_returned", correlation_id=task_message.correlation_id, causation_id=task_event_id)

    add_trace(trace, event="acknowledged", correlation_id=task_message.correlation_id, causation_id=result_event_id)

    try:
        add_trace(trace, event="invalid_event", correlation_id="")

    except ValueError as error:
        trace.append({"event": "trace_rejected", "error": str(error)})

    output = json.dumps(trace, indent=2)

    print(output)

    (OUTPUT_DIR / "correlation_trace.txt").write_text(output, encoding="utf-8")