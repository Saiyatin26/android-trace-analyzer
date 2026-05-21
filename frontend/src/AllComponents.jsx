import { useEffect, useState } from "react"
import axios from "axios"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LineChart,
  Line
} from "recharts"

function AllComponents() {
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await axios.get("/api/analyze")
        setAnalysis(response.data)
      } catch (err) {
        setError(err.message || "Failed to load analysis data.")
      } finally {
        setLoading(false)
      }
    }

    fetchAnalysis()
  }, [])

  const cpuData = analysis?.trace_b?.cpu?.top_threads?.map(
    (row, index) => ({
      thread: `Thread-${row[0] ?? index + 1}`,
      cpu: row[1] ?? 0
    })
  ) ?? [
    { thread: "Thread-1", cpu: 6.1 },
    { thread: "Thread-2", cpu: 2.9 },
    { thread: "Thread-3", cpu: 1.5 },
    { thread: "Thread-4", cpu: 0.8 }
  ]

  const frameData = analysis?.trace_b?.frame?.worst_frame_times?.map(
    (duration, index) => ({ frame: index + 1, time: duration })
  ) ?? [
    { frame: 1, time: 5 },
    { frame: 2, time: 8 },
    { frame: 3, time: 14 },
    { frame: 4, time: 20 },
    { frame: 5, time: 12 }
  ]

  const binderPaths = analysis?.trace_b?.binder?.slow_binder_paths ?? [
    ["binder transaction", 5.5],
    ["binder reply", 2.8]
  ]

  const traceA = analysis?.trace_a
  const traceB = analysis?.trace_b

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Android Trace Analyzer Dashboard</h1>

      {loading && <p>Loading analysis from backend...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && !error && analysis && (
        <>
          <section>
            <h2>AI Insights</h2>
            <ul>
              {analysis.ai_insights.map((insight, index) => (
                <li key={index}>{insight}</li>
              ))}
            </ul>
          </section>

          <section>
            <h2>Optimization Suggestions</h2>
            {analysis.optimization.map((item, index) => (
              <div
                key={index}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  marginBottom: "12px",
                  padding: "12px"
                }}
              >
                <strong>Problem:</strong> {item.problem}
                <br />
                <strong>Optimization:</strong> {item.optimization}
                <br />
                <strong>Expected Improvement:</strong> {item.expected_improvement}
              </div>
            ))}
          </section>

          <section>
            <h2>Trace Comparison</h2>
            <table border="1" cellPadding="10" style={{ width: "100%", marginBottom: "20px" }}>
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Trace A</th>
                  <th>Trace B</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Binder Latency</td>
                  <td>{traceA?.binder?.average_latency_ms?.toFixed(2) ?? "N/A"} ms</td>
                  <td>{traceB?.binder?.average_latency_ms?.toFixed(2) ?? "N/A"} ms</td>
                </tr>
                <tr>
                  <td>CPU Duration</td>
                  <td>{traceA?.cpu?.average_duration_ms?.toFixed(2) ?? "N/A"} ms</td>
                  <td>{traceB?.cpu?.average_duration_ms?.toFixed(2) ?? "N/A"} ms</td>
                </tr>
                <tr>
                  <td>Jank Percentage</td>
                  <td>{traceA?.frame?.jank_percentage?.toFixed(2) ?? "N/A"}%</td>
                  <td>{traceB?.frame?.jank_percentage?.toFixed(2) ?? "N/A"}%</td>
                </tr>
              </tbody>
            </table>

            <h3>Comparison Insights</h3>
            <ul>
              {analysis.comparison.insights.map((insight, index) => (
                <li key={index}>{insight}</li>
              ))}
            </ul>

            <p>
              <strong>Final Result:</strong> {analysis.comparison.final_result}
            </p>
          </section>

          <section>
            <h2>CPU Analysis</h2>
            <BarChart width={600} height={300} data={cpuData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="thread" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cpu" fill="#8884d8" />
            </BarChart>
          </section>

          <section>
            <h2>Binder Analysis</h2>
            <table border="1" cellPadding="10" style={{ width: "100%" }}>
              <thead>
                <tr>
                  <th>Binder Path</th>
                  <th>Max Latency (ms)</th>
                </tr>
              </thead>
              <tbody>
                {binderPaths.map((path, index) => (
                  <tr key={index}>
                    <td>{path[0]}</td>
                    <td>{path[1]?.toFixed?.(2) ?? path[1]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <section>
            <h2>Frame & Jank Analysis</h2>
            <LineChart width={700} height={300} data={frameData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="frame" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="time" stroke="#82ca9d" />
            </LineChart>
            <p>Dropped Frames: {traceB?.frame?.dropped_frames ?? 0}</p>
            <p>Jank Percentage: {traceB?.frame?.jank_percentage?.toFixed(2) ?? 0}%</p>
          </section>

          <section>
            <h2>Temporal Event Chains</h2>
            <ul>
              {analysis.trace_b.temporal.map((chain) => (
                <li key={chain.chain_id}>
                  <strong>Chain {chain.chain_id}:</strong> {chain.events.join(" → ")}
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
    </div>
  )
}

export default AllComponents