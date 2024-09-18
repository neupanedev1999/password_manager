import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from encryption import derive_key, encrypt_password, decrypt_password
from database import create_db, add_password, get_passwords, delete_password

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x300")
        
        self.master_password = None
        self.salt = os.urandom(16)
        self.key = None

        # Ask for master password at the start
        self.ask_master_password()

        # Create buttons for actions
        self.add_password_button = tk.Button(self.root, text="Add New Password", command=self.add_password)
        self.add_password_button.pack(pady=10)

        self.view_passwords_button = tk.Button(self.root, text="View Stored Passwords", command=self.view_passwords)
        self.view_passwords_button.pack(pady=10)

        self.delete_password_button = tk.Button(self.root, text="Delete Password", command=self.delete_password)
        self.delete_password_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def ask_master_password(self):
        """Prompt user for a master password and derive the encryption key."""
        self.master_password = simpledialog.askstring("Master Password", "Enter your master password:", show='*')
        if self.master_password:
            self.key = derive_key(self.master_password, self.salt)
        else:
            messagebox.showerror("Error", "Master password is required!")
            self.root.quit()

    def add_password(self):
        """Prompt user to add a new password for a website."""
        website = simpledialog.askstring("Website", "Enter website name:")
        username = simpledialog.askstring("Username", "Enter username:")
        password = simpledialog.askstring("Password", "Enter password:", show='*')

        if website and username and password:
            encrypted_password = encrypt_password(password, self.key)
            add_password(website, username, encrypted_password)
            messagebox.showinfo("Success", "Password added successfully!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def view_passwords(self):
        """Retrieve and display stored passwords."""
        records = get_passwords()
        if records:
            passwords = []
            for record in records:
                decrypted_password = decrypt_password(record[3], self.key)
                # Decoding the decrypted password using 'latin1' to avoid Unicode errors
                passwords.append(f"ID: {record[0]}, Website: {record[1]}, Username: {record[2]}, Password: {decrypted_password.decode('latin1')}")
            passwords_str = "\n".join(passwords)
            messagebox.showinfo("Stored Passwords", passwords_str)
        else:
            messagebox.showinfo("No Records", "No passwords stored yet!")

    def delete_password(self):
        """Prompt user to enter the ID of the password to delete."""
        password_id = simpledialog.askinteger("Delete Password", "Enter the ID of the password to delete:")
        if password_id:
            delete_password(password_id)
            messagebox.showinfo("Success", f"Password with ID {password_id} deleted.")
        else:
            messagebox.showerror("Error", "ID is required to delete a password!")

if __name__ == "__main__":
    create_db()  # Ensure the database and table are created before starting the app
    
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
