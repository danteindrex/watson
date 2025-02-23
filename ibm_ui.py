import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt
import numpy as np

# Set wide layout for full-screen effect
st.set_page_config(layout="wide")

# --- Custom Navigation Bar using streamlit-option-menu ---
selected = option_menu(
    menu_title=None,
    options=["Home", "CRM Summary", "Supply Chain Summary", "Financial Summary", "Process Dashboard", "Settings"],
    icons=["house", "person-lines-fill", "truck", "currency-dollar", "speedometer", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f4f7f6"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
            "padding": "12px 20px"
        },
        "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
    }
)

# --- Define page functions ---
def home_page():
    st.title("Home Page")
    st.write("Welcome to the Process Management App!")
    with st.form("login_form"):
        position = st.text_input("Position in the Company", placeholder="e.g., Manager")
        name = st.text_input("Name", placeholder="Enter your full name")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.success(f"Welcome, {name}! You are logged in as {position}.")

def crm_summary():
    st.title("CRM Summary")
    st.write("This page displays CRM metrics and insights.")
    # Sample CRM data
    data = {
        "Customer": ["Alice", "Bob", "Charlie", "Diana"],
        "Sales": [1200, 1500, 1100, 1800],
        "Satisfaction": [4.5, 4.7, 4.0, 4.8]
    }
    df = pd.DataFrame(data)
    st.table(df)
    # Bar chart for sales
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Customer:N", title="Customer"),
        y=alt.Y("Sales:Q", title="Sales ($)")
    ).properties(width=600, height=300, title="Sales by Customer")
    st.altair_chart(chart, use_container_width=True)

def supply_chain_summary():
    st.title("Supply Chain Summary")
    st.write("Overview of supply chain performance and KPIs.")
    # Simulated on-time delivery data for 6 months
    months = pd.date_range(start="2024-01-01", periods=6, freq="M").strftime("%b %Y")
    on_time = np.random.randint(80, 100, size=6)
    df = pd.DataFrame({"Month": months, "On-Time Delivery (%)": on_time})
    st.line_chart(df.set_index("Month"))
    st.write("The chart above shows the on-time delivery performance over the last six months.")

def financial_summary():
    st.title("Financial Summary")
    st.write("Financial performance metrics and charts.")
    # Simulated financial data for 12 months
    months = pd.date_range(start="2024-01-01", periods=12, freq="M").strftime("%b %Y")
    revenue = np.random.randint(100000, 200000, size=12)
    expenses = np.random.randint(50000, 150000, size=12)
    profit = revenue - expenses
    df = pd.DataFrame({
        "Month": months,
        "Revenue": revenue,
        "Expenses": expenses,
        "Profit": profit
    })
    # Line chart for Revenue vs. Expenses
    line_chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Month:N", title="Month"),
        y=alt.Y("value:Q", title="Amount ($)"),
        color="variable:N"
    ).transform_fold(
        ["Revenue", "Expenses"],
        as_=["variable", "value"]
    ).properties(width=700, height=300, title="Monthly Revenue vs. Expenses")
    st.altair_chart(line_chart, use_container_width=True)
    st.write("Key Financial Metrics:")
    st.dataframe(df.set_index("Month"))

def process_dashboard():
    st.title("Process Dashboard")
    st.write("Monitor key process metrics across the organization.")
    # Simulated KPI data
    kpis = {
        "Process": ["Order Fulfillment", "Invoice Processing", "Customer Support"],
        "Efficiency (%)": [90, 85, 92],
        "Cycle Time (days)": [2, 5, 1]
    }
    df = pd.DataFrame(kpis)
    st.table(df)
    st.metric(label="Average Order Fulfillment Efficiency", value="90%")
    st.metric(label="Average Invoice Processing Cycle", value="5 days")

def settings_page():
    st.title("Settings")
    st.write("Manage your app settings and preferences.")
    with st.form("settings_form"):
        theme = st.selectbox("Select Theme", ["Light", "Dark"])
        notifications = st.checkbox("Enable Notifications", value=True)
        save = st.form_submit_button("Save Settings")
        if save:
            st.success("Settings updated successfully!")

# --- Map selected menu option to the corresponding page function ---
pages = {
    "Home": home_page,
    "CRM Summary": crm_summary,
    "Supply Chain Summary": supply_chain_summary,
    "Financial Summary": financial_summary,
    "Process Dashboard": process_dashboard,
    "Settings": settings_page
}

# Render the selected page
pages[selected]()
