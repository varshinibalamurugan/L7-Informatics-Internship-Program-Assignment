# 💾 L7-Informatics-Internship-Program-Assignment

## ✅ Working Application & How to Run It

This is a **Python-Streamlit-based Expense & Budget Tracker**, designed as a complete solution. It allows users to plan, track, and analyze their expenses against monthly budgets in a clear, visual interface.

---

## 🔧 Setup Instructions

**1. Clone or Download the Application Folder:**  
Download or clone the folder containing `app.py`, `requirements.txt`, and `README.md`.

**2. Install Python Requirements:**  
Ensure Python 3.7+ is installed. Then install the dependencies:
```
pip install streamlit pandas
```

**3. Launch the Application:**  
Navigate to the folder where the app is located and run:
```
streamlit run app.py
```
This will launch the app in your default browser at:  
[http://localhost:8501](http://localhost:8501)

---

## 🧪 Test Steps to Validate the Application

1. Open the application using `streamlit run app.py`.
2. Go to **Set Budget** and set budget values for each category for the current month.
3. Navigate to **Add Expense** and log expenses under the same categories.
4. Go to **Monthly Summary** and verify:
   - Expense entries are listed.
   - Total spent and remaining budget are calculated correctly.
5. Use **Plan Expense** to check if a hypothetical amount fits your budget.
6. Use **Split Expense** to divide a shared expense among multiple people.
7. Use **Delete Expense** to remove any incorrect entries.
8. Use **Budget Alerts** to verify alert functionality near or beyond budget.

---

## ✅ SQL Queries / ORM Abstraction

Covered in the code using `sqlite3` statements:
- `CREATE TABLE`
- `INSERT INTO`
- `SELECT`, `DELETE`
- `GROUP BY`

All queries are cleanly abstracted in Python functions:
- `add_expense()`
- `set_budget()`
- `check_budget_alerts()`
- `get_monthly_summary()`

---

## 💡 Highlights

- Beautiful UI with background image and branded header
- Real-time toast notifications for budget thresholds
- Editable budget and expense tracking with immediate feedback
- Summarized monthly view of spending and remaining funds
- Option to split shared expenses
- Delete functionality to correct any input errors
- Fully modular Python code with SQLite backend

---

> ✅ This application is ideal for personal budgeting and financial tracking as part of the L7 Informatics Internship assignment.
