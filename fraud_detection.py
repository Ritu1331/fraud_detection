import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 20px;
}

.badge-high {
    background: #78350f;
    color: #facc15;
    padding: 10px;
    border-radius: 12px;
    font-weight: bold;
}

.success-box {
    background: #064e3b;
    padding: 15px;
    border-radius: 14px;
    color: #6ee7b7;
    font-weight: bold;
}

.error-box {
    background: #7f1d1d;
    padding: 15px;
    border-radius: 14px;
    color: #fecaca;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load("fraud_detection_pipeline.pkl")

# ---------------- HEADER ----------------
st.markdown('<div class="title">🛡️ Fraud Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered transaction risk analysis</div>', unsafe_allow_html=True)

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💳 Transaction Details")

col1, col2 = st.columns(2)

with col1:
    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT", "DEBIT", "CASH_IN"]
    )
    amount = st.number_input("Amount", min_value=0.0, step=100.0, value=1000.0)

with col2:
    oldbalanceOrg = st.number_input("Sender Balance", min_value=0.0, step=500.0, value=10000.0)
    oldbalanceDest = st.number_input("Receiver Balance", min_value=0.0, step=500.0, value=0.0)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- AUTO BALANCE LOGIC ----------------
if transaction_type in ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT"]:
    newbalanceOrig = max(oldbalanceOrg - amount, 0)
else:
    newbalanceOrig = oldbalanceOrg + amount

if transaction_type in ["TRANSFER", "CASH_IN", "DEPOSIT"]:
    newbalanceDest = oldbalanceDest + amount
else:
    newbalanceDest = oldbalanceDest

# ---------------- BALANCE CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Auto-Calculated Balances")

b1, b2 = st.columns(2)
b1.metric("New Sender Balance", f"₹ {newbalanceOrig:,.2f}")
b2.metric("New Receiver Balance", f"₹ {newbalanceDest:,.2f}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RISK ALERT ----------------
if transaction_type in ["TRANSFER", "CASH_OUT"] and amount > 0.9 * oldbalanceOrg:
    st.markdown(
        '<div class="badge-high">⚠️ High-risk transaction: Almost entire balance moved</div>',
        unsafe_allow_html=True
    )

# ---------------- PREDICTION ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔮 Fraud Prediction")

if st.button("🚀 Analyze Transaction"):
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    fraud_prob = model.predict_proba(input_data)[0][1]
    prediction = int(fraud_prob > 0.5)

    st.write("### 📈 Fraud Probability")
    st.progress(min(fraud_prob, 1.0))
    st.write(f"**{fraud_prob*100:.2f}% risk score**")

    if prediction == 1:
        st.markdown(
            '<div class="error-box">🚨 FRAUD DETECTED<br>Suspicious transaction pattern identified</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="success-box">✅ TRANSACTION IS LEGITIMATE<br>No strong fraud indicators</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


