import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://127.0.0.1:8001/api/upload/", formData);
    setSummary(res.data);
    fetchHistory();
  };

  const fetchHistory = async () => {
    const res = await axios.get("http://127.0.0.1:8001/api/history/");
    setHistory(res.data);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const downloadPDF = () => {
    window.open("http://127.0.0.1:8001/api/report/");
  };

  const chartData = summary
    ? {
        labels: Object.keys(summary.type_distribution),
        datasets: [
          {
            label: "Equipment Count",
            data: Object.values(summary.type_distribution),
          },
        ],
      }
    : null;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Chemical Equipment Parameter Visualizer</h2>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload CSV</button>
      <button onClick={downloadPDF}>Download PDF Report</button>

      {summary && (
        <>
          <h3>Summary</h3>
          <p>Total Count: {summary.total_count}</p>
          <p>Avg Flowrate: {summary.avg_flowrate}</p>
          <p>Avg Pressure: {summary.avg_pressure}</p>
          <p>Avg Temperature: {summary.avg_temperature}</p>

          <h3>Equipment Type Distribution</h3>
          <Bar data={chartData} />
        </>
      )}

      <h3>Upload History</h3>
      <ul>
        {history.map((item, index) => (
          <li key={index}>
            {item.name} — {item.upload_time}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
