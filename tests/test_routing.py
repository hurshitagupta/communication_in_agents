import pytest

from message_schema import make_message
from routing import route_message


def test_route_to_executor():
    message = make_message("planner", "executor", "task", {"action": "lookup"})
    assert route_message(message) == "executor_queue"

def test_route_to_reviewer():
    message = make_message("planner", "reviewer", "task", {"action": "review"})

    assert route_message(message) == "reviewer_queue"

def test_unknown_recipient_is_rejected():
    message = make_message("planner", "unknown_agent", "task", {"action": "lookup"})

    with pytest.raises(ValueError, match="unknown recipient"):
        route_message(message)

def test_empty_recipient_is_rejected():
    with pytest.raises(ValueError, match="recipient is required"):
        make_message("planner", "", "task", {"action": "lookup"})
