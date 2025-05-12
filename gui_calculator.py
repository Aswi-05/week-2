import tkinter as tk
from tkinter import messagebox
import sqlite3
import logging

# Set up logging
logging.basicConfig(filename='calc.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Save operation to SQLite database
def save_to_db(a, op, b, result):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY,
            num1 REAL,
            operator TEXT,
            num2 REAL,
            result TEXT
        )
    ''')
    cursor.execute("INSERT INTO calculations (num1, operator, num2, result) VALUES (?, ?, ?, ?)",
                   (a, op, b, str(result)))
    conn.commit()
    conn.close()

# Perform calculation and log it
def calculate(op):
    try:
        a = float(entry1.get())
        b = float(entry2.get())

        if op == '+':
            result = a + b
        elif op == '-':
            result = a - b
        elif op == '*':
            result = a * b
        elif op == '/':
            if b == 0:
                raise ValueError("Cannot divide by zero.")
            result = a / b
        else:
            raise ValueError("Unknown operation.")

        # Display result on the GUI
        result_label.config(text=f"Result: {result}")
        
        # Save to SQLite DB
        save_to_db(a, op, b, result)

        # Log the operation to calc.log
        logging.info(f"{a} {op} {b} = {result}")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

# Show calculation history in a new window
def show_history():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calculations")
    rows = cursor.fetchall()
    conn.close()

    history_win = tk.Toplevel(root)
    history_win.title("Calculation History")

    if not rows:
        tk.Label(history_win, text="No history available.").pack()
    else:
        for row in rows:
            text = f"{row[1]} {row[2]} {row[3]} = {row[4]}"
            tk.Label(history_win, text=text).pack(anchor='w')

# GUI setup
root = tk.Tk()
root.title("GUI Calculator")

# Entry for first number
tk.Label(root, text="Enter First Number:").grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

# Entry for second number
tk.Label(root, text="Enter Second Number:").grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

# Calculator buttons
tk.Button(root, text="+", width=5, command=lambda: calculate('+')).grid(row=2, column=0)
tk.Button(root, text="-", width=5, command=lambda: calculate('-')).grid(row=2, column=1)
tk.Button(root, text="*", width=5, command=lambda: calculate('*')).grid(row=3, column=0)
tk.Button(root, text="/", width=5, command=lambda: calculate('/')).grid(row=3, column=1)

# Result label
result_label = tk.Label(root, text="Result:")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Button to view history
tk.Button(root, text="View History", command=show_history).grid(row=5, column=0, columnspan=2, pady=5)

# Start the GUI main loop
root.mainloop()
