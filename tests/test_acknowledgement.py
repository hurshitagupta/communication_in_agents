import pytest
from message_schema import make_message
from acknowledgement import create_acknowledgement

def test_acknowledgement_is_created():
    message = make_message( "planner", "executor", "task", {"action": "lookup"})

    ack = create_acknowledgement(message)

    assert ack.kind == "ack"
    assert ack.sender == "executor"
    assert ack.recipient == "planner"
    assert ack.payload["status"] == "received"

def test_ack_contains_original_correlation_id():
    message = make_message( "planner", "executor", "task", {"action": "lookup"})

    ack = create_acknowledgement(message)

    assert ack.payload["correlation_id"] == message.correlation_id


def test_ack_message_cannot_be_acknowledged_again():
    message = make_message("executor", "planner", "ack", {"status": "received"})

    with pytest.raises(ValueError, match="cannot acknowledge an acknowledgement"):
        create_acknowledgement(message)