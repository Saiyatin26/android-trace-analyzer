# =========================================================
# AI ROOT CAUSE ENGINE
# =========================================================

def generate_ai_insights(

    cpu_analysis_a,
    cpu_analysis_b,

    binder_analysis_a,
    binder_analysis_b,

    frame_analysis_a,
    frame_analysis_b
):

    insights = []

    # =====================================================
    # CPU ANALYSIS
    # =====================================================

    cpu_a = cpu_analysis_a["average_duration_ms"]

    cpu_b = cpu_analysis_b["average_duration_ms"]

    if cpu_b > cpu_a:

        insights.append(
            "Trace B shows higher CPU contention compared to Trace A."
        )

    else:

        insights.append(
            "Trace B shows lower CPU contention compared to Trace A."
        )

    # =====================================================
    # BINDER ANALYSIS
    # =====================================================

    binder_a = binder_analysis_a["average_latency_ms"]

    binder_b = binder_analysis_b["average_latency_ms"]

    if binder_b > binder_a:

        insights.append(
            "Trace B has increased Binder transaction latency."
        )

    else:

        insights.append(
            "Trace B has reduced Binder transaction latency."
        )

    # =====================================================
    # FRAME / JANK ANALYSIS
    # =====================================================

    jank_a = frame_analysis_a["jank_percentage"]

    jank_b = frame_analysis_b["jank_percentage"]

    if jank_b > jank_a:

        insights.append(
            "Trace B shows increased UI jank and frame instability."
        )

    else:

        insights.append(
            "Trace B maintains stable frame rendering performance."
        )

    # =====================================================
    # ROOT CAUSE ATTRIBUTION
    # =====================================================

    if (
        binder_b > binder_a
        and cpu_b > cpu_a
    ):

        insights.append(
            "Potential bottleneck detected: "
            "CPU contention is likely contributing "
            "to Binder transaction delays."
        )

    if (
        jank_b > jank_a
        and binder_b > binder_a
    ):

        insights.append(
            "Frame rendering instability may be "
            "caused by delayed Binder transactions."
        )

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    if (
        cpu_b < cpu_a
        and binder_b < binder_a
        and jank_b <= jank_a
    ):

        insights.append(
            "Overall, Trace B demonstrates "
            "better system performance and responsiveness."
        )

    else:

        insights.append(
            "Overall, Trace B demonstrates "
            "performance degradation compared to Trace A."
        )

    return insights