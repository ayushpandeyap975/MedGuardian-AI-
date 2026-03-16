import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

st.title("🏥 Digital Care Coordinator AI Dashboard")

# SIDEBAR FILTER
st.sidebar.header("🔍 Filters")

severity_filter = st.sidebar.multiselect(
    "Filter by Severity",
    options=df["severity"].unique(),
    default=df["severity"].unique()
)

filtered_df = df[df["severity"].isin(severity_filter)]

# SUMMARY METRICS
total_patients = len(filtered_df)
critical_cases = len(filtered_df[filtered_df["severity"] == "CRITICAL"])
high_risk = len(filtered_df[filtered_df["severity"] == "HIGH"])
medium_risk = len(filtered_df[filtered_df["severity"] == "MEDIUM"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", total_patients)
col2.metric("Critical 🔴", critical_cases)
col3.metric("High Risk 🟠", high_risk)
col4.metric("Medium Risk 🟡", medium_risk)

# BAR CHART
st.subheader("📊 Risk Severity Distribution")

severity_counts = filtered_df["severity"].value_counts()

fig, ax = plt.subplots()
severity_counts.plot(kind="bar", ax=ax)
st.pyplot(fig)

# PIE CHART
st.subheader("📊 Patient Risk Distribution")

fig2, ax2 = plt.subplots()

ax2.pie(
    severity_counts,
    labels=severity_counts.index,
    autopct="%1.1f%%"
)

st.pyplot(fig2)

# PATIENT SELECTOR
patient = st.selectbox(
    "Select Patient",
    filtered_df["patient_id"],
    key="patient_selector"
)

row = filtered_df[filtered_df["patient_id"] == patient].iloc[0]

# SEVERITY FUNCTION
def severity_badge(severity):
    if severity == "CRITICAL":
        st.error("🔴 CRITICAL")
    elif severity == "HIGH":
        st.warning("🟠 HIGH")
    elif severity == "MEDIUM":
        st.info("🟡 MEDIUM")
    else:
        st.success("🟢 LOW")

# PATIENT DETAILS
st.subheader("🧾 Patient Analysis")

st.markdown("### ⚠ Issues")
st.write(row["issues"])

st.markdown("### 📊 Severity")
severity_badge(row["severity"])

st.markdown("### ⚡ Recommended Actions")
st.write(row["actions"])

st.markdown("### 🧠 Coordination Insight")
st.write(row["coordination_explanation"])

st.markdown("### 🚨 Emergency Alert")
st.error(row["emergency_alert"])