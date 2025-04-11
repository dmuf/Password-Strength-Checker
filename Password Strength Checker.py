import tkinter as tk
from tkinter import messagebox
import re

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[@$!%*?&#]', password):
        score += 1

    if score == 5:
        return "Strong"
    elif score >= 3:
        return "Moderate"
    else:
        return "Weak"

def evaluate():
    password = entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    strength = check_password_strength(password)
    result_label.config(text=f"Password Strength: {strength}")

def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

# GUI
root = tk.Tk()
root.title("Password Strength Checker")

tk.Label(root, text="Enter Password:").pack(pady=5)

entry = tk.Entry(root, width=30, show="*")
entry.pack(pady=5)

show_var = tk.BooleanVar()
show_check = tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password)
show_check.pack()

tk.Button(root, text="Check Strength", command=evaluate).pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
