# 🛡️ FINTRACE AI – RIFT-Compliant Money Muling Detection System

---

## 📌 Project Overview

**FINTRACE AI** is a graph-based financial fraud detection system designed to identify **money muling networks** from transactional datasets.  
The system strictly adheres to the **RIFT JSON Schema** and focuses on detecting suspicious transaction patterns using advanced **graph analytics** and **risk scoring techniques**.

The platform enables investigators and financial institutions to:

- Detect coordinated fraud rings  
- Visualize complex transaction networks  
- Identify mule accounts using behavioral patterns  
- Export structured **RIFT-compliant intelligence reports**

---

## 🎯 Goal

Build a **RIFT-compliant Money Muling Detection System** that:

- Generates exact JSON outputs matching the RIFT schema  
- Detects fraud rings using graph analytics  
- Calculates suspicion scores for involved entities  
- Provides an interactive dashboard for visualization and analysis  

---

## 🧩 System Architecture


CSV Transaction Data
↓
FastAPI Backend
↓
Graph Construction (NetworkX)
↓
Pattern Detection Engine
↓
Suspicion Score Generator
↓
RIFT JSON Builder
↓
React Dashboard Visualization


---

## ⚙️ Tech Stack

| Layer          | Technology        |
|--------------|------------------|
| Backend      | FastAPI          |
| Graph Logic  | NetworkX         |
| Frontend     | React (Vite)     |
| Visualization| Graph-based UI   |
| Data Input   | CSV Upload       |
| Output       | RIFT JSON Schema |

---

## 👥 Team Execution Plan

### 🔹 Backend Team

#### **Fathima**
- FastAPI Setup  
- CSV Upload Endpoint  
- Graph Construction using NetworkX  
- Cycle Detection (Length 3–5)  
- Suspicion Score Base Structure  
- JSON Schema Builder  

#### **Krishnapriya**
- Fan-in Detection  
- Fan-out Detection  
- Shell Chain Detection  
- 72-Hour Velocity Detection  
- False Positive Mitigation Logic  

✅ **Deliverable by Hour 8:**  
Backend returns valid **RIFT-compliant JSON** for sample CSV input.

---

### 🔹 Frontend Team

#### **Nandana**
- React App Setup  
- File Upload UI  
- Summary Panel  
- Fraud Ring Summary Table  
- JSON Download Button  

#### **Fayiza**
- Graph Visualization  
- Node Size based on Suspicion Score  
- Risk Level Color Coding  
- Visual Highlighting of Fraud Rings  

✅ **Deliverable by Hour 15:**  
Fully functional dashboard integrated with backend.

---

## 🧠 Detection Logic Implemented

The system detects the following suspicious transaction patterns:

- **Transaction Cycles** (Length 3–5)  
- **Fan-in Patterns** (10+ senders → 1 receiver)  
- **Fan-out Patterns** (1 sender → 10+ receivers)  
- **Shell Chains** (Layered transaction chains)  
- **72-Hour High Velocity Transfers**

Each detected entity is assigned a **Suspicion Score** based on:

- Pattern involvement  
- Transaction frequency  
- Network centrality  
- Temporal behavior  

---

## 🔌 Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
💻 Frontend Setup
cd frontend
npm install
npm run dev
📤 API Endpoints
Method	Endpoint	Description
POST	/upload-csv	Upload transaction CSV
GET	/detect	Run detection engine
GET	/export-json	Download RIFT JSON report
📊 Dashboard Features

Upload transaction dataset

View detected fraud rings

Risk-based node visualization

Suspicion score scaling

Tabular fraud summaries

Export structured JSON reports

📁 Output

The system generates:

Structured RIFT-compliant JSON report

Fraud network visualization

Summary of detected mule rings

🚀 Future Enhancements

Machine Learning-based scoring

Real-time transaction ingestion

Role-based investigator access

Alert prioritization system

🏁 Hackathon Timeline
Time	Milestone
Hour 8	Backend JSON Output Ready
Hour 15	Dashboard Integration Complete
📜 License

This project is developed as part of a hackathon challenge for financial fraud detection using graph intelligence.
