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

  // =====================================================
  // CPU DATA
  // =====================================================

  const cpuData = [
    { thread: "Thread-1", cpu: 6.1 },
    { thread: "Thread-2", cpu: 2.9 },
    { thread: "Thread-3", cpu: 1.5 },
    { thread: "Thread-4", cpu: 0.8 }
  ]

  // =====================================================
  // FRAME DATA
  // =====================================================

  const frameData = [
    { frame: 1, time: 5 },
    { frame: 2, time: 8 },
    { frame: 3, time: 14 },
    { frame: 4, time: 20 },
    { frame: 5, time: 12 }
  ]

  return (

    <div style={{ padding: "20px" }}>

      <h1>Android Trace Analyzer Dashboard</h1>

      {/* ================================================= */}
      {/* CPU ANALYSIS */}
      {/* ================================================= */}

      <h2>CPU Analysis</h2>

      <BarChart
        width={600}
        height={300}
        data={cpuData}
      >

        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="thread" />

        <YAxis />

        <Tooltip />

        <Bar dataKey="cpu" />

      </BarChart>

      {/* ================================================= */}
      {/* BINDER ANALYSIS */}
      {/* ================================================= */}

      <h2>Binder Analysis</h2>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>Binder Path</th>
            <th>Latency</th>
          </tr>
        </thead>

        <tbody>

          <tr>
            <td>binder transaction</td>
            <td>5.5ms</td>
          </tr>

          <tr>
            <td>binder reply</td>
            <td>2.8ms</td>
          </tr>

        </tbody>

      </table>

      {/* ================================================= */}
      {/* FRAME / JANK ANALYSIS */}
      {/* ================================================= */}

      <h2>Frame & Jank Analysis</h2>

      <LineChart
        width={700}
        height={300}
        data={frameData}
      >

        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="frame" />

        <YAxis />

        <Tooltip />

        <Line dataKey="time" />

      </LineChart>

      <p>Dropped Frames: 0</p>

      <p>Jank Percentage: 0%</p>

      {/* ================================================= */}
      {/* TRACE COMPARISON */}
      {/* ================================================= */}

      <h2>Trace Comparison</h2>

      <table border="1" cellPadding="10">

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
            <td>0.66ms</td>
            <td>1.20ms</td>
          </tr>

          <tr>
            <td>CPU Usage</td>
            <td>6%</td>
            <td>12%</td>
          </tr>

          <tr>
            <td>Jank</td>
            <td>0%</td>
            <td>8%</td>
          </tr>

        </tbody>

      </table>

      {/* ================================================= */}
      {/* TEMPORAL TIMELINE */}
      {/* ================================================= */}

      <h2>Camera Launch Timeline</h2>

      <ul>

        <li>Touch Event</li>

        <li>Surface Creation</li>

        <li>Camera Open</li>

        <li>Binder Transaction</li>

        <li>Preview Start</li>

        <li>First Frame Displayed</li>

      </ul>

    </div>
  )
}

export default AllComponents