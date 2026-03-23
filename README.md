## FraudDetect — Credit Card Fraud Detection

A machine learning web application that detects fraudulent credit card 
transactions in real time. Built with XGBoost, trained on 100,000 synthetic 
transactions, and deployed with Streamlit.

### Live Demo
🔗 [FraudDetect on Streamlit](https://credit-card-fraud-detection-ces3hjzcqwevx5hrwo77pt.streamlit.app/)

### Overview
Credit card fraud costs billions globally every year. This project builds 
a complete ML pipeline — from data generation and exploratory analysis to 
model training, evaluation and live deployment — to detect fraud instantly 
from transaction details.

### Features
- 🔍 **Real-time prediction** — enter any transaction and get an instant verdict
- 📊 **Model comparison dashboard** — all 6 algorithms compared across 5 metrics
- 🎯 **Risk scoring** — fraud probability % with visual gauge and risk level badge
- 💡 **Explainability** — shows exactly which features triggered the fraud alert
- 🛡️ **Synthetic dataset** — no real customer data, fully privacy safe

### Results

| Model | Accuracy | F1 Score | ROC-AUC |
|---|---|---|---|
| **XGBoost** ✅ | 99.84% | 0.9612 | 0.9995 |
| Random Forest | 99.79% | 0.9484 | 0.9995 |
| KNN | 99.49% | 0.8806 | 0.9828 |
| Decision Tree | 99.43% | 0.8703 | 0.9739 |
| Logistic Regression | 98.53% | 0.7259 | 0.9983 |
| Naive Bayes | 97.63% | 0.6096 | 0.9919 |

### Tech Stack
Python · XGBoost · Scikit-learn · SMOTE · Streamlit · Plotly · Pandas

### Key Insights
- Online transactions account for **40% of XGBoost's fraud decisions**
- Distance from home shows a **6.7x difference** between fraud and normal
- Transaction velocity is **3x higher** for fraudulent cards
- No single feature catches everything — ML combines weak signals into 
  strong predictions

### Author
Built by [Arjuman Sultana](https://github.com/arjumannsultana)
