import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import json
import os

def get_key():
    key_file = "key.txt"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as kf:
            kf.write(key)
    else:
        with open(key_file, "rb") as kf:
            key = kf.read()
    return key

def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        passwords = {}
    key = get_key()
    decrypted_passwords = {}
    cipher_suite = Fernet(key)
    for user, encrypted_password in passwords.items():
        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        except (Exception) as e:
            print(f"Error decrypting password for {user}: {e}")
            decrypted_password = "[Decryption Failed]"
        decrypted_passwords[user] = decrypted_password
    return decrypted_passwords

def display_passwords():
    text_area.delete(1.0, tk.END)
    decrypted_passwords = load_passwords()
    if not decrypted_passwords:
        messagebox.showinfo("Info", "No passwords found.")
        return
    
    for user, decrypted_password in decrypted_passwords.items():
        text_area.insert(tk.END, f"Username/Website: {user}\n")
        text_area.insert(tk.END, f"Decrypted Password: {decrypted_password}\n\n")

    text_area.configure(state='disabled')

def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

root = tk.Tk()
root.title("Password Manager")

width = 350  
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')  
root.resizable(False, False)  
root.config(bg="#7091E6")

head = tk.Label(root, text="Passwords", font=("Arial", 24), relief="raised", background="#7091E6")
head.grid(row=0, column=0, columnspan=2, pady=25)

text_area = tk.scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=25)
text_area.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

display_button = tk.Button(root, text="Show All Passwords (Decrypted)", width=30, background="blue", foreground="white", font=("Arial", 15), command=display_passwords)
display_button.place(relx=0.5, rely=0.9, anchor="center")

root.mainloop()
