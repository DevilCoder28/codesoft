import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import json
import random
import os

def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        passwords = {}
    return passwords

def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

def generate_password(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def get_key():
    key_file = "key.txt"
    if not os.path.exists(key_file):
        # Generate a new key if key file doesn't exist
        key = Fernet.generate_key()
        with open(key_file, "wb") as key_file:
            key_file.write(key)
    else:
        # Read the key from the key file
        with open(key_file, "rb") as key_file:
            key = key_file.read()
    return key

def add_password():
    user = user_entry.get().lower()
    pass1 = pass_entry.get()
    if user == "" or pass1 == "":
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        passwords = load_passwords()
        if user in passwords:
            messagebox.showerror("Error", "Username already exists. Please choose another one.")
            return
        key = get_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(pass1.encode())
        passwords[user] = cipher_text.decode()
        save_passwords(passwords)
        user_entry.delete(0, tk.END)
        pass_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password added successfully")
        
def show_password():
    root.destroy()
    import showall

root = tk.Tk()

width = 350
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')  
root.resizable(False, False)  
root.config(bg="#7091E6")

head = tk.Label(root, text="Add Password", font=("Arial", 24), relief="raised", background="#7091E6")
head.grid(row=0, column=0, columnspan=2, pady=25)

# scale to know length of generated password
pass_length_label = tk.Label(root, text="Password Length", anchor="w", font=("Arial", 15), background="#7091E6")
pass_length_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")

pass_length = tk.Scale(root, from_=8, to=20, orient="horizontal",background="#7091E6",highlightthickness=0)
pass_length.set(12)
pass_length.grid(row=1, column=1, padx=20, pady=15)

user = tk.Label(root, text="Username/Website", anchor="w", font=("Arial", 15), background="#7091E6")
user.grid(row=2, column=0, padx=20, pady=15, sticky="w")

user_entry = tk.Entry(root, width=40, highlightthickness=1, background="#7091E6", foreground="black")
user_entry.grid(row=3, column=0, padx=0, pady=2, columnspan=2)

pass1 = tk.Label(root, text="Password", anchor="w", font=("Arial", 15), background="#7091E6")
pass1.grid(row=4, column=0, padx=20, pady=15, sticky="w")

pass_entry = tk.Entry(root, width=40, highlightthickness=1, background="#7091E6", foreground="white", show="*")
pass_entry.grid(row=5, column=0, padx=0, pady=2, columnspan=2)

generate_button = tk.Button(root, text="Generate Password", width=20, background="blue", foreground="white", font=("Arial", 15), command=lambda: pass_entry.insert(0, generate_password(pass_length.get())))
generate_button.grid(row=6, column=0, padx=0, pady=2, columnspan=2)

add = tk.Button(root, text="ADD", width=10, background="blue", foreground="white", font=("Arial", 15), command=add_password)
add.place(relx=0.38, rely=0.85, anchor="center")

show = tk.Button(root, text="show", width=10, background="green", foreground="white", font=("Arial", 15), command=show_password)
show.place(relx=0.7, rely=0.85, anchor="center")


root.mainloop()
