from parser import parse_trace

from normalization import (
    normalize_sched_events,
    normalize_binder_events,
    normalize_frame_events
)

from database import (
    create_database,
    clear_events,
    insert_events
)

from analysis_engine import (
    analyze_cpu_load,
    analyze_binder_calls,
    analyze_frame_jank,
    compare_traces
)

from temporal_engine import (
    build_event_chains,
    generate_temporal_insights
)

from optimization_engine import (
    generate_optimization_recommendations
)

from comparison_engine import (
    compare_device_performance
)

from ai_engine import generate_ai_insights


# =========================================================
# TRACE FILES
# =========================================================

TRACE_A = "traces/trace_A.perfetto-trace"

TRACE_B = "traces/trace_B.perfetto-trace"


# =========================================================
# DATABASE SETUP
# =========================================================

create_database()


# =========================================================
# GENERIC TRACE PROCESSOR
# =========================================================

def process_trace(trace_file):

    clear_events()

    trace_data = parse_trace(trace_file)

    normalized_cpu = normalize_sched_events(
        trace_data["cpu_events"]
    )

    normalized_binder = normalize_binder_events(
        trace_data["binder_events"]
    )

    normalized_frame = normalize_frame_events(
        trace_data["frame_events"]
    )

    all_events = (
        normalized_cpu
        + normalized_binder
        + normalized_frame
    )

    insert_events(all_events)

    cpu_analysis = analyze_cpu_load()

    binder_analysis = analyze_binder_calls()

    frame_analysis = analyze_frame_jank()

    chains = build_event_chains()

    temporal_insights = (
        generate_temporal_insights(chains)
    )

    return {

        "cpu": cpu_analysis,

        "binder": binder_analysis,

        "frame": frame_analysis,

        "temporal": temporal_insights
    }


# =========================================================
# PROCESS TRACE A
# =========================================================

print("\n==============================")
print("TRACE A ANALYSIS")
print("==============================")

trace_a_results = process_trace(TRACE_A)

print("\nCPU ANALYSIS\n")
print(trace_a_results["cpu"])

print("\nBINDER ANALYSIS\n")
print(trace_a_results["binder"])

print("\nFRAME ANALYSIS\n")
print(trace_a_results["frame"])


# =========================================================
# PROCESS TRACE B
# =========================================================

print("\n==============================")
print("TRACE B ANALYSIS")
print("==============================")

trace_b_results = process_trace(TRACE_B)

print("\nCPU ANALYSIS\n")
print(trace_b_results["cpu"])

print("\nBINDER ANALYSIS\n")
print(trace_b_results["binder"])

print("\nFRAME ANALYSIS\n")
print(trace_b_results["frame"])


# =========================================================
# COMPARATIVE ANALYSIS
# =========================================================

comparison = compare_traces(

    {
        "average_duration_ms":
        trace_a_results["cpu"][
            "average_duration_ms"
        ],

        "average_latency_ms":
        trace_a_results["binder"][
            "average_latency_ms"
        ]
    },

    {
        "average_duration_ms":
        trace_b_results["cpu"][
            "average_duration_ms"
        ],

        "average_latency_ms":
        trace_b_results["binder"][
            "average_latency_ms"
        ]
    }
)

print("\n==============================")
print("COMPARATIVE ANALYSIS")
print("==============================")

print(comparison)


# =========================================================
# TEMPORAL ANALYSIS
# =========================================================

print("\n==============================")
print("TEMPORAL EVENT CHAINS")
print("==============================")

for insight in trace_b_results["temporal"]:

    print(insight)


# =========================================================
# AI INSIGHTS
# =========================================================

ai_insights = generate_ai_insights(

    trace_a_results["cpu"],
    trace_b_results["cpu"],

    trace_a_results["binder"],
    trace_b_results["binder"],

    trace_a_results["frame"],
    trace_b_results["frame"]
)

print("\n==============================")
print("AI PERFORMANCE INSIGHTS")
print("==============================")

for insight in ai_insights:

    print("-", insight)


# =========================================================
# OPTIMIZATION RECOMMENDATIONS
# =========================================================

optimization_results = (
    generate_optimization_recommendations(

        trace_b_results["cpu"],
        trace_b_results["binder"],
        trace_b_results["frame"]
    )
)

print("\n==============================")
print("OPTIMIZATION RECOMMENDATIONS")
print("==============================")

for recommendation in optimization_results:

    print("\nProblem:")
    print(recommendation["problem"])

    print("\nOptimization:")
    print(recommendation["optimization"])

    print("\nExpected Improvement:")
    print(recommendation[
        "expected_improvement"
    ])

    print("\n-----------------------------------")


# =========================================================
# FINAL DEVICE COMPARISON
# =========================================================

comparison_results = compare_device_performance(

    trace_a_results["cpu"],
    trace_b_results["cpu"],

    trace_a_results["binder"],
    trace_b_results["binder"],

    trace_a_results["frame"],
    trace_b_results["frame"]
)

print("\n==============================")
print("FINAL DEVICE COMPARISON")
print("==============================")

print("\nTRACE A SCORE:")
print(comparison_results["trace_a_score"])

print("\nTRACE B SCORE:")
print(comparison_results["trace_b_score"])

print("\nCOMPARATIVE INSIGHTS\n")

for insight in comparison_results["insights"]:

    print("-", insight)

print("\nFINAL RESULT\n")

print(comparison_results["final_result"])