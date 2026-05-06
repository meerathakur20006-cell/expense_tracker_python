import streamlit as st
import pandas as pd
from db_config import get_connection

conn = get_connection()

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Personal Expense Tracker")

# -------- Sidebar (Dashboard Controls Only) --------

st.sidebar.title("Dashboard")

menu = st.sidebar.radio(
    "Dashboard Controls",
    ["Home", "Summary", "Analysis", "Reports"]
)

# -------- HOME PAGE --------

if menu == "Home":

    st.header("Welcome to your Expense Tracker")

    st.write("""
    This application helps you manage your daily expenses easily.

    Features:
    - Add new expenses
    - View all transactions
    - Edit records
    - Delete unwanted entries
    - Visualize spending through charts
    """)

    st.write("### Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    # -------- ADD EXPENSE --------

    with col1:
        st.markdown("### ➕ Add")

        date = st.date_input("Date")

        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            value=None,
            placeholder="Enter amount"
        )

        description = st.text_input("Description")

        if st.button("Add Expense"):

            if amount is None:
                st.warning("Please enter amount")

            else:
                cursor = conn.cursor()

                query = """
                INSERT INTO expenses (date, category, amount, description)
                VALUES (%s,%s,%s,%s)
                """

                cursor.execute(query, (date, category, amount, description))
                conn.commit()

                st.success("Expense Added")

    # -------- VIEW EXPENSE --------

    with col2:
        st.markdown("### 📋 View")

        if st.button("Show Expenses"):

            query = "SELECT * FROM expenses"
            df = pd.read_sql(query, conn)

            st.dataframe(df)

    # -------- EDIT EXPENSE --------

    with col3:
        st.markdown("### ✏ Edit")

        edit_id = st.number_input("Expense ID to Edit", step=1)

        new_amount = st.number_input(
            "New Amount",
            min_value=0.0,
            value=None,
            placeholder="Enter new amount"
        )

        if st.button("Update Expense"):

            cursor = conn.cursor()

            query = "UPDATE expenses SET amount=%s WHERE id=%s"

            cursor.execute(query, (new_amount, edit_id))
            conn.commit()

            st.success("Expense Updated")

    # -------- DELETE EXPENSE --------

    with col4:
        st.markdown("### ❌ Delete")

        delete_id = st.number_input("Expense ID to Delete", step=1)

        if st.button("Delete Expense"):

            cursor = conn.cursor()

            query = "DELETE FROM expenses WHERE id=%s"

            cursor.execute(query, (delete_id,))
            conn.commit()

            st.warning("Expense Deleted")


# -------- SUMMARY --------

elif menu == "Summary":

    st.header("Expense Summary")

    query = "SELECT * FROM expenses"
    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No expenses available")

    else:

        total = df["amount"].sum()

        col1, col2 = st.columns(2)

        col1.metric("Total Expenses", f"₹ {total}")
        col2.metric("Number of Transactions", len(df))

        # ⭐ Top spending category
        top_category = df.groupby("category")["amount"].sum().idxmax()

        st.write(f"**Top Spending Category:** {top_category}")


# -------- ANALYSIS --------

elif menu == "Analysis":

    st.header("Category Analysis")

    query = "SELECT * FROM expenses"
    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No expenses available")

    else:

        # ⭐ Category Filter
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(df["category"].unique())
        )

        if category_filter != "All":
            df = df[df["category"] == category_filter]

        category_data = df.groupby("category")["amount"].sum()

        st.bar_chart(category_data)

        # ⭐ Monthly analysis
        df["date"] = pd.to_datetime(df["date"])

        df["month"] = df["date"].dt.to_period("M")

        monthly = df.groupby("month")["amount"].sum()

        st.write("### Monthly Spending Trend")

        st.line_chart(monthly)


# -------- REPORTS --------

elif menu == "Reports":

    st.header("Expense Reports")

    query = "SELECT * FROM expenses"
    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No expenses to export")

    else:

        st.dataframe(df)

        st.download_button(
            label="Download Report (CSV)",
            data=df.to_csv(index=False),
            file_name="expense_report.csv",
            mime="text/csv"
        )