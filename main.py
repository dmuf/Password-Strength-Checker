import tkinter as tk

def check_password():
    password = entry.get()  

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_special = True

    score = 0
    if len(password) >= 8:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score <= 2:
        result_label.config(text="Weak password ❌", fg="red")
    elif score in [3, 4]:
        result_label.config(text="Medium strength ⚠️", fg="orange")
    else:
        result_label.config(text="Strong password ✅", fg="green")

# GUI part
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("350x200")

label = tk.Label(root, text="Enter a password:", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, show="*", width=30)  # password input box
entry.pack(pady=5)

check_button = tk.Button(root, text="Check Strength", command=check_password)
check_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=5)

root.mainloop()

