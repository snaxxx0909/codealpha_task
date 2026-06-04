import tkinter as tk
from tkinter import ttk, messagebox
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Hardcoded stock prices
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 350,
    "AMZN": 170,
    "NFLX": 450
}

portfolio = []

# Main window
root = tk.Tk()
root.title("Anshika's Stock Portfolio Dashboard")
root.geometry("900x650")
root.configure(bg="#f5f5f5")

# Title
title = tk.Label(
    root,
    text="📈 Stock Portfolio Dashboard",
    font=("Arial", 20, "bold"),
    bg="#f5f5f5"
)
title.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Stock:", bg="#f5f5f5").grid(row=0, column=0, padx=5)

stock_var = tk.StringVar()
stock_dropdown = ttk.Combobox(
    input_frame,
    textvariable=stock_var,
    values=list(stock_prices.keys()),
    state="readonly"
)
stock_dropdown.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Quantity:", bg="#f5f5f5").grid(row=0, column=2, padx=5)

qty_entry = tk.Entry(input_frame)
qty_entry.grid(row=0, column=3, padx=5)

# Table
columns = ("Stock", "Price", "Quantity", "Investment")

tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(pady=15)

# Total label
total_label = tk.Label(
    root,
    text="Total Investment: $0",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5"
)
total_label.pack()

# Chart Figure
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=15)

def update_chart():
    ax.clear()

    if portfolio:
        stocks = [item["stock"] for item in portfolio]
        values = [item["investment"] for item in portfolio]

        ax.bar(stocks, values)
        ax.set_title("Portfolio Investment")
        ax.set_ylabel("Value ($)")

    canvas.draw()

def update_total():
    total = sum(item["investment"] for item in portfolio)
    total_label.config(text=f"Total Investment: ${total}")

def add_stock():
    stock = stock_var.get()

    if not stock:
        messagebox.showwarning("Warning", "Select a stock.")
        return

    try:
        quantity = int(qty_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid quantity.")
        return

    price = stock_prices[stock]
    investment = price * quantity

    portfolio.append({
        "stock": stock,
        "price": price,
        "quantity": quantity,
        "investment": investment
    })

    tree.insert(
        "",
        "end",
        values=(stock, price, quantity, investment)
    )

    update_total()
    update_chart()

    qty_entry.delete(0, tk.END)

def save_csv():
    with open("portfolio.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["Stock", "Price", "Quantity", "Investment"]
        )

        for item in portfolio:
            writer.writerow([
                item["stock"],
                item["price"],
                item["quantity"],
                item["investment"]
            ])

    messagebox.showinfo(
        "Saved",
        "Portfolio saved as portfolio.csv"
    )

def clear_portfolio():
    portfolio.clear()

    for item in tree.get_children():
        tree.delete(item)

    update_total()
    update_chart()

# Buttons
button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack()

tk.Button(
    button_frame,
    text="Add Stock",
    font=("Arial", 11, "bold"),
    command=add_stock
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="Save CSV",
    font=("Arial", 11, "bold"),
    command=save_csv
).grid(row=0, column=1, padx=10)

tk.Button(
    button_frame,
    text="Clear Portfolio",
    font=("Arial", 11, "bold"),
    command=clear_portfolio
).grid(row=0, column=2, padx=10)

root.mainloop()
