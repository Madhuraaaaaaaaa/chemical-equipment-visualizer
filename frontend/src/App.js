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
import "./App.css";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8001/api/upload/",
      formData
    );
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
            backgroundColor: "#1976d2",
          },
        ],
      }
    : null;

  return (
    <div className="app-container">
      <h2>Chemical Equipment Parameter Visualizer</h2>

      <div className="section upload-box">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload CSV</button>
        <button className="secondary-btn" onClick={downloadPDF}>
          Download PDF
        </button>
      </div>

      {summary && (
        <>
          <div className="section summary">
            <h3>Summary</h3>
            <p>Total Count: {summary.total_count}</p>
            <p>Avg Flowrate: {summary.avg_flowrate}</p>
            <p>Avg Pressure: {summary.avg_pressure}</p>
            <p>Avg Temperature: {summary.avg_temperature}</p>
          </div>

          <div className="section chart-box">
            <h3>Equipment Type Distribution</h3>
            <Bar data={chartData} />
          </div>
        </>
      )}

      <div className="section history">
        <h3>Upload History</h3>
        <ul>
          {history.map((item, index) => (
            <li key={index}>
              {item.name} —{" "}
              {new Date(item.upload_time).toLocaleString()}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
