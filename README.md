# 🚀 Loan Approval Prediction System

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-teal?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

A **full-stack machine learning web application** that predicts loan approval status based on applicant details.  
The project follows **clean architecture**, **scalable backend design**, and **industry-standard ML practices**, making it suitable for **academic, portfolio, and FinTech prototype use**.

---

## 📌 Overview

The **Loan Approval Prediction System** collects applicant information via a responsive frontend, processes it through a FastAPI backend, and predicts loan approval using a trained machine learning model.

---

## ✨ Features

- ⚡ High-performance REST API using FastAPI
- 🧠 ML-powered loan approval prediction
- 📊 Data visualization using Chart.js
- 🧩 Clean separation of frontend, backend, and ML layers
- 📱 Responsive and user-friendly UI
- 🔐 Input validation using Pydantic schemas

---

## 🛠️ Tech Stack

### Frontend

| Technology | Version | Purpose |
|---------|---------|--------|
| HTML5 | Latest | Semantic markup |
| CSS3 | Latest | Styling with variables & BEM methodology |
| JavaScript | ES6+ | Event-driven interactivity |
| Chart.js | 4.4.0 | Data visualization |
| Inter Font | Latest | Professional typography |

---

### Backend

| Technology | Version | Purpose |
|---------|---------|--------|
| Python | 3.8+ | Programming language |
| FastAPI | 0.104.1 | REST API framework |
| Uvicorn | 0.24.0 | ASGI server |
| Pydantic | 2.4.2 | Data validation |

---

### Machine Learning

| Technology | Version | Purpose |
|---------|---------|--------|
| Scikit-learn | 1.3.2 | ML framework |
| Pandas | 2.1.3 | Data manipulation |
| NumPy | 1.26.2 | Numerical computing |
| Joblib | 1.3.2 | Model serialization |

---

## 📂 Project Structure

### 🖥️ Backend

```bash
backend/
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── create_dataset.py            # Dataset generation script
├── train_model.py               # Machine learning model training
│
├── app/
│   ├── __init__.py               # Package initialization
│   ├── routers/
│   │   └── predictions.py        # Loan prediction API endpoints
│   ├── schemas/
│   │   └── schemas.py            # Request & response validation models
│   └── services/
│       └── prediction_service.py # ML inference and business logic

### 🖥️ Frontend

```bash
frontend/
├── index.html                   # Semantic HTML structure
├── styles.css                   # CSS using BEM methodology
└── script.js                    # Event driven JavaScript logic



