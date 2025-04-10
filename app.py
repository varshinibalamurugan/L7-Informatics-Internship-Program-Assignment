# streamlit_app.py
import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = "expenses.db"

# DB Setup
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT,
        category TEXT,
        amount REAL
    )''')
    conn.commit()
    conn.close()

# DB Operations
def add_expense(date, category, amount):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, category, amount) VALUES (?, LOWER(?), ?)", (date, category, amount))
    conn.commit()
    conn.close()

def set_budget(month, category, amount):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Delete previous entry for same month/category to avoid duplicates
    cur.execute("DELETE FROM budgets WHERE month = ? AND LOWER(category) = LOWER(?)", (month, category))
    # Insert new budget value
    cur.execute("INSERT INTO budgets (month, category, amount) VALUES (?, LOWER(?), ?)", (month, category, amount))
    conn.commit()
    conn.close()

def get_monthly_summary(month):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY category", (month,))
    summary = cur.fetchall()
    conn.close()
    return summary

def check_budget_alerts(month):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category, amount FROM budgets WHERE month = ?", (month,))
    budgets = {row[0]: row[1] for row in cur.fetchall()}
    cur.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY category", (month,))
    expenses = cur.fetchall()
    alerts = []
    for category, total in expenses:
        if category in budgets:
            if total > budgets[category]:
                alerts.append((category, total, budgets[category], "Over Budget"))
            elif total > 0.9 * budgets[category]:
                alerts.append((category, total, budgets[category], "Almost Over Budget"))
    conn.close()
    return alerts

# App UI
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://img.freepik.com/free-vector/purple-gradient-background_78370-3518.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .title-container {
            text-align: center;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .title-container h1 {
            font-size: 40px;
            color: #2E3A59;
        }
    </style>
    <div class="title-container">
        <h1>💾 L7 Informatics Expense & Budget Tracker</h1>
    </div>
""", unsafe_allow_html=True)

init_db()

menu = ["Plan Expense", "Add Expense", "Set Budget", "Monthly Summary", "Budget Alerts", "Split Expense"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Plan Expense":
    st.subheader("📝 How much do you planned to spend today")
    with st.form(key='plan_form'):
        plan_date = st.date_input("Planned Date", datetime.today())
        category_options = ["Food", "Shopping", "Transportation", "Entertainment", "Utilities", "Healthcare", "Other"]
        plan_category_raw = st.selectbox("Category", category_options)
        plan_category = plan_category_raw.lower()
        plan_amount = st.number_input("Planned Amount", min_value=0.0, format="%.2f")
        plan_submit = st.form_submit_button("Check Feasibility")

        if plan_submit:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            month = plan_date.strftime("%Y-%m")
            cur.execute("SELECT amount FROM budgets WHERE month = ? AND LOWER(category) = LOWER(?)", (month, plan_category))
            result = cur.fetchone()

            if result:
                budget = result[0]
                cur.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ? AND LOWER(category) = LOWER(?)", (month, plan_category))
                spent = cur.fetchone()[0] or 0.0
                remaining = budget - spent
                if plan_amount > remaining:
                    st.toast(f"Planned expense of ${plan_amount:.2f} exceeds remaining budget of ${remaining:.2f} in {plan_category_raw} category.", icon="🚨")
                else:
                    st.success(f"Planned expense of ${plan_amount:.2f} is within the remaining budget of ${remaining:.2f} in {plan_category_raw} category.")
                    if 'plan_data' not in st.session_state:
                        st.session_state['plan_data'] = []
                    st.session_state['plan_data'].append({
                        "Date": plan_date.strftime("%Y-%m-%d"),
                        "Category": plan_category_raw,
                        "Amount": plan_amount
                    })
            else:
                st.warning(f"No budget set for {plan_category_raw} in {month}.")
            conn.close()

    if 'plan_data' in st.session_state and st.session_state['plan_data']:
        import pandas as pd
        st.markdown("### ✅ Feasible Planned Expenses for Today")
        st.dataframe(pd.DataFrame(st.session_state['plan_data']))

elif choice == "Add Expense":
    st.subheader("📅 How much do you spend ?")
    with st.form(key='expense_form'):
        date = st.date_input("Date", datetime.today())
        category_options = ["Food", "Shopping", "Transportation", "Entertainment", "Utilities", "Healthcare", "Other"]
        category = st.selectbox("Category", category_options)
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add")

        if submit and category:
            add_expense(date.strftime("%Y-%m-%d"), category, amount)
            st.success("Expense added successfully!")

            # Check for budget alert immediately after adding the expense
            current_month = date.strftime("%Y-%m")
            alerts = check_budget_alerts(current_month)
            for cat, spent, budget, status in alerts:
                if cat == category:
                    st.toast(f"{status} in {cat}: Spent ${spent:.2f} / Budget ${budget:.2f}", icon="🚨")

elif choice == "Set Budget":
    st.subheader("💰 Set Monthly Budget")
    month = st.text_input("Month (YYYY-MM)", value=datetime.today().strftime("%Y-%m"))
    category_options = ["Food", "Shopping", "Transportation", "Entertainment", "Utilities", "Healthcare", "Other"]

    st.markdown("### ✏️ Enter Budgets for Each Category")
    budget_data = []
    for category in category_options:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{category}**")
        with col2:
            budget = st.number_input(f"Budget for {category}", key=f"budget_{category}", min_value=0.0, format="%.2f")
            budget_data.append((category, budget))

    if st.button("Save All Budgets"):
        for category, amount in budget_data:
            set_budget(month, category, amount)
        st.success(f"Budgets updated for all categories in {month}.")

        # Refresh budget display after saving
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT category, amount FROM budgets WHERE month = ?", (month,))
        existing_budgets = cur.fetchall()
        conn.close()

        if existing_budgets:
            df_budgets = pd.DataFrame(existing_budgets, columns=["Category", "Budget Amount"])
            st.markdown("### 📋 Updated Budgets for the Month")
            st.dataframe(df_budgets)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category, amount FROM budgets WHERE month = ?", (month,))
    existing_budgets = cur.fetchall()
    conn.close()

    if existing_budgets:
        df_budgets = pd.DataFrame(existing_budgets, columns=["Category", "Budget Amount"])
        st.markdown("### 📋 Existing Budgets for the Month")
        st.dataframe(df_budgets)

elif choice == "Monthly Summary":
    st.subheader("📊 Monthly Spending Summary")
    month = st.text_input("Enter Month (YYYY-MM)", value=datetime.today().strftime("%Y-%m"))
    if month:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT date, category, amount FROM expenses WHERE strftime('%Y-%m', date) = ? ORDER BY date", (month,))
        expense_data = cur.fetchall()

        cur.execute("SELECT category, amount FROM budgets WHERE month = ?", (month,))
        budget_data = dict(cur.fetchall())
        conn.close()

        if expense_data:
            df = pd.DataFrame(expense_data, columns=["Date", "Category", "Amount"])
            st.dataframe(df)

            total_spent = df['Amount'].sum()
            st.markdown(f"### 💾 Total Spent: ${total_spent:.2f}")

            st.markdown("### 📌 Remaining Budgets:")
            spent_by_category = {k.lower(): v for k, v in df.groupby("Category")["Amount"].sum().to_dict().items()}
            reminders = []

            for category, budget in budget_data.items():
                spent = spent_by_category.get(category.lower(), 0.0)
                remaining = budget - spent
                reminders.append((category.title(), budget, spent, remaining))

            df_reminders = pd.DataFrame(reminders, columns=["Category", "Budget", "Spent", "Remaining"])
            st.dataframe(df_reminders)
        else:
            st.info("No expenses recorded for this month.")
            
elif choice == "Split Expense":
    st.subheader("👥 Split an Expense Among People")
    with st.form(key="split_form"):
        description = st.text_input("Description of the shared expense")
        total_amount = st.number_input("Total Expense Amount", min_value=0.0, format="%.2f")
        num_people = st.number_input("Number of People", min_value=1, step=1)
        split_submit = st.form_submit_button("Calculate Split")

        if split_submit:
            if num_people > 0:
                amount_per_person = total_amount / num_people
                st.success(f"Each person should pay: ${amount_per_person:.2f}")
            else:
                st.error("Please enter a valid number of people.")

elif choice == "Budget Alerts":
    st.subheader("⚠️ Budget Alerts")
    month = st.text_input("Enter Month (YYYY-MM)", value=datetime.today().strftime("%Y-%m"))
    if st.button("Check Alerts"):
        alerts = check_budget_alerts(month)
        if alerts:
            for category, spent, budget, status in alerts:
                st.toast(f"{status} in {category}: Spent ${spent:.2f} / Budget ${budget:.2f}", icon="🚨")
        else:
            st.toast("All spending is within budget! ✅", icon="🎉")

