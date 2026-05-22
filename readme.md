# 🛡️ FraudShield  
### AI-Powered Credit Card Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Node](https://img.shields.io/badge/Node.js-18+-green?logo=node.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Open Source](https://img.shields.io/badge/Open--Source-Yes-orange)

---

## 🚀 Overview

FraudShield is a real-time AI-powered fraud detection system that analyzes credit card transactions using machine learning and provides instant risk scoring through a full-stack dashboard.

> It simulates how real fintech fraud detection systems evaluate and block suspicious transactions.

---

## 🧠 Problem Statement

Credit card fraud causes massive financial losses globally.

FraudShield demonstrates how AI can:
- Detect suspicious patterns
- Score transaction risk in real time
- Automate fraud decisions (APPROVE / REVIEW / BLOCK)

---

## 🏗️ System Architecture

### 🔷 High-Level Flow

![Architecture](./assets/imgs/architecture.png)

---

### 🔷 Architecture Breakdown

| Layer        | Responsibility                     |
| ------------ | ---------------------------------- |
| 🎨 Frontend  | User dashboard + transaction input |
| ⚙️ Backend   | API + business logic               |
| 🤖 ML Model  | Fraud prediction engine            |
| 🗄️ Database | Stores users + transactions        |

---

## ✨ Features

✔ Secure JWT Authentication
✔ Role-based Access (Admin/User)
✔ Real-time Fraud Prediction
✔ ML-based Risk Scoring
✔ Transaction Audit Logs
✔ Interactive Dashboard Charts
✔ Admin Override Controls

---

## 📦 Installation

### ⚙️ Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 🎨 Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 👤 Demo Credentials

| Role  | Username | Password |
| ----- | -------- | -------- |
| Admin | admin    | admin123 |
| User  | user     | user123  |

---

## 📸 UI PREVIEW


### 🔐 Login Page

![Login](./assets/imgs/signin.png)

### 📊 Dashboard

![Dashboard](./assets/imgs/dashboard.png)

### 📈 Prediction View

![Prediction](./assets/imgs/pred1.png)

---

## ⚠️ Limitations

* Synthetic dataset (not real banking data)
* SQLite not production-grade
* No real-time model training
* Basic concurrency handling

---

## 📜 License

MIT License © 2026 FraudShield

---

## ❤️ Footer

Built with ❤️ using AI + Full Stack Engineering

````

---