import tkinter as tk
from tkinter import messagebox
import hashlib
import requests
import secrets
import string

# Constants
HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"
REQUEST_TIMEOUT = 5
SUGGESTED_PASSWORD_LENGTH = 16


def is_password_pwned(password: str) -> int:
    if not password:
        return 0
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        resp = requests.get(HIBP_RANGE_URL.format(prefix), timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException:
        raise

    for line in resp.text.splitlines():
        parts = line.split(":")
        if len(parts) == 2 and parts[0] == suffix:
            return int(parts[1]) if parts[1].isdigit() else 1
    return 0

def generate_strong_password(length=SUGGESTED_PASSWORD_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd)
            and any(c.isupper() for c in pwd)
            and any(c.isdigit() for c in pwd)
            and any(c in string.punctuation for c in pwd)):
            return pwd

#Gui functions
def check_password():
    password = entry.get()
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = sum([
        len(password) >= 8,
        has_upper,
        has_lower,
        has_digit,
        has_special
    ])

    if score <= 2:
        result_label.config(text="Weak password ❌", fg="red")
    elif score in (3, 4):
        result_label.config(text="Medium strength ⚠️", fg="orange")
    else:
        result_label.config(text="Strong password ✅", fg="green")

    try:
        pwn_count = is_password_pwned(password)
    except Exception:
        hibp_label.config(text="HIBP check failed (network error).", fg="gray")
        return

    if pwn_count > 0:
        hibp_label.config(
            text=f"Pwned! Seen {pwn_count:,} time(s) — avoid using this.",
            fg="red"
        )
    else:
        hibp_label.config(text="Not found in known breaches.", fg="green")

def on_generate():
    entry_var.set(generate_strong_password())
    check_password()
    entry.focus_set()

def toggle_show_password():
    entry.config(show="" if show_var.get() else "*")

def on_exit():
    if messagebox.askokcancel("Exit", "Close Password Checker?"):
        root.destroy()

#Gui setup
root = tk.Tk()
root.title("Password Checker")
root.geometry("500x220")
root.resizable(True, True)

main_frame = tk.Frame(root, padx=8, pady=8)
main_frame.pack(fill="both", expand=True)

tk.Label(main_frame, text="Enter password:", font=("Arial", 11)).pack(anchor="w")

entry_var = tk.StringVar()
entry = tk.Entry(main_frame, textvariable=entry_var, show="*", width=45)
entry.pack(fill="x", pady=4)

controls_frame = tk.Frame(main_frame)
controls_frame.pack(fill="x", pady=4)

check_button = tk.Button(controls_frame, text="Check", command=check_password)
check_button.pack(side="left", padx=2)

generate_button = tk.Button(controls_frame, text="Generate", command=on_generate)
generate_button.pack(side="left", padx=2)

show_var = tk.BooleanVar(value=False)
show_check = tk.Checkbutton(controls_frame, text="Show", variable=show_var, command=toggle_show_password)
show_check.pack(side="left", padx=2)

exit_button = tk.Button(controls_frame, text="Exit", command=on_exit)
exit_button.pack(side="right", padx=2)

result_label = tk.Label(main_frame, text="", font=("Arial", 10))
result_label.pack(anchor="w", pady=(6, 2))

hibp_label = tk.Label(main_frame, text="", font=("Arial", 9))
hibp_label.pack(anchor="w")

root.mainloop()
