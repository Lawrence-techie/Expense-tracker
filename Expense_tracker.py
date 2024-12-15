import os
import csv
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt

# File to store expenses
EXPENSE_FILE = "expenses.csv"

# Initialize the expense file if it doesn't exist
def initialize_file():
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

# Add an expense
def add_expense(date, category, amount, description):
    with open(EXPENSE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

# View expenses
def view_expenses():
    expenses = []
    with open(EXPENSE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            expenses.append(row)
    return expenses

# Generate summary
def generate_summary():
    summary = {}
    with open(EXPENSE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            category = row[1]
            amount = float(row[2])
            summary[category] = summary.get(category, 0) + amount
    return summary

# Generate a bar chart
def generate_chart():
    summary = generate_summary()
    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts, color="skyblue")
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI Application
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Labels and entries for adding expense
        tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=5)
        self.description_entry = tk.Entry(root)
        self.description_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(root, text="View Expenses", command=self.show_expenses).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Generate Chart", command=generate_chart).grid(row=6, column=0, columnspan=2, pady=10)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()

        if not date or not category or not amount:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        add_expense(date, category, amount, description)
        messagebox.showinfo("Success", "Expense added successfully!")

    def show_expenses(self):
        expenses = view_expenses()
        if not expenses:
            messagebox.showinfo("No Data", "No expenses recorded yet.")
            return

        top = tk.Toplevel(self.root)
        top.title("View Expenses")

        tk.Label(top, text=f"{'Date':<12}{'Category':<15}{'Amount':<10}{'Description':<20}").pack()
        tk.Label(top, text="-" * 60).pack()

        for row in expenses:
            tk.Label(top, text=f"{row[0]:<12}{row[1]:<15}{row[2]:<10}{row[3]:<20}").pack()

# Run the application
if __name__ == "__main__":
    initialize_file()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
