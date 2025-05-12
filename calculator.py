import logging
import sqlite3

# Set up logging
logging.basicConfig(filename='calc.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Arithmetic functions
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

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

# View history from SQLite
def view_history():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calculations")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No history available.")
    else:
        print("\n--- Calculation History ---")
        for row in rows:
            print(f"{row[1]} {row[2]} {row[3]} = {row[4]}")
        print("---------------------------\n")

# Main program
def main():
    print("Welcome to the Python Calculator!")

    while True:
        print("\nSelect an option:")
        print("1. Perform Calculation")
        print("2. View History")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            try:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                op = input("Choose operation (+, -, *, /): ")

                if op == '+':
                    result = add(a, b)
                elif op == '-':
                    result = subtract(a, b)
                elif op == '*':
                    result = multiply(a, b)
                elif op == '/':
                    result = divide(a, b)
                else:
                    print("Invalid operation.")
                    continue

                print(f"Result: {result}")
                logging.info(f"{a} {op} {b} = {result}")
                save_to_db(a, op, b, result)

            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '2':
            view_history()

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
