import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Expense Analytics", layout="wide")

st.title("💰 Personal Expense Analytics Dashboard")

# Dataset URL
url = "https://raw.githubusercontent.com/plotly/datasets/master/tips.csv"

# Load dataset
df = pd.read_csv(url)

# Rename columns for expense project
df = df.rename(columns={
    "tip": "Amount",
    "day": "Category",
    "time": "Time",
    "size": "People"
})

st.success("Dataset Loaded Successfully!")

st.subheader("Dataset Preview")
st.dataframe(df)

# Sidebar Filter
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

if category != "All":
    df = df[df["Category"] == category]

# KPIs
total = df["Amount"].sum()
average = df["Amount"].mean()
highest = df["Amount"].max()
lowest = df["Amount"].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Expense", f"${total:.2f}")
c2.metric("Average", f"${average:.2f}")
c3.metric("Highest", f"${highest:.2f}")
c4.metric("Lowest", f"${lowest:.2f}")

st.divider()

# Category Analysis
st.subheader("Category-wise Expense")

category_data = df.groupby("Category")["Amount"].sum()

fig, ax = plt.subplots(figsize=(7,4))
category_data.plot(kind="bar", ax=ax)
ax.set_ylabel("Expense")
st.pyplot(fig)

# Pie Chart
st.subheader("Expense Distribution")

fig2, ax2 = plt.subplots(figsize=(6,6))
category_data.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# Histogram
st.subheader("Expense Distribution Histogram")

fig3, ax3 = plt.subplots(figsize=(7,4))
ax3.hist(df["Amount"], bins=15)
ax3.set_xlabel("Expense")
ax3.set_ylabel("Frequency")
st.pyplot(fig3)

# Top Expenses
st.subheader("Top 10 Expenses")

top = df.sort_values("Amount", ascending=False).head(10)
st.dataframe(top)

# Summary Statistics
st.subheader("Summary Statistics")
st.write(df["Amount"].describe())

# Download Button
csv = df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)