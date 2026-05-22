# 🛡️ FraudShield — AI-Powered Credit Card Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Node](https://img.shields.io/badge/Node.js-18+-green?logo=node.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Open Source](https://img.shields.io/badge/Open--Source-Yes-orange)

---

## 🚀 Tagline

A real-time, full-stack AI system that detects fraudulent credit card transactions using machine learning, secure APIs, and an interactive analytics dashboard.

---

## 🧠 Project Overview

FraudShield is a full-stack machine learning system designed to simulate and detect credit card fraud in real time.

It combines:

* A React-based analytics dashboard
* A FastAPI backend serving ML predictions
* A trained ML model for fraud scoring
* Secure JWT authentication system
* Transaction logging and audit trail

### 🎯 Real-World Problem

Credit card fraud causes billions in global financial losses annually. FraudShield demonstrates how AI systems can analyze transaction patterns and flag suspicious activity instantly before damage occurs.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
A[User] --> B[React Frontend]
B --> C[FastAPI Backend]
C --> D[Authentication Layer (JWT)]
C --> E[ML Fraud Detection Model]
E --> F[Decision Engine]
F --> G[SQLite Database]
G --> B
```

---

## 🔄 System Workflow

```
User Login
   ↓
JWT Authentication
   ↓
Transaction Input (Frontend)
   ↓
API Request (FastAPI)
   ↓
Feature Processing
   ↓
ML Model Prediction
   ↓
Risk Scoring Engine
   ↓
Decision (APPROVE / REVIEW / BLOCK)
   ↓
Store in Database
   ↓
Update Dashboard UI
```

---

## ✨ Features

* 🔐 Secure JWT Authentication (Role-based access)
* 📊 Real-time fraud analytics dashboard
* 🤖 Machine Learning prediction engine
* 🧾 Transaction audit logs
* 👮 Admin override controls
* 📈 Interactive charts & metrics visualization
* ⚡ Low-latency API inference system

---

## 🧰 Technology Stack

### 🎨 Frontend

* React (Vite)
* Tailwind CSS
* Axios
* Recharts

### ⚙️ Backend

* FastAPI
* Python
* SQLAlchemy
* Pydantic
* JWT Authentication

### 🤖 Machine Learning

* Scikit-learn
* XGBoost / Random Forest
* Pandas
* NumPy

### 🗄️ Database

* SQLite

### 🛠️ Tools

* Docker (optional)
* Postman
* Git & GitHub

---

## 📦 Installation Guide

### ⚙️ Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 🎨 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 👤 Demo Credentials

### Admin

```
Username: admin
Password: admin123
```

### User

```
Username: user
Password: user123
```

---

## ⚠️ Limitations

* Uses synthetic dataset (not real banking data)
* SQLite not suitable for large-scale production
* ML model is static (no continuous retraining)
* No distributed system support
* Limited concurrency handling

---

## 📸 UI Preview

* `/assets/img/signin.png`
* `/assets/img/dashboard.png`
* `/assets/img/pred1.png`

---

## 👤 Credits & License

- **Built by:** Athrav Khandelwal
- **License:** MIT License

---
