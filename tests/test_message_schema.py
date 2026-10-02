import pytest

from message_schema import make_message

def test_valid_message():
    message = make_message("planner", "executor", "task", {"action": "lookup"})

    assert message.kind == "task"
    assert message.sender == "planner"
    assert message.recipient == "executor"
    assert message.correlation_id

def test_invalid_message_kind():
    with pytest.raises(ValueError, match="unsupported message kind"):
        make_message("planner", "executor", "invalid",{"action": "lookup"})