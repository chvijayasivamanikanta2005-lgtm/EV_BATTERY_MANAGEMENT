---
title: Explainable AI EV Battery Management
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.32.0"
python_version: "3.11"
app_file: app.py
pinned: false
---

# ⚡ Explainable AI EV Battery Management System

An **Explainable AI** powered Electric Vehicle Battery Management Dashboard integrating deep learning, reinforcement learning, and explainable AI to optimise EV battery health and charging decisions.

---

## 📋 Project Overview

This system predicts **Battery State-of-Health (SoH)** using a **GRU neural network**, determines optimal charging actions using a **Double Deep Q-Network (Double DQN)**, and explains every decision through **SHAP explainability** — all presented in a real-time Streamlit dashboard.

---

## 🏗 System Architecture

```text
Battery Sensor Inputs
        │
        ▼
┌──────────────────┐
│  GRU Neural Net  │ ──→ Raw SoH Prediction
│  (20-step seq)   │
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  SoH Calibration │ ──→ Calibrated SoH (cycle-degradation adjusted)
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  Double DQN      │ ──→ Charging Action (Increase / Maintain / Decrease)
│  RL Controller   │
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  SHAP            │ ──→ 9 Explainability Visualisations
│  Explainability  │
└──────────────────┘
        │
        ▼
    Dashboard UI
```

---

## 🧠 GRU Workflow

The GRU model takes 6 battery sensor features as input:

| Feature | Description |
|---------|-------------|
| IR | Internal Resistance (Ω) |
| QC | Charge Capacity (Ah) |
| QD | Discharge Capacity (Ah) |
| Tavg | Average Temperature (°C) |
| Tmax | Maximum Temperature (°C) |
| ChargeTime | Charging Duration (s) |

- Input tensor shape: `(1, 20, 6)`
- Output: Predicted Battery State-of-Health (SoH)
- Scaling: `gru_scaler_X.pkl` (features), `gru_scaler_y.pkl` (target)

---

## 🎮 Double DQN Workflow

The RL controller receives a 4-dimensional state vector:

```text
[SoH, Temperature, Cycle Count, Charging Current]
```

And selects one of three actions:
- **Increase Charging** — Battery is healthy and cool
- **Maintain Charging** — Parameters are optimal
- **Decrease Charging** — Risk of degradation or thermal runaway

---

## 📊 SHAP Explainability

9 XAI visualisations are generated:

1. Global Feature Importance
2. SHAP Distribution Plot
3. SHAP Heatmap (All Actions)
4. Temperature Dependence
5. Cycle Dependence
6. Current Dependence
7. RL Action Influence
8. Feature Ranking
9. Combined GRU + RL Explanation

---

## 📸 Screenshots

*Add screenshots here after deployment.*

---

## 📁 Project Structure

```text
EV_Battery_AI_System/
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── components/
│   │   ├── led_switch/
│   │   └── new_input/
│   ├── images/
│   └── style.css
├── models/
│   ├── gru_soh_model.keras        (313 KB)
│   ├── double_dqn_calibrated.keras ( 84 KB)
│   ├── gru_scaler_X.pkl
│   └── gru_scaler_y.pkl
├── notebooks/
│   ├── training.ipynb
│   ├── evaluation.ipynb
│   └── preprocessing.ipynb
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── pipeline.py
│   │   ├── preprocessing.py
│   │   └── calibration.py
│   ├── models_logic/
│   │   ├── load_models.py
│   │   ├── gru_logic.py
│   │   └── rl_logic.py
│   ├── explainability/
│   │   └── shap_logic.py
│   └── visualization/
│       ├── charts.py
│       └── gauges.py
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   ├── helpers.py
│   ├── validators.py
│   └── styling.py
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🚀 Installation & Local Execution

```bash
# 1. Clone the repository
git clone <repository-url>
cd EV_Battery_AI_System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

---

## 🐳 Docker Deployment

```bash
docker build -t ev-bms-dashboard .
docker run -p 8501:8501 ev-bms-dashboard
```

---

## ☁️ Streamlit Cloud

Connect your GitHub repository to [Streamlit Cloud](https://streamlit.io/cloud). The `runtime.txt` specifies Python 3.11.

---

## 🤗 HuggingFace Spaces

This repository is compatible with HuggingFace Spaces. The `README.md` front-matter configures the Space automatically. **No Git LFS required** — all model files are stored as standard git objects.

---

## 🔬 Model Details

| Model | Architecture | File | Size |
|-------|-------------|------|------|
| SoH Predictor | GRU (64→32→1) | `gru_soh_model.keras` | 313 KB |
| RL Controller | Double DQN (Dense) | `double_dqn_calibrated.keras` | 84 KB |
| Feature Scaler | MinMaxScaler | `gru_scaler_X.pkl` | < 1 KB |
| Target Scaler | MinMaxScaler | `gru_scaler_y.pkl` | < 1 KB |

---

## ✨ Features

- Real-time SoH prediction with interactive gauge
- AI-powered charging decision with Q-value visualisation
- 9 SHAP explainability charts
- Natural language AI reasoning
- Responsive white-neumorphism design
- Cross-platform portable (macOS / Windows / Linux)

---

## 🔮 Future Improvements

- Multi-cell battery pack support
- Real-time sensor data integration via MQTT/WebSocket
- Historical trend analysis and degradation forecasting
- Edge deployment optimisation (TFLite / ONNX)
- User authentication and fleet management

---

## 👤 Author

**Vijay Manikanta**
*B.Tech — Artificial Intelligence & Machine Learning*
Research Area: Explainable AI for Electric Vehicle Battery Management