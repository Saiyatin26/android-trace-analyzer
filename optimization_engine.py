# =========================================================
# OPTIMIZATION RECOMMENDATION ENGINE
# =========================================================

def generate_optimization_recommendations(

    cpu_analysis,
    binder_analysis,
    frame_analysis
):

    recommendations = []

    # =====================================================
    # CPU OPTIMIZATION
    # =====================================================

    avg_cpu = cpu_analysis["average_duration_ms"]

    if avg_cpu > 0.5:

        recommendations.append({

            "problem":
            "High CPU contention detected.",

            "optimization":
            "Move heavy tasks to background threads.",

            "expected_improvement":
            "Reduced main-thread blocking and smoother execution."
        })

        recommendations.append({

            "problem":
            "CPU scheduling overhead observed.",

            "optimization":
            "Reduce unnecessary thread wakeups and optimize scheduling.",

            "expected_improvement":
            "Lower CPU latency and better responsiveness."
        })

    # =====================================================
    # BINDER OPTIMIZATION
    # =====================================================

    avg_binder = binder_analysis["average_latency_ms"]

    if avg_binder > 0.5:

        recommendations.append({

            "problem":
            "High Binder transaction latency detected.",

            "optimization":
            "Reduce synchronous Binder calls and use asynchronous communication.",

            "expected_improvement":
            "Faster IPC communication and reduced blocking."
        })

        recommendations.append({

            "problem":
            "Frequent Binder transactions detected.",

            "optimization":
            "Batch Binder requests to reduce IPC overhead.",

            "expected_improvement":
            "Reduced Binder overhead and improved throughput."
        })

    # =====================================================
    # FRAME / JANK OPTIMIZATION
    # =====================================================

    jank = frame_analysis["jank_percentage"]

    if jank > 5:

        recommendations.append({

            "problem":
            "UI frame instability detected.",

            "optimization":
            "Optimize rendering pipeline and reduce UI thread blocking.",

            "expected_improvement":
            "Reduced dropped frames and smoother animations."
        })

        recommendations.append({

            "problem":
            "Slow frame rendering observed.",

            "optimization":
            "Reduce overdraw and optimize frame composition.",

            "expected_improvement":
            "Improved rendering performance and lower frame latency."
        })

    # =====================================================
    # OVERALL SYSTEM OPTIMIZATION
    # =====================================================

    if (
        avg_cpu > 0.5
        and avg_binder > 0.5
    ):

        recommendations.append({

            "problem":
            "Combined CPU and Binder bottleneck detected.",

            "optimization":
            "Parallelize workloads and reduce IPC dependency on main thread.",

            "expected_improvement":
            "Improved camera launch latency and system responsiveness."
        })

    # =====================================================
    # DEFAULT CASE
    # =====================================================

    if len(recommendations) == 0:

        recommendations.append({

            "problem":
            "No major bottlenecks detected.",

            "optimization":
            "Current system performance is stable.",

            "expected_improvement":
            "Maintain current optimization strategy."
        })

    return recommendations


# =========================================================
# OPTIMIZATION VALIDATION REPORT
# =========================================================

def generate_validation_report(validation_results):

    report = []

    cpu_improvement = (
        validation_results[
            "cpu_improvement_percent"
        ]
    )

    binder_improvement = (
        validation_results[
            "binder_improvement_percent"
        ]
    )

    jank_improvement = (
        validation_results[
            "jank_improvement_percent"
        ]
    )

    overall_score = (
        validation_results[
            "overall_optimization_score"
        ]
    )

    # =====================================================
    # CPU VALIDATION
    # =====================================================

    if cpu_improvement > 0:

        report.append(

            f"CPU performance improved by "
            f"{cpu_improvement}% after optimization."
        )

    else:

        report.append(

            "CPU optimization did not improve performance."
        )

    # =====================================================
    # BINDER VALIDATION
    # =====================================================

    if binder_improvement > 0:

        report.append(

            f"Binder latency improved by "
            f"{binder_improvement}% after optimization."
        )

    else:

        report.append(

            "Binder optimization showed limited improvement."
        )

    # =====================================================
    # JANK VALIDATION
    # =====================================================

    if jank_improvement > 0:

        report.append(

            f"UI jank reduced by "
            f"{jank_improvement}% after optimization."
        )

    else:

        report.append(

            "No major frame rendering improvement detected."
        )

    # =====================================================
    # OVERALL SCORE
    # =====================================================

    if overall_score > 50:

        report.append(

            "Overall optimization effectiveness is HIGH."
        )

    elif overall_score > 20:

        report.append(

            "Overall optimization effectiveness is MODERATE."
        )

    else:

        report.append(

            "Overall optimization effectiveness is LOW."
        )

    return report