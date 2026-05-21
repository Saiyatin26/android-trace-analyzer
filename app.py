from flask import Flask
from flask import jsonify

from main import process_trace

from ai_engine import (
    generate_ai_insights
)

from optimization_engine import (
    generate_optimization_recommendations
)

from comparison_engine import (
    compare_device_performance
)

app = Flask(__name__)

# =========================================================
# API HOME
# =========================================================

@app.route("/")

def home():

    return jsonify({

        "message":
        "Android Trace Analyzer API Running"
    })


# =========================================================
# FULL ANALYSIS API
# =========================================================

@app.route("/analyze")

def analyze():

    # =====================================================
    # PROCESS TRACE A
    # =====================================================

    trace_a = process_trace(
        "traces/trace_A.perfetto-trace"
    )

    # =====================================================
    # PROCESS TRACE B
    # =====================================================

    trace_b = process_trace(
        "traces/trace_B.perfetto-trace"
    )

    # =====================================================
    # AI INSIGHTS
    # =====================================================

    ai_insights = generate_ai_insights(

        trace_a["cpu"],
        trace_b["cpu"],

        trace_a["binder"],
        trace_b["binder"],

        trace_a["frame"],
        trace_b["frame"]
    )

    # =====================================================
    # OPTIMIZATION SUGGESTIONS
    # =====================================================

    optimization = (
        generate_optimization_recommendations(

            trace_b["cpu"],
            trace_b["binder"],
            trace_b["frame"]
        )
    )

    # =====================================================
    # FINAL DEVICE COMPARISON
    # =====================================================

    comparison = compare_device_performance(

        trace_a["cpu"],
        trace_b["cpu"],

        trace_a["binder"],
        trace_b["binder"],

        trace_a["frame"],
        trace_b["frame"]
    )

    # =====================================================
    # FINAL JSON RESPONSE
    # =====================================================

    return jsonify({

        "trace_a": trace_a,

        "trace_b": trace_b,

        "ai_insights": ai_insights,

        "optimization": optimization,

        "comparison": comparison
    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)