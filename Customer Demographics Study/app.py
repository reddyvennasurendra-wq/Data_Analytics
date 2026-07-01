# ==========================================================
# Customer Demographics Dashboard
# Data Analytics Internship Project
# Author: Venna Surendra Reddy
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Customer Demographics Dashboard",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Demographics Dashboard")
st.markdown("Analyze customer demographics using interactive charts and KPIs.")

# ----------------------------
# Generate Sample Dataset
# ----------------------------

@st.cache_data
def load_data():

    np.random.seed(42)

    n = 500

    names = [f"Customer {i}" for i in range(1, n+1)]

    age = np.random.randint(18, 65, n)

    gender = np.random.choice(
        ["Male", "Female"],
        n
    )

    city = np.random.choice(
        ["Hyderabad","Bangalore","Chennai","Mumbai","Delhi"],
        n
    )

    occupation = np.random.choice(
        ["Student","Engineer","Doctor","Teacher","Business"],
        n
    )

    education = np.random.choice(
        ["High School","Bachelor","Master","PhD"],
        n
    )

    income = np.random.randint(
        20000,
        120000,
        n
    )

    df = pd.DataFrame({

        "Customer ID": range(1,n+1),
        "Name": names,
        "Age": age,
        "Gender": gender,
        "City": city,
        "Occupation": occupation,
        "Education": education,
        "Income": income

    })

    return df


df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("Filters")

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].unique())
)

city = st.sidebar.selectbox(
    "City",
    ["All"] + sorted(df["City"].unique())
)

if gender != "All":
    df = df[df["Gender"] == gender]

if city != "All":
    df = df[df["City"] == city]

# ----------------------------
# KPI Cards
# ----------------------------

total_customers = len(df)

average_age = df["Age"].mean()

average_income = df["Income"].mean()

highest_income = df["Income"].max()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Customers",
    total_customers
)

c2.metric(
    "Average Age",
    f"{average_age:.1f}"
)

c3.metric(
    "Average Income",
    f"₹{average_income:,.0f}"
)

c4.metric(
    "Highest Income",
    f"₹{highest_income:,.0f}"
)

st.divider()

# ----------------------------
# Dataset Preview
# ----------------------------

st.subheader("Customer Dataset")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# ----------------------------
# Gender Distribution
# ----------------------------

st.subheader("Gender Distribution")

gender_count = df["Gender"].value_counts()

fig, ax = plt.subplots(figsize=(5,4))

gender_count.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

# ----------------------------
# Age Distribution
# ----------------------------

st.subheader("Age Distribution")

fig, ax = plt.subplots(figsize=(7,4))

ax.hist(
    df["Age"],
    bins=10
)

ax.set_xlabel("Age")
ax.set_ylabel("Customers")

st.pyplot(fig)

st.divider()

# ----------------------------
# City-wise Customers
# ----------------------------

st.subheader("Customers by City")

city_count = df["City"].value_counts()

fig, ax = plt.subplots(figsize=(7,4))

city_count.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Customers")

st.pyplot(fig)

st.divider()
# ----------------------------
# Occupation Analysis
# ----------------------------

st.subheader("Occupation Distribution")

occupation_count = df["Occupation"].value_counts()

fig, ax = plt.subplots(figsize=(7,4))

occupation_count.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Customers")
ax.set_xlabel("Occupation")

st.pyplot(fig)

st.divider()

# ----------------------------
# Education Analysis
# ----------------------------

st.subheader("Education Distribution")

education_count = df["Education"].value_counts()

fig, ax = plt.subplots(figsize=(7,4))

education_count.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Customers")
ax.set_xlabel("Education")

st.pyplot(fig)

st.divider()

# ----------------------------
# Average Income by City
# ----------------------------

st.subheader("Average Income by City")

income_city = df.groupby("City")["Income"].mean()

fig, ax = plt.subplots(figsize=(7,4))

income_city.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Average Income (₹)")
ax.set_xlabel("City")

st.pyplot(fig)

st.divider()

# ----------------------------
# Customer Segmentation
# ----------------------------

st.subheader("Customer Segmentation")

def segment(income):
    if income < 40000:
        return "Low Income"
    elif income < 80000:
        return "Middle Income"
    else:
        return "High Income"

df["Segment"] = df["Income"].apply(segment)

segment_count = df["Segment"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))

segment_count.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

st.divider()

# ----------------------------
# Top 10 Highest Income Customers
# ----------------------------

st.subheader("Top 10 Highest Income Customers")

top10 = df.sort_values(
    by="Income",
    ascending=False
).head(10)

st.dataframe(
    top10,
    use_container_width=True
)

st.divider()

# ----------------------------
# Summary Statistics
# ----------------------------

st.subheader("Summary Statistics")

st.dataframe(
    df.describe(),
    use_container_width=True
)

st.divider()

# ----------------------------
# Business Insights
# ----------------------------

st.subheader("Business Insights")

highest_city = income_city.idxmax()

most_common_occupation = occupation_count.idxmax()

most_common_education = education_count.idxmax()

highest_income = df["Income"].max()

st.success(f"""

### 📊 Key Insights

- 👥 Total Customers : **{len(df)}**

- 🎂 Average Age : **{df['Age'].mean():.1f} Years**

- 💰 Average Income : **₹{df['Income'].mean():,.0f}**

- 🏙 Highest Income City : **{highest_city}**

- 💼 Most Common Occupation : **{most_common_occupation}**

- 🎓 Most Common Education : **{most_common_education}**

- 💵 Highest Income : **₹{highest_income:,.0f}**

""")

st.divider()

# ----------------------------
# Download Dataset
# ----------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="customer_demographics.csv",
    mime="text/csv"
)

st.divider()

# ----------------------------
# Footer
# ----------------------------

st.markdown("---")

st.markdown(
    """
    ### 👨‍💻 Project Information

    **Project:** Customer Demographics Study

    **Intern Name:** Venna Surendra Reddy

    **Intern ID:** CTIS9822

    **Domain:** Data Analytics

    **Duration:** 8 Weeks

    **Tools Used:** Python, Pandas, NumPy, Matplotlib, Streamlit
    """
)