from perfetto.trace_processor import TraceProcessor
from perfetto.trace_processor.api import TraceProcessorConfig

# =========================================================
# PERFETTO CONFIG
# =========================================================

config = TraceProcessorConfig(
    bin_path="./trace_processor_shell.exe"
)

# =========================================================
# GENERIC TRACE PARSER
# =========================================================

def parse_trace(trace_file):

    tp = TraceProcessor(
        trace=trace_file,
        config=config
    )

    print(f"\nTrace Loaded: {trace_file}\n")

    # =====================================================
    # CPU EVENTS
    # =====================================================

    sched_query = """
    SELECT
        ts,
        dur,
        cpu,
        utid
    FROM sched
    LIMIT 20;
    """

    sched_result = tp.query(sched_query)

    cpu_events = []

    for row in sched_result:

        event = {
            "ts": row.ts,
            "dur": row.dur,
            "cpu": row.cpu,
            "utid": row.utid
        }

        cpu_events.append(event)

    # =====================================================
    # BINDER EVENTS
    # =====================================================

    binder_query = """
    SELECT
        ts,
        dur,
        name
    FROM slice
    WHERE name LIKE '%binder%'
    LIMIT 20;
    """

    binder_result = tp.query(binder_query)

    binder_events = []

    for row in binder_result:

        event = {
            "ts": row.ts,
            "dur": row.dur,
            "name": row.name
        }

        binder_events.append(event)

    # =====================================================
    # FRAME EVENTS
    # =====================================================

    frame_query = """
    SELECT
        ts,
        dur,
        name
    FROM slice
    WHERE
        name LIKE '%frame%'
        OR name LIKE '%DrawFrame%'
    LIMIT 20;
    """

    frame_result = tp.query(frame_query)

    frame_events = []

    for row in frame_result:

        event = {
            "ts": row.ts,
            "dur": row.dur,
            "name": row.name
        }

        frame_events.append(event)

    return {
        "cpu_events": cpu_events,
        "binder_events": binder_events,
        "frame_events": frame_events
    }