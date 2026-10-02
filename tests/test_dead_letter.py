import pytest

from dead_letter import DEAD_LETTERS, MAX_ATTEMPTS, add_to_dead_letter
from message_schema import make_message

def test_message_is_added_to_dead_letter():
    DEAD_LETTERS.clear()

    message = make_message("planner", "unknown_agent", "task", {"action": "lookup"})

    record = add_to_dead_letter(message, "delivery failed after retries", 2)

    assert record["recipient"] == "unknown_agent"
    assert record["attempts"] == 2
    assert len(DEAD_LETTERS) == 1


def test_correlation_id_is_preserved():
    message = make_message("planner", "unknown_agent", "task", {"action": "lookup"})

    record = add_to_dead_letter(message, "routing failed", 2)

    assert record["correlation_id"] == message.correlation_id

def test_reason_is_required():
    message = make_message("planner", "executor", "task", {"action": "lookup"})

    with pytest.raises(ValueError, match="dead letter reason is required"):
        add_to_dead_letter(message, "", 1)

def test_attempt_limit_is_enforced():
    message = make_message("planner", "executor", "task", {"action": "lookup"})

    with pytest.raises( ValueError, match="attempt limit exceeded"):
        add_to_dead_letter(message, "delivery failed", MAX_ATTEMPTS + 1)