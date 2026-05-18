import sqlite3

DB_NAME = "events.db"

# =========================================================
# CPU & THREAD STATE ANALYZER
# =========================================================

def analyze_cpu_load():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'CPU_SCHED'
    """)

    total_events = cursor.fetchone()[0]

    cursor.execute("""
    SELECT AVG(duration_ms)
    FROM events
    WHERE event_type = 'CPU_SCHED'
    """)

    avg_duration = cursor.fetchone()[0]

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

    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'BINDER_CALL'
    """)

    total_calls = cursor.fetchone()[0]

    cursor.execute("""
    SELECT AVG(duration_ms)
    FROM events
    WHERE event_type = 'BINDER_CALL'
    """)

    avg_latency = cursor.fetchone()[0]

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

    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'FRAME_RENDER'
    """)

    total_frames = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE event_type = 'FRAME_RENDER'
    AND duration_ms > 16
    """)

    dropped_frames = cursor.fetchone()[0]

    cursor.execute("""
    SELECT duration_ms
    FROM events
    WHERE event_type = 'FRAME_RENDER'
    ORDER BY duration_ms DESC
    LIMIT 10
    """)

    worst_frames = cursor.fetchall()

    conn.close()

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
# IMPROVEMENT PERCENTAGE CALCULATOR
# =========================================================

def calculate_improvement(before, after):

    if before == 0:
        return 0

    improvement = (
        (before - after) / before
    ) * 100

    return round(improvement, 2)


# =========================================================
# OPTIMIZATION VALIDATION ENGINE
# =========================================================

def validate_optimization(

    cpu_before,
    cpu_after,

    binder_before,
    binder_after,

    frame_before,
    frame_after
):

    cpu_improvement = calculate_improvement(

        cpu_before["average_duration_ms"],
        cpu_after["average_duration_ms"]
    )

    binder_improvement = calculate_improvement(

        binder_before["average_latency_ms"],
        binder_after["average_latency_ms"]
    )

    jank_improvement = calculate_improvement(

        frame_before["jank_percentage"],
        frame_after["jank_percentage"]
    )

    overall_score = (

        cpu_improvement
        + binder_improvement
        + jank_improvement

    ) / 3

    return {

        "cpu_improvement_percent":
        cpu_improvement,

        "binder_improvement_percent":
        binder_improvement,

        "jank_improvement_percent":
        jank_improvement,

        "overall_optimization_score":
        round(overall_score, 2)
    }


# =========================================================
# TRACE COMPARISON
# =========================================================

def compare_traces(trace_before, trace_after):

    comparison = {

        "cpu_difference":

        trace_after["average_duration_ms"]
        - trace_before["average_duration_ms"],

        "binder_latency_difference":

        trace_after["average_latency_ms"]
        - trace_before["average_latency_ms"]
    }

    return comparison