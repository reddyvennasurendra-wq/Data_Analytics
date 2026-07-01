import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Sales Trend Visualization", layout="wide")

st.title("📈 Sales Trend Visualization Dashboard")

# -----------------------------
# Load Dataset from Public URL
# -----------------------------
DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

try:
    df = pd.read_csv(DATA_URL)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -----------------------------
# Convert Dataset for Sales Analysis
# -----------------------------
df.rename(columns={
    "total_bill": "Sales",
    "day": "Day",
    "time": "Time",
    "sex": "Gender",
    "smoker": "Customer Type",
    "size": "Quantity"
}, inplace=True)

st.success("Dataset Loaded Successfully!")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

days = ["All"] + sorted(df["Day"].unique().tolist())

selected_day = st.sidebar.selectbox(
    "Select Day",
    days
)

if selected_day != "All":
    df = df[df["Day"] == selected_day]

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(df)

# -----------------------------
# KPI Cards
# -----------------------------
total_sales = df["Sales"].sum()
avg_sales = df["Sales"].mean()
highest_sale = df["Sales"].max()
lowest_sale = df["Sales"].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"${total_sales:.2f}")
c2.metric("Average Sale", f"${avg_sales:.2f}")
c3.metric("Highest Sale", f"${highest_sale:.2f}")
c4.metric("Lowest Sale", f"${lowest_sale:.2f}")

st.divider()

# -----------------------------
# Sales by Day
# -----------------------------
st.subheader("📊 Sales by Day")

sales_day = df.groupby("Day")["Sales"].sum()

fig1, ax1 = plt.subplots(figsize=(8,4))
sales_day.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Day")
ax1.set_ylabel("Sales")
st.pyplot(fig1)

# -----------------------------
# Sales Distribution
# -----------------------------
st.subheader("🥧 Sales Distribution")

fig2, ax2 = plt.subplots(figsize=(6,6))
sales_day.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# -----------------------------
# Histogram
# -----------------------------
st.subheader("📈 Sales Distribution Histogram")

fig3, ax3 = plt.subplots(figsize=(8,4))
ax3.hist(df["Sales"], bins=20)
ax3.set_xlabel("Sales")
ax3.set_ylabel("Frequency")
st.pyplot(fig3)

# -----------------------------
# Customer Type Analysis
# -----------------------------
st.subheader("🚬 Sales by Customer Type")

customer = df.groupby("Customer Type")["Sales"].sum()

fig4, ax4 = plt.subplots(figsize=(6,4))
customer.plot(kind="bar", ax=ax4)
ax4.set_ylabel("Sales")
st.pyplot(fig4)

# -----------------------------
# Top Transactions
# -----------------------------
st.subheader("🏆 Top 10 Sales")

top = df.sort_values("Sales", ascending=False).head(10)

st.dataframe(top)

# -----------------------------
# Summary Statistics
# -----------------------------
st.subheader("📋 Summary Statistics")

st.write(df["Sales"].describe())

# -----------------------------
# Business Insights
# -----------------------------
st.subheader("💡 Business Insights")

highest_day = sales_day.idxmax()

st.success(f"""
• Highest Sales Day: **{highest_day}**

• Total Sales: **${total_sales:.2f}**

• Average Sales: **${avg_sales:.2f}**

• Highest Transaction: **${highest_sale:.2f}**
""")

# -----------------------------
# Download CSV
# -----------------------------
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "sales_data.csv",
    "text/csv"
)