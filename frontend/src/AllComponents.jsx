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
  Line,
  ResponsiveContainer,
  ScatterChart,
  Scatter
} from "recharts"

function AllComponents() {
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadAnalysis = async () => {
      try {
        const response = await axios.get("/api/analyze")
        setAnalysis(response.data)
      } catch (err) {
        const backendDown =
          err.code === "ECONNREFUSED" ||
          err.response?.status === 502 ||
          err.response?.status === 504

        const message = backendDown
          ? "Backend unavailable. Start the Flask API with 'python app.py' on port 5000 and refresh."
          : err.response?.data?.message || err.message || "Unable to fetch analysis data."

        setError(message)
      } finally {
        setLoading(false)
      }
    }
    loadAnalysis()
  }, [])

  const traceA = analysis?.trace_a
  const traceB = analysis?.trace_b

  const cpuData = traceB?.cpu?.top_threads?.length
    ? traceB.cpu.top_threads.map((row, index) => ({
        thread: row[0] ?? `Thread ${index + 1}`,
        cpu: Number(row[1] ?? 0)
      }))
    : [
        { thread: "Thread-1", cpu: 6.1 },
        { thread: "Thread-2", cpu: 2.9 },
        { thread: "Thread-3", cpu: 1.5 },
        { thread: "Thread-4", cpu: 0.8 }
      ]

  const frameData = traceB?.frame?.worst_frame_times?.length
    ? traceB.frame.worst_frame_times.map((item, index) => ({
        frame: index + 1,
        time: Number(Array.isArray(item) ? item[0] : item)
      }))
    : [
        { frame: 1, time: 5 },
        { frame: 2, time: 8 },
        { frame: 3, time: 14 },
        { frame: 4, time: 20 },
        { frame: 5, time: 12 }
      ]

  const binderPaths = traceB?.binder?.slow_binder_paths ?? []
  const temporalChains = traceB?.temporal ?? []
  const temporalGraphData = temporalChains.flatMap((chain) =>
    chain.events.map((event, index) => ({
      chainId: chain.chain_id,
      position: index + 1,
      event,
      label: `Chain ${chain.chain_id}`
    }))
  )

  const formatValue = (value, suffix = "") =>
    value === null || value === undefined ? "N/A" : `${Number(value).toFixed(2)}${suffix}`

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <span className="dashboard__eyebrow">Android Trace Analyzer</span>
          <h1>Trace performance visualized</h1>
          <p className="dashboard__subtitle">
            See AI insights, optimization suggestions, and temporal relations directly in your browser.
          </p>
        </div>
      </header>

      {loading && <div className="dashboard__status">Loading analysis...</div>}
      {error && <div className="dashboard__status error">{error}</div>}

      {!loading && !error && analysis && (
        <>
          <section className="summary-cards">
            <article className="summary-card">
              <span className="summary-card__label">Trace B CPU Avg</span>
              <strong>{formatValue(traceB?.cpu?.average_duration_ms, " ms")}</strong>
              <p>{traceB?.cpu?.total_cpu_events ?? 0} CPU events</p>
            </article>
            <article className="summary-card">
              <span className="summary-card__label">Trace B Binder Avg</span>
              <strong>{formatValue(traceB?.binder?.average_latency_ms, " ms")}</strong>
              <p>{traceB?.binder?.total_binder_calls ?? 0} Binder calls</p>
            </article>
            <article className="summary-card">
              <span className="summary-card__label">Trace B Jank</span>
              <strong>{formatValue(traceB?.frame?.jank_percentage, "%")}</strong>
              <p>{traceB?.frame?.dropped_frames ?? 0} dropped frames</p>
            </article>
          </section>

          <section className="card-grid">
            <article className="card card--wide">
              <h2>AI Insights</h2>
              <div className="insights-list">
                {analysis.ai_insights.map((insight, index) => (
                  <div key={index} className="insight-card">
                    {insight}
                  </div>
                ))}
              </div>
            </article>

            <article className="card card--wide">
              <h2>Optimization Suggestions</h2>
              <div className="insights-list">
                {analysis.optimization.map((item, index) => (
                  <div key={index} className="insight-card">
                    <strong>Problem:</strong> {item.problem}
                    <br />
                    <strong>Optimization:</strong> {item.optimization}
                    <br />
                    <strong>Expected:</strong> {item.expected_improvement}
                  </div>
                ))}
              </div>
            </article>
          </section>

          <section className="dashboard__section chart-row">
            <article className="card chart-card">
              <h2>CPU Thread Load</h2>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={cpuData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="thread" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="cpu" fill="#8054ff" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </article>

            <article className="card chart-card">
              <h2>Frame Render Times</h2>
              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={frameData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="frame" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="time" stroke="#16a34a" strokeWidth={3} dot />
                </LineChart>
              </ResponsiveContainer>
            </article>
          </section>

          <section className="card-grid">
            <article className="card">
              <h2>Binder Latency</h2>
              <table className="table">
                <thead>
                  <tr>
                    <th>Binder Path</th>
                    <th>Max Latency</th>
                  </tr>
                </thead>
                <tbody>
                  {binderPaths.length > 0 ? (
                    binderPaths.map((path, index) => (
                      <tr key={index}>
                        <td>{path[0]}</td>
                        <td>{formatValue(path[1], " ms")}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="2">No binder path data available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </article>

            <article className="card">
              <h2>Trace Comparison</h2>
              <table className="table">
                <tbody>
                  <tr>
                    <th>Metric</th>
                    <th>Trace A</th>
                    <th>Trace B</th>
                  </tr>
                  <tr>
                    <td>CPU Avg</td>
                    <td>{formatValue(traceA?.cpu?.average_duration_ms, " ms")}</td>
                    <td>{formatValue(traceB?.cpu?.average_duration_ms, " ms")}</td>
                  </tr>
                  <tr>
                    <td>Binder Avg</td>
                    <td>{formatValue(traceA?.binder?.average_latency_ms, " ms")}</td>
                    <td>{formatValue(traceB?.binder?.average_latency_ms, " ms")}</td>
                  </tr>
                  <tr>
                    <td>Jank</td>
                    <td>{formatValue(traceA?.frame?.jank_percentage, "%")}</td>
                    <td>{formatValue(traceB?.frame?.jank_percentage, "%")}</td>
                  </tr>
                </tbody>
              </table>
              <div className="callout">
                <strong>Final Result:</strong> {analysis.comparison.final_result}
              </div>
            </article>
          </section>

          <section className="card-grid">
            <article className="card card--wide temporal-card">
              <h2>Temporal Relation Graph</h2>
              <div className="temporal-graph-container">
                <ResponsiveContainer width="100%" height={360}>
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      type="number"
                      dataKey="chainId"
                      name="Chain"
                      tickFormatter={(value) => `C${value}`}
                      allowDecimals={false}
                    />
                    <YAxis type="number" dataKey="position" name="Position" allowDecimals={false} />
                    <Tooltip
                      cursor={{ strokeDasharray: "3 3" }}
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload
                          return (
                            <div className="tooltip-box">
                              <div><strong>{data.label}</strong></div>
                              <div>Event: {data.event}</div>
                              <div>Position: {data.position}</div>
                            </div>
                          )
                        }
                        return null
                      }}
                    />
                    <Scatter data={temporalGraphData} fill="#ff7043" />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
              <div className="insights-list">
                {temporalChains.map((chain) => (
                  <div key={chain.chain_id} className="insight-card">
                    <strong>Chain {chain.chain_id}:</strong> {chain.events.join(" → ")}
                  </div>
                ))}
              </div>
            </article>
          </section>
        </>
      )}
    </div>
  )
}

export default AllComponents