import pytest

from correlation_trace import MAX_TRACE_STEPS, add_trace

def test_trace_event_is_added():
    trace = []

    event_id = add_trace(trace, "task_sent", "corr-123")

    assert len(trace) == 1
    assert trace[0]["event"] == "task_sent"
    assert trace[0]["correlation_id"] == "corr-123"
    assert event_id

def test_causation_id_is_recorded():
    trace = []

    first_event = add_trace(trace, "task_sent", "corr-123")

    add_trace(trace, "result_returned", "corr-123", causation_id=first_event)

    assert trace[1]["causation_id"] == first_event

def test_same_correlation_id_tracks_flow():
    trace = []

    first_event = add_trace(trace, "task_sent", "corr-123")

    add_trace(trace, "result_returned", "corr-123", first_event)

    assert trace[0]["correlation_id"] == "corr-123"
    assert trace[1]["correlation_id"] == "corr-123"

def test_missing_correlation_id_is_rejected():
    trace = []

    with pytest.raises(ValueError, match="correlation id is required"):
        add_trace(trace, "task_sent", "")

def test_trace_step_limit_is_enforced():
    trace = []

    for i in range(MAX_TRACE_STEPS):
        add_trace(trace, f"event_{i}", "corr-123")

    with pytest.raises(ValueError, match="trace step limit reached"):
        add_trace(trace, "extra_event", "corr-123")