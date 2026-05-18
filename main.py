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

clear_events()

# =========================================================
# PROCESS TRACE A
# =========================================================

trace_a = parse_trace(TRACE_A)

normalized_cpu_a = normalize_sched_events(
    trace_a["cpu_events"]
)

normalized_binder_a = normalize_binder_events(
    trace_a["binder_events"]
)

normalized_frame_a = normalize_frame_events(
    trace_a["frame_events"]
)

events_a = (
    normalized_cpu_a
    + normalized_binder_a
    + normalized_frame_a
)

insert_events(events_a)

cpu_analysis_a = analyze_cpu_load()

binder_analysis_a = analyze_binder_calls()

frame_analysis_a = analyze_frame_jank()

print("\nTRACE A ANALYSIS\n")

print(cpu_analysis_a)

print(binder_analysis_a)

print(frame_analysis_a)

# =========================================================
# CLEAR DB FOR TRACE B
# =========================================================

clear_events()

# =========================================================
# PROCESS TRACE B
# =========================================================

trace_b = parse_trace(TRACE_B)

normalized_cpu_b = normalize_sched_events(
    trace_b["cpu_events"]
)

normalized_binder_b = normalize_binder_events(
    trace_b["binder_events"]
)

normalized_frame_b = normalize_frame_events(
    trace_b["frame_events"]
)

events_b = (
    normalized_cpu_b
    + normalized_binder_b
    + normalized_frame_b
)

insert_events(events_b)

cpu_analysis_b = analyze_cpu_load()

binder_analysis_b = analyze_binder_calls()

frame_analysis_b = analyze_frame_jank()

print("\nTRACE B ANALYSIS\n")

print(cpu_analysis_b)

print(binder_analysis_b)

print(frame_analysis_b)

# =========================================================
# COMPARATIVE ANALYSIS
# =========================================================

comparison = compare_traces(
    {
        "average_duration_ms":
        cpu_analysis_a["average_duration_ms"],

        "average_latency_ms":
        binder_analysis_a["average_latency_ms"]
    },

    {
        "average_duration_ms":
        cpu_analysis_b["average_duration_ms"],

        "average_latency_ms":
        binder_analysis_b["average_latency_ms"]
    }
)

print("\nCOMPARATIVE ANALYSIS\n")

print(comparison)

# =========================================================
# TEMPORAL ANALYSIS
# =========================================================

chains = build_event_chains()

temporal_insights = generate_temporal_insights(chains)

print("\nTEMPORAL EVENT CHAINS\n")

for insight in temporal_insights:

    print(insight)
    
# =========================================================
# AI ROOT CAUSE ENGINE
# =========================================================

ai_insights = generate_ai_insights(

    cpu_analysis_a,
    cpu_analysis_b,

    binder_analysis_a,
    binder_analysis_b,

    frame_analysis_a,
    frame_analysis_b
)

print("\nAI PERFORMANCE INSIGHTS\n")

for insight in ai_insights:

    print("-", insight)
    
    
# =========================================================
# OPTIMIZATION ENGINE
# =========================================================

optimization_results = generate_optimization_recommendations(

    cpu_analysis_a,
    binder_analysis_a,
    frame_analysis_a
)
print("\nOPTIMIZATION RECOMMENDATIONS\n")

for recommendation in optimization_results:

    print("\nProblem:")
    print(recommendation["problem"])

    print("\nOptimization:")
    print(recommendation["optimization"])

    print("\nExpected Improvement:")
    print(recommendation["expected_improvement"])

    print("\n-----------------------------------")