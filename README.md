# L7-Informatics-Internship-Program-Assignment

✅ Working Application & How to Run It :

This is a Python-Streamlit-based Expense & Budget Tracker, designed as a complete solution. It allows users to plan, track, and analyze their expenses against monthly budgets in a clear, visual interface.

🔧 Setup Instructions :
1. Clone or Download the Application Folder :
Download or clone the folder containing app.py, and the README.md file.
2. Install Python Requirements :
Ensure Python 3.7+ is installed.
Use pip to install required libraries:
streamlit, pandas
These can be installed by typing this in the terminal: pip install streamlit pandas
3. Launch the Application :
Navigate to the folder where app.py is located.
Run the following command: streamlit run app.py

The application will open in your default web browser at http://localhost:8501.

🧪 Test Steps to Validate the Application
1.Open the application using streamlit run app.py.
2.Go to Set Budget and set budget values for each category for the current month.
3.Navigate to Add Expense and log expenses under the same categories.
4.Go to Monthly Summary and verify:
    Expense entries are listed.Total spent and remaining budget are calculated correctly.
5.Use Plan Expense to enter a hypothetical amount and verify that toast feedback shows if it's feasible.
6.Use Split Expense to calculate fair share of a group expense.
7.In Budget Alerts, test if alerts show when expenses exceed or approach 90% of the budget.

✅ SQL Queries / ORM Abstraction :
Covered in the code via sqlite3 statements:
CREATE TABLE, INSERT INTO, SELECT, DELETE, and GROUP BY are all SQL-based interactions.
Queries are cleanly abstracted in functions like:
~add_expense()
~set_budget()
~check_budget_alerts()
~get_monthly_summary()

💡 Highlights
1. Beautiful UI with background image and branded title
2. Toast notifications for budget limits
3. Live table updates when saving budgets or logging expenses
4. All calculations are based on actual stored values in a local SQLite database
5. Fully modular and extendable Python code
