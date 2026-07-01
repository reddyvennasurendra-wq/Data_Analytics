# =====================================================
# Website Traffic Sources Dashboard
# Data Analytics Internship Project
# Intern: Venna Surendra Reddy
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Website Traffic Sources",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Website Traffic Sources Dashboard")
st.markdown("### Data Analytics Internship Project")

# ----------------------------------------------------
# Generate Sample Dataset
# ----------------------------------------------------

@st.cache_data
def load_data():

    np.random.seed(42)

    n = 500

    dates = pd.date_range("2025-01-01", periods=n)

    traffic = np.random.choice(
        [
            "Google",
            "Direct",
            "Facebook",
            "Instagram",
            "LinkedIn",
            "Twitter",
            "YouTube"
        ],
        n
    )

    visitors = np.random.randint(100, 5000, n)

    device = np.random.choice(
        [
            "Desktop",
            "Mobile",
            "Tablet"
        ],
        n
    )

    browser = np.random.choice(
        [
            "Chrome",
            "Edge",
            "Firefox",
            "Safari"
        ],
        n
    )

    country = np.random.choice(
        [
            "India",
            "USA",
            "UK",
            "Canada",
            "Australia"
        ],
        n
    )

    bounce = np.random.randint(20, 80, n)

    duration = np.random.randint(1, 15, n)

    df = pd.DataFrame({

        "Date": dates,
        "Traffic Source": traffic,
        "Visitors": visitors,
        "Device": device,
        "Browser": browser,
        "Country": country,
        "Bounce Rate": bounce,
        "Session Duration": duration

    })

    return df


df = load_data()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------

st.sidebar.header("Filters")

source = st.sidebar.selectbox(
    "Traffic Source",
    ["All"] + sorted(df["Traffic Source"].unique())
)

device = st.sidebar.selectbox(
    "Device",
    ["All"] + sorted(df["Device"].unique())
)

if source != "All":
    df = df[df["Traffic Source"] == source]

if device != "All":
    df = df[df["Device"] == device]

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

total_visitors = df["Visitors"].sum()

average_visitors = df["Visitors"].mean()

average_bounce = df["Bounce Rate"].mean()

average_duration = df["Session Duration"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Visitors",
    f"{total_visitors:,}"
)

c2.metric(
    "Average Visitors",
    f"{average_visitors:.0f}"
)

c3.metric(
    "Average Bounce %",
    f"{average_bounce:.1f}%"
)

c4.metric(
    "Avg Session",
    f"{average_duration:.1f} min"
)

st.divider()

# ----------------------------------------------------
# Dataset Preview
# ----------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Traffic Source Distribution
# ----------------------------------------------------

st.subheader("Traffic Source Distribution")

traffic_count = df["Traffic Source"].value_counts()

fig, ax = plt.subplots(figsize=(6,5))

traffic_count.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

st.divider()

# ----------------------------------------------------
# Daily Visitors Trend
# ----------------------------------------------------

st.subheader("Daily Visitors Trend")

daily = df.groupby("Date")["Visitors"].sum()

fig, ax = plt.subplots(figsize=(10,4))

daily.plot(ax=ax)

ax.set_ylabel("Visitors")

st.pyplot(fig)

st.divider()

# ----------------------------------------------------
# Device Analysis
# ----------------------------------------------------

st.subheader("Visitors by Device")

device_count = df.groupby("Device")["Visitors"].sum()

fig, ax = plt.subplots(figsize=(6,4))

device_count.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Visitors")

st.pyplot(fig)

st.divider()
# ----------------------------------------------------
# Browser Analysis
# ----------------------------------------------------

st.subheader("🌐 Browser Analysis")

browser_visitors = df.groupby("Browser")["Visitors"].sum()

fig, ax = plt.subplots(figsize=(7,4))

browser_visitors.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Visitors")
ax.set_xlabel("Browser")

st.pyplot(fig)

st.divider()

# ----------------------------------------------------
# Country-wise Visitors
# ----------------------------------------------------

st.subheader("🌍 Country-wise Visitors")

country_visitors = df.groupby("Country")["Visitors"].sum()

fig, ax = plt.subplots(figsize=(7,4))

country_visitors.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Visitors")
ax.set_xlabel("Country")

st.pyplot(fig)

st.divider()

# ----------------------------------------------------
# Bounce Rate Analysis
# ----------------------------------------------------

st.subheader("📉 Bounce Rate Analysis")

fig, ax = plt.subplots(figsize=(8,4))

ax.hist(
    df["Bounce Rate"],
    bins=10
)

ax.set_xlabel("Bounce Rate (%)")
ax.set_ylabel("Frequency")

st.pyplot(fig)

st.divider()

# ----------------------------------------------------
# Session Duration Analysis
# ----------------------------------------------------

st.subheader("⏱ Session Duration")

fig, ax = plt.subplots(figsize=(8,4))

ax.hist(
    df["Session Duration"],
    bins=10
)

ax.set_xlabel("Session Duration (Minutes)")
ax.set_ylabel("Frequency")

st.pyplot(fig)

st.divider()

# ----------------------------------------------------
# Top 5 Traffic Sources
# ----------------------------------------------------

st.subheader("🏆 Top Traffic Sources")

top_sources = (
    df.groupby("Traffic Source")["Visitors"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
      .reset_index()
)

st.dataframe(
    top_sources,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Summary Statistics
# ----------------------------------------------------

st.subheader("📊 Summary Statistics")

summary = df[["Visitors","Bounce Rate","Session Duration"]].describe()

st.dataframe(
    summary,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Business Insights
# ----------------------------------------------------

st.subheader("💡 Business Insights")

best_source = (
    df.groupby("Traffic Source")["Visitors"]
      .sum()
      .idxmax()
)

best_country = (
    df.groupby("Country")["Visitors"]
      .sum()
      .idxmax()
)

best_browser = (
    df.groupby("Browser")["Visitors"]
      .sum()
      .idxmax()
)

best_device = (
    df.groupby("Device")["Visitors"]
      .sum()
      .idxmax()
)

highest_day = df.loc[df["Visitors"].idxmax(), "Date"]

st.success(f"""

### Website Traffic Insights

- 🌐 Total Visitors : **{total_visitors:,}**

- 🏆 Best Traffic Source : **{best_source}**

- 🌍 Highest Visitor Country : **{best_country}**

- 💻 Most Used Device : **{best_device}**

- 🌐 Most Used Browser : **{best_browser}**

- 📅 Highest Traffic Day : **{highest_day.strftime('%d-%m-%Y')}**

- 📉 Average Bounce Rate : **{average_bounce:.1f}%**

- ⏱ Average Session Duration : **{average_duration:.1f} Minutes**

""")

st.divider()

# ----------------------------------------------------
# Download Dataset
# ----------------------------------------------------

st.subheader("📥 Download Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="website_traffic_data.csv",
    mime="text/csv"
)

st.divider()

# ----------------------------------------------------
# Project Information
# ----------------------------------------------------

st.markdown("---")

st.markdown("""
## 👨‍💻 Project Information

**Project Name:** Website Traffic Sources

**Intern Name:** Venna Surendra Reddy

**Intern ID:** CTIS9822

**Domain:** Data Analytics

**Duration:** 8 Weeks

**Tools Used**

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

---

### Project Scope

This dashboard analyzes website traffic using different dimensions such as traffic source, browser, device, country, bounce rate, and session duration. It helps identify user behavior and provides business insights for improving website performance.

---

© 2026 Data Analytics Internship Project
""")