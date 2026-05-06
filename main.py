from db_config import get_connection
import pandas as pd

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO expenses (date, category, amount, description) VALUES (%s,%s,%s,%s)"
    values = (date, category, amount, description)

    cursor.execute(query, values)
    conn.commit()

    print("Expense added successfully!")

    conn.close()


def view_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    results = cursor.fetchall()

    print("\nID | Date | Category | Amount | Description")
    print("--------------------------------------------")

    for row in results:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

    conn.close()


def monthly_summary():
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(amount) FROM expenses
    WHERE MONTH(date) = %s AND YEAR(date) = %s
    """

    cursor.execute(query, (month, year))
    result = cursor.fetchone()

    print("Total expense:", result[0])

    conn.close()


def category_summary():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    cursor.execute(query)

    results = cursor.fetchall()

    print("\nCategory Wise Expenses:")
    for row in results:
        print(row[0], ":", row[1])

    conn.close()

def delete_expense():
    expense_id = input("Enter Expense ID to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM expenses WHERE id = %s"
    cursor.execute(query, (expense_id,))

    conn.commit()

    print("Expense deleted successfully!")

    conn.close()

def export_to_excel():
    conn = get_connection()

    query = "SELECT * FROM expenses"

    df = pd.read_sql(query, conn)

    df.to_excel("expenses.xlsx", index=False)

    print("Expenses exported to Excel!")

    conn.close()


def menu():
    while True:

        print("\n===== Expense Tracker =====")
        print("1 Add Expense")
        print("2 View Expenses")
        print("3 Monthly Summary")
        print("4 Category Summary")
        print("5 Export to Excel")
        print("6 Delete Expense")
        print("7 Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            monthly_summary()

        elif choice == "4":
            category_summary()

        elif choice == "5":
            export_to_excel()

        elif choice == "6":
            delete_expense()

        elif choice == "7":
            break

        else:
            print("Invalid choice")


menu()