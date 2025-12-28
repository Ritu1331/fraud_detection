import streamlit as st
import pandas as pd
import joblib


model = joblib.load("fraud_detection_pipeline.pkl")

st.title("Fraud Detection Prediction App")


st.markdown("Please enter the transaction details and use the predict button")


st.divider()

transaction_type = st.selectbox("Transaction Type", options=["PAYMENT", "TRANSFER", "CASH_OUT","DEPOSIT" ,"DEBIT", "CASH_IN"])

amount = st.number_input("Amount", min_value=0.0, step=0.01 , value = 1000.0)

oldbalanceOrg = st.number_input("Old Balance of Origin Account(sender)", min_value=0.0, step=0.01, value = 10000.0)

newbalanceOrig = oldbalanceOrg - amount
if newbalanceOrig < 0:
    newbalanceOrig = 0.0

st.number_input(
    "New Balance of Origin Account (sender)",
    value=newbalanceOrig,
    disabled=True
)

oldbalanceDest = st.number_input(
    "Old Balance of Destination Account (receiver)",
    min_value=0.0,
    step=0.01,
    value=5000.0
)

newbalanceDest = oldbalanceDest + amount

st.number_input(
    "New Balance of Destination Account (receiver)",
    value=newbalanceDest,
    disabled=True
)


if st.button("Predict"):
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    prediction = model.predict(input_data)[0]
    st.subheader(f"Prediction : '{int(prediction)}'")


    if prediction == 1:
        st.error("The transaction is predicted to be FRAUDULENT.")
    else:
        st.success("The transaction is predicted to be LEGITIMATE.")
