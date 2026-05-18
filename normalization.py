# =========================================================
# CPU EVENT NORMALIZATION
# =========================================================

def normalize_sched_events(raw_events):

    normalized_events = []

    for event in raw_events:

        normalized_event = {
            "timestamp": event["ts"],
            "duration_ms": event["dur"] / 1_000_000,
            "event_type": "CPU_SCHED",
            "cpu_core": event["cpu"],
            "thread_id": event["utid"],
            "binder_name": None
        }

        normalized_events.append(normalized_event)

    return normalized_events


# =========================================================
# BINDER EVENT NORMALIZATION
# =========================================================

def normalize_binder_events(raw_events):

    normalized_events = []

    for event in raw_events:

        normalized_event = {
            "timestamp": event["ts"],
            "duration_ms": event["dur"] / 1_000_000,
            "event_type": "BINDER_CALL",
            "cpu_core": None,
            "thread_id": None,
            "binder_name": event["name"]
        }

        normalized_events.append(normalized_event)

    return normalized_events


# =========================================================
# FRAME EVENT NORMALIZATION
# =========================================================

def normalize_frame_events(raw_events):

    normalized_events = []

    for event in raw_events:

        normalized_event = {
            "timestamp": event["ts"],
            "duration_ms": event["dur"] / 1_000_000,
            "event_type": "FRAME_RENDER",
            "cpu_core": None,
            "thread_id": None,
            "binder_name": event["name"]
        }

        normalized_events.append(normalized_event)

    return normalized_events