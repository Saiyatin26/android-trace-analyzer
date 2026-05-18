# =========================================================
# FINAL COMPARATIVE INTELLIGENCE ENGINE
# =========================================================

def compare_device_performance(

    trace_a_cpu,
    trace_b_cpu,

    trace_a_binder,
    trace_b_binder,

    trace_a_frame,
    trace_b_frame
):

    insights = []

    score_a = 0
    score_b = 0

    # =====================================================
    # CPU COMPARISON
    # =====================================================

    cpu_a = trace_a_cpu["average_duration_ms"]

    cpu_b = trace_b_cpu["average_duration_ms"]

    if cpu_a < cpu_b:

        score_a += 1

        insights.append(

            "Trace A shows lower CPU scheduling latency."
        )

    else:

        score_b += 1

        insights.append(

            "Trace B shows lower CPU scheduling latency."
        )

    # =====================================================
    # BINDER COMPARISON
    # =====================================================

    binder_a = trace_a_binder[
        "average_latency_ms"
    ]

    binder_b = trace_b_binder[
        "average_latency_ms"
    ]

    if binder_a < binder_b:

        score_a += 1

        insights.append(

            "Trace A has lower Binder transaction latency."
        )

    else:

        score_b += 1

        insights.append(

            "Trace B has lower Binder transaction latency."
        )

    # =====================================================
    # FRAME / JANK COMPARISON
    # =====================================================

    jank_a = trace_a_frame[
        "jank_percentage"
    ]

    jank_b = trace_b_frame[
        "jank_percentage"
    ]

    if jank_a < jank_b:

        score_a += 1

        insights.append(

            "Trace A shows better frame rendering stability."
        )

    else:

        score_b += 1

        insights.append(

            "Trace B shows better frame rendering stability."
        )

    # =====================================================
    # FINAL WINNER
    # =====================================================

    if score_a > score_b:

        final_result = (

            "TRACE A demonstrates better overall "
            "performance and responsiveness."
        )

    elif score_b > score_a:

        final_result = (

            "TRACE B demonstrates better overall "
            "performance and responsiveness."
        )

    else:

        final_result = (

            "TRACE A and TRACE B show "
            "similar performance characteristics."
        )

    return {

        "trace_a_score": score_a,

        "trace_b_score": score_b,

        "insights": insights,

        "final_result": final_result
    }