<div align="center">

# 🧠 Business DecisionAI
### Enterprise Decision Intelligence, Big Data SQL Agent & Temporal Knowledge Vault

<p align="center">
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Light%20Bulb.png" alt="Light Bulb" width="45" height="45" />
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Bar%20Chart.png" alt="Bar Chart" width="45" height="45" />
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Locked%20with%20Key.png" alt="Locked" width="45" height="45" />
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Rocket.png" alt="Rocket" width="45" height="45" />
</p>

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React 18](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![SQL](https://img.shields.io/badge/SQL_Engine-CC292B?style=for-the-badge&logo=sqlite&logoColor=white)](https://en.wikipedia.org/wiki/SQL)
[![Google Gemini API](https://img.shields.io/badge/Google_Gemini_GenAI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS_v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker / Container](https://img.shields.io/badge/Cloud_Run-2496ED?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)

<p align="center">
  <b>Transforming massive enterprise datasets, multi-period financial baselines, and macro market conditions into grounded, audit-ready AI decisions.</b>
</p>

</div>

---

## ⚡ Key Architectural Overview

> **Core Philosophy: Token-Efficient, Statistically Grounded RAG.**  
> Rather than dumping unparsed gigabytes of raw data directly into the LLM context window—which causes hallucination, token exhaustion, and context degradation—**Business DecisionAI** routes big tabular records through an in-memory SQL execution agent. It extracts verified statistical deltas, aggregates, and variances first, feeding only high-signal, mathematically proven facts into the generative reasoning pipeline.
code
Code
┌──────────────────────────────────────────────────────────────┐
                │               Raw Big Data Ingestion                         │
                │         (CSVs, JSON, Financials, Warehouse Logs)             │
                └──────────────────────────────┬───────────────────────────────┘
                                               │
                                               ▼
                ┌──────────────────────────────────────────────────────────────┐
                │               Autonomous Big Data SQL Agent                  │
                │   • Automatic Schema & Type Inference (Num/Date/Str/Bool)    │
                │   • ANSI SQL Execution (<5ms in-memory queries)              │
                │   • Multi-period Variance: (Current - Past) / Past           │
                │   • Holding Cost, Margin Erosion & Churn Risk Metrics        │
                └──────────────────────────────┬───────────────────────────────┘
                                               │
                                               ▼ (Grounded Summaries Only)
┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
│ Historical Vault Baseline │ │ Current Operational Updates │ │ Real-time Macro Benchmarks │
│ (Prior year balance sheets,│ │ (Active supply chain status, │ │ (Sector CAGR, Interest Rates│
│ inventory reserves logs) │ │ Q1 expansion reports) │ │ Freight Index volatility) │
└──────────────┬───────────────┘ └──────────────┬───────────────┘ └──────────────┬───────────────┘
│ │ │
└───────────────────────────────────┼───────────────────────────────────┘
▼
┌──────────────────────────────────────────────────────────────┐
│ Google Gemini GenAI Decision Intelligence Core │
│ • Executive Summary Generation │
│ • Quantitative Risk Assessment (LOW / MEDIUM / HIGH) │
│ • Mathematical Confidence Calibration (0 - 100%) │
│ • Root-Cause Strategic Reasoning Breakdown │
│ • Actionable, Phased Deployment Recommendations │
└──────────────────────────────┬───────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────┐
│ Interactive Glassmorphic Intelligence Dashboard │
│ (Temporal Delta Audit, Voice Dictation, SQL Console) │
└──────────────────────────────────────────────────────────────┘
code
Code
---

## ✨ Standout Features

### 🗄️ 1. Company Historical Data Vault & Temporal Memory
* **Company-Isolated Containers**: Stores historical baseline documents and past data tables separately from incoming operational documents under designated company IDs (e.g., `AMAZON`, `MICROSOFT`).
* **Multi-Period Temporal Tracking**: Automatically compares historical quarterly margins against newly uploaded real-time data to identify positive or negative KPI trajectories before evaluating decisions.
* **Macro Market Trend Signals**: Ingests real-world sector growth rates (CAGR), inflation metrics, cost of capital, and supply chain friction indicators into the evaluation matrix.

### 📊 2. Autonomous Big Data SQL Agent & Query Console
* **Instant In-Memory Relational Engine**: Parses and queries up to tens of thousands of records instantly using an embedded SQL engine (`AlaSQL` + `PapaParse`).
* **Smart Schema Inference**: Auto-detects data types (`number`, `string`, `date`, `boolean`) without manual schema declarations.
* **Interactive SQL Terminal**: Execute ad-hoc queries, test multi-table joins, view real-time latency (in milliseconds), and inspect data structures directly in the UI.

### 🛡️ 3. Evidence Fusion & GenAI Reasoning
* **Strict Format Enforcement**: Produces executive decision summaries, calibrated risk ratings, confidence percentages, and structured root-cause reasons.
* **Fallback Heuristic System**: Built-in statistical heuristic engine guarantees seamless risk modeling even in air-gapped environments or without active API keys.
* **Voice-Enabled Dictation**: Native Web Speech Recognition integration allows executives and analysts to dictate complex business inquiries hands-free.

---

## 🧮 Statistical & Mathematical Methods Used

| Domain | Technique / Metric | Implementation & Purpose |
| :--- | :--- | :--- |
| **Descriptive Statistics** | Grouped Aggregations & Weighted Central Tendency | `SUM(revenue)`, `AVG(margin_pct)`, and `AVG(current_stock)` per region/SKU. |
| **Time-Series Variance** | Period-over-Period Delta Calculation | $\Delta\% = \frac{\text{Current} - \text{Past}}{\text{Past}} \times 100$ to audit margin compression and revenue drift. |
| **Risk Sensitivity** | Boundary Threshold & Concentration Modeling | Isolating accounts with churn probability $> 75\%$ or inventory holding cost $> 15\%$. |
| **Confidence Scoring** | Normalized Multi-Factor Evidence Scoring | Calibrating AI confidence ($0-100\%$) based on row coverage, variance consistency, and document density. |
| **Macro Fusion** | Sensitivity Weighting | Discounting expansion initiatives against high interest-rate environments. |

---

## 🛠️ Technology Stack & Tooling

### **Languages & Frameworks**
* **Frontend**: React 18, TypeScript, Tailwind CSS v4, Motion (`framer-motion`), Lucide Icons
* **Backend**: Node.js, Express, TypeScript (`tsx`), Vite Middleware
* **Core Analytics & Big Data**: SQL (`AlaSQL`), PapaParse (CSV Streaming & Ingestion)
* **Generative AI & LLMs**: Google Gemini API (`@google/genai`), Few-shot Prompt Engineering
* **Voice & Audio**: Web Speech API (SpeechRecognition & Webkit fallback)

### **Deployment & Cloud Architecture**
* **Containerization**: Docker / Cloud Run (Port 3000 ingress)
* **Build System**: `esbuild` bundled CJS backend + Vite SPA production pipeline
* **Data Privacy**: Client-side secure API proxy keeping LLM and storage keys server-side

---

## 🚀 Quickstart & Local Installation

### Prerequisites
* **Node.js**: v18+ or v20+
* **Package Manager**: `npm` or `bun`
* **Gemini API Key**: (Optional, default local heuristic engine available)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Business-Decision-Ai-App.git
cd Business-Decision-Ai-App

2. Install Dependencies
code
Bash
npm install

3. Configure Environment Variables
Create a .env file in the root directory:
code
Env
GEMINI_API_KEY=your_gemini_api_key_here

4. Run Development Server
code
Bash
npm run dev
Open http://localhost:3000 in your browser.

5. Production Build
code
Bash
npm run build
npm start

💡 How It Works (Step-by-Step Scenario)
Select or Create a Company Profile: Choose a pre-seeded enterprise preset (e.g. Amazon, Microsoft) or enter your own business name, industry, and target market.
Upload Past & Current Datasets:
Add a past baseline spreadsheet (e.g. prior year's inventory or customer metrics).
Add current period documents (e.g. current quarter logistics constraints or proposed budget changes).
Autonomous SQL Ingestion: The Big Data SQL Agent ingests all files, translates them into structured tables, and pre-calculates statistical deltas.
Pose a Decision Query:
"Should I increase my investment in motor inventory by 10% this year?"
Receive Grounded Analytics: The system returns:
Risk Level: High / Medium / Low
Confidence: Calibrated percentage
Temporal Delta Matrix: Revenue drift and warehouse utilization variance
Root-Cause Reasoning: Step-by-step analytical arguments
Recommended Next Step: Actionable, staged pilot milestones
