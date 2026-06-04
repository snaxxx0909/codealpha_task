import tkinter as tk
from tkinter import filedialog, messagebox
import re

emails = []

def open_file():
    global emails

    filepath = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if not filepath:
        return

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    emails = re.findall(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        content
    )

    result_box.delete("1.0", tk.END)

    if emails:
        for email in emails:
            result_box.insert(tk.END, email + "\n")

        count_label.config(
            text=f"Emails Found: {len(emails)}"
        )
    else:
        result_box.insert(
            tk.END,
            "No email addresses found."
        )

        count_label.config(text="Emails Found: 0")

def save_emails():
    if not emails:
        messagebox.showwarning(
            "Warning",
            "No emails to save."
        )
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if save_path:
        with open(save_path, "w") as file:
            for email in emails:
                file.write(email + "\n")

        messagebox.showinfo(
            "Success",
            "Emails saved successfully!"
        )

root = tk.Tk()
root.title("Email Extractor Tool")
root.geometry("700x500")
root.configure(bg="#f5f7fa")

title = tk.Label(
    root,
    text="📧 Email Extractor",
    font=("Arial", 20, "bold"),
    bg="#f5f7fa"
)
title.pack(pady=15)

open_btn = tk.Button(
    root,
    text="Open TXT File",
    font=("Arial", 12, "bold"),
    command=open_file
)
open_btn.pack(pady=10)

count_label = tk.Label(
    root,
    text="Emails Found: 0",
    font=("Arial", 12),
    bg="#f5f7fa"
)
count_label.pack()

result_box = tk.Text(
    root,
    width=60,
    height=15,
    font=("Consolas", 11)
)
result_box.pack(pady=15)

save_btn = tk.Button(
    root,
    text="Save Emails",
    font=("Arial", 12, "bold"),
    command=save_emails
)
save_btn.pack(pady=10)

root.mainloop()