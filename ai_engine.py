# =========================================================
# AI COMPARATIVE REASONING ENGINE
# =========================================================

def generate_ai_insights(

    trace_a_cpu,
    trace_b_cpu,

    trace_a_binder,
    trace_b_binder,

    trace_a_frame,
    trace_b_frame
):

    insights = []

    # =====================================================
    # CPU ANALYSIS
    # =====================================================

    cpu_a = trace_a_cpu[
        "average_duration_ms"
    ]

    cpu_b = trace_b_cpu[
        "average_duration_ms"
    ]

    if cpu_a < cpu_b:

        insights.append(

            "Trace A shows lower CPU contention "
            "and better scheduling efficiency."
        )

    else:

        insights.append(

            "Trace B shows lower CPU contention "
            "and better scheduling efficiency."
        )

    # =====================================================
    # BINDER ANALYSIS
    # =====================================================

    binder_a = trace_a_binder[
        "average_latency_ms"
    ]

    binder_b = trace_b_binder[
        "average_latency_ms"
    ]

    if binder_a < binder_b:

        insights.append(

            "Trace A demonstrates lower Binder "
            "transaction latency."
        )

    else:

        insights.append(

            "Trace B demonstrates lower Binder "
            "transaction latency."
        )

    # =====================================================
    # FRAME / JANK ANALYSIS
    # =====================================================

    jank_a = trace_a_frame[
        "jank_percentage"
    ]

    jank_b = trace_b_frame[
        "jank_percentage"
    ]

    if jank_a < jank_b:

        insights.append(

            "Trace A provides smoother frame "
            "rendering and lower UI jank."
        )

    else:

        insights.append(

            "Trace B provides smoother frame "
            "rendering and lower UI jank."
        )

    # =====================================================
    # ROOT CAUSE ANALYSIS
    # =====================================================

    if cpu_a > cpu_b and binder_a > binder_b:

        insights.append(

            "CPU contention in Trace A may be "
            "contributing to higher Binder delays."
        )

    if jank_a > jank_b:

        insights.append(

            "Frame instability in Trace A may be "
            "related to scheduling or rendering delays."
        )

    if binder_a > binder_b and jank_a > jank_b:

        insights.append(

            "High Binder latency in Trace A may "
            "be impacting frame rendering performance."
        )

    # =====================================================
    # FINAL PERFORMANCE SUMMARY
    # =====================================================

    score_a = 0
    score_b = 0

    if cpu_a < cpu_b:
        score_a += 1
    else:
        score_b += 1

    if binder_a < binder_b:
        score_a += 1
    else:
        score_b += 1

    if jank_a < jank_b:
        score_a += 1
    else:
        score_b += 1

    if score_a > score_b:

        insights.append(

            "Overall, Trace A demonstrates "
            "better responsiveness and system performance."
        )

    elif score_b > score_a:

        insights.append(

            "Overall, Trace B demonstrates "
            "better responsiveness and system performance."
        )

    else:

        insights.append(

            "Both traces show similar "
            "performance characteristics."
        )

    return insights