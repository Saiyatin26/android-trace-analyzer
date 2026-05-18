import sqlite3

DB_NAME = "events.db"

# =========================================================
# CPU & THREAD STATE ANALYZER
# =========================================================

def analyze_cpu_load():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Total CPU scheduling events
    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'CPU_SCHED'
    """)

    total_events = cursor.fetchone()[0]

    # Average CPU execution duration
    cursor.execute("""
    SELECT AVG(duration_ms)
    FROM events
    WHERE event_type = 'CPU_SCHED'
    """)

    avg_duration = cursor.fetchone()[0]

    # Top CPU-consuming threads
    cursor.execute("""
    SELECT
        thread_id,
        SUM(duration_ms) as total_cpu_time
    FROM events
    WHERE event_type = 'CPU_SCHED'
    GROUP BY thread_id
    ORDER BY total_cpu_time DESC
    LIMIT 10
    """)

    top_threads = cursor.fetchall()

    conn.close()

    return {
        "total_cpu_events": total_events,
        "average_duration_ms": avg_duration,
        "top_threads": top_threads
    }


# =========================================================
# BINDER CALL ANALYZER
# =========================================================

def analyze_binder_calls():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Total Binder calls
    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'BINDER_CALL'
    """)

    total_calls = cursor.fetchone()[0]

    # Average Binder latency
    cursor.execute("""
    SELECT AVG(duration_ms)
    FROM events
    WHERE event_type = 'BINDER_CALL'
    """)

    avg_latency = cursor.fetchone()[0]

    # Top 10 slowest Binder paths
    cursor.execute("""
    SELECT
        binder_name,
        MAX(duration_ms) as max_latency
    FROM events
    WHERE event_type = 'BINDER_CALL'
    GROUP BY binder_name
    ORDER BY max_latency DESC
    LIMIT 10
    """)

    slow_paths = cursor.fetchall()

    conn.close()

    return {
        "total_binder_calls": total_calls,
        "average_latency_ms": avg_latency,
        "slow_binder_paths": slow_paths
    }


# =========================================================
# FRAME DROP & JANK ANALYZER
# =========================================================

def analyze_frame_jank():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Total frame events
    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'FRAME_RENDER'
    """)

    total_frames = cursor.fetchone()[0]

    # Frames taking longer than 16ms
    # (60 FPS threshold)
    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'FRAME_RENDER'
    AND duration_ms > 16
    """)

    dropped_frames = cursor.fetchone()[0]

    # Worst frame render times
    cursor.execute("""
    SELECT duration_ms
    FROM events
    WHERE event_type = 'FRAME_RENDER'
    ORDER BY duration_ms DESC
    LIMIT 10
    """)

    worst_frames = cursor.fetchall()

    conn.close()

    # Jank percentage
    jank_percentage = 0

    if total_frames > 0:
        jank_percentage = (
            dropped_frames / total_frames
        ) * 100

    return {
        "total_frames": total_frames,
        "dropped_frames": dropped_frames,
        "jank_percentage": jank_percentage,
        "worst_frame_times": worst_frames
    }


# =========================================================
# COMPARATIVE ANALYSIS
# =========================================================

def compare_traces(trace_a_metrics, trace_b_metrics):

    comparison = {

        "cpu_difference":
        trace_b_metrics["average_duration_ms"]
        - trace_a_metrics["average_duration_ms"],

        "binder_latency_difference":
        trace_b_metrics["average_latency_ms"]
        - trace_a_metrics["average_latency_ms"]
    }

    return comparison