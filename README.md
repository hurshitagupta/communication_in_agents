# Topic 16 — Implement Communication

## Overview

This project implements the core communication behaviors required in the hands-on assessment.

The implementation focuses on:

- Message schema
- Message routing
- Acknowledgements
- Dead-letter handling
- Correlation tracing

Communication rules are implemented deterministically because routing, acknowledgement, retries, and tracing should behave predictably.

## Project Structure

```text
implement_communication/
│
├── message_schema.py
├── routing.py
├── acknowledgement.py
├── dead_letter.py
├── correlation_trace.py
│
├── tests/
│   ├── test_message_schema.py
│   ├── test_routing.py
│   ├── test_acknowledgement.py
│   ├── test_dead_letter.py
│   └── test_correlation_trace.py
│
├── outputs/
│   ├── message_schema.txt
│   ├── routing.txt
│   ├── acknowledgement.txt
│   ├── dead_letter.txt
│   └── correlation_trace.txt
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Task 1 — Message Schema

Implemented a basic message contract containing:

- Message kind
- Sender
- Recipient
- Payload
- Correlation ID

The implementation validates required fields and rejects unsupported message types.

### Run

```bash
python message_schema.py
```

### Test

```bash
pytest tests/test_message_schema.py -v
```

### Evidence

```text
outputs/message_schema.txt
```

---

## Task 2 — Routing

Implemented recipient-based routing.

Known recipients are mapped to their corresponding queues.

Example:

```text
executor → executor_queue
reviewer → reviewer_queue
```

Unknown recipients are rejected.

### Run

```bash
python routing.py
```

### Test

```bash
pytest tests/test_routing.py -v
```

### Evidence

```text
outputs/routing.txt
```

---

## Task 3 — Acknowledgement

Implemented acknowledgement messages for successfully received communication.

When a task message is received:

- Sender and recipient are reversed.
- Message type becomes `ack`.
- A received status is returned.
- The original correlation ID is included for traceability.

Acknowledgement messages cannot acknowledge another acknowledgement.

### Run

```bash
python acknowledgement.py
```

### Test

```bash
pytest tests/test_acknowledgement.py -v
```

### Evidence

```text
outputs/acknowledgement.txt
```

---

## Task 4 — Dead Letter

Implemented a dead-letter mechanism for messages that cannot be delivered.

The implementation includes:

- Maximum delivery attempts
- Failure recording
- Dead-letter storage
- Correlation ID preservation
- Required failure reason validation

The retry loop is capped using `MAX_ATTEMPTS` to prevent unlimited retries.

### Run

```bash
python dead_letter.py
```

### Test

```bash
pytest tests/test_dead_letter.py -v
```

### Evidence

```text
outputs/dead_letter.txt
```

---

## Task 5 — Correlation Trace

Implemented message-flow tracing using correlation and causation IDs.

The trace demonstrates the flow:

```text
task_sent
    ↓
result_returned
    ↓
acknowledged
```

The same correlation ID is used throughout the flow.

The causation ID identifies which previous event caused the next event.

The implementation also includes a maximum trace-step limit.

### Run

```bash
python correlation_trace.py
```

### Test

```bash
pytest tests/test_correlation_trace.py -v
```

### Evidence

```text
outputs/correlation_trace.txt
```

---

## Run All Tests

```bash
pytest tests/ -v
```

## Requirements

Install the required package:

```bash
pip install pytest
```

Or use:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
pytest
```

## Guardrails

The project includes relevant guardrails such as:

- Input validation
- Route validation
- Rejection of unsupported messages
- Retry limits
- Trace step limits
- Dead-letter handling
- Correlation tracking
- No hardcoded secrets

Timeout handling was not added where there are no external network or API calls that can hang.

## LLM Usage

No LLM calls were required for this assessment.

The communication features implemented here are protocol-level behaviors such as schema validation, routing, acknowledgements, retries, dead-letter handling, and tracing. These should remain deterministic and predictable.

## Outputs

Each task saves observable evidence inside the `outputs/` directory.

This provides traceable proof of:

- Successful execution
- Rejection or failure behavior
- Routing decisions
- Delivery retries
- Dead-letter creation
- Correlation and causation tracing