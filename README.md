# Chemical Equipment Parameter Visualizer (Hybrid App)

A hybrid application that works as:
- 🌐 Web App (React.js + Chart.js)
- 🖥 Desktop App (PyQt5 + Matplotlib)
- ⚙ Backend (Django + Django REST Framework)

The app allows users to upload a CSV file containing chemical equipment data and visualizes summary statistics and equipment type distribution.

---

## 🚀 Features

- Upload CSV file (Web & Desktop)
- Backend parses and analyzes data using Pandas
- Shows:
  - Total equipment count
  - Average Flowrate, Pressure, Temperature
  - Equipment type distribution chart
- Stores last 5 uploads (history)
- Generate PDF report
- Same backend used by both Web & Desktop frontend

---

## 🛠 Tech Stack

**Backend**
- Django
- Django REST Framework
- Pandas
- SQLite

**Web Frontend**
- React.js
- Axios
- Chart.js

**Desktop App**
- PyQt5
- Matplotlib
- Requests

---

## 📂 Project Structure

