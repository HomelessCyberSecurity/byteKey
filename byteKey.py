import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import pyperclip

class CryptoTool:
    def __init__(self, master):
        self.master = master
        master.title("Crypto Tool Menu")
        window_width = 450
        window_height = 550
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        master.resizable(False, False)

        self.current_frame = None
        self.show_password = tk.BooleanVar()

        self.main_menu_frame = self.create_main_menu_frame(master)
        self.encrypt_frame = self.create_encrypt_frame(master)
        self.encrypt_with_key_frame = self.create_encrypt_with_key_frame(master)
        self.decrypt_frame = self.create_decrypt_frame(master)

        self.show_frame(self.main_menu_frame)

    def generate_key(self):
        return Fernet.generate_key().decode()

    def encrypt_with_key(self, password, key_bytes):
        f = Fernet(key_bytes)
        return f.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password, key_bytes):
        f = Fernet(key_bytes)
        try:
            return f.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            messagebox.showerror("Error", "Invalid key or encrypted data.")
            return None

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = frame
        frame.pack(padx=10, pady=10, fill="both", expand=True)

    def create_main_menu_frame(self, master):
        frame = ttk.Frame(master)
        ttk.Label(frame, text="Select an Action:", font=("Arial", 16)).pack(pady=20)
        ttk.Button(frame, text="Encrypt (Generate Key)", command=lambda: self.show_frame(self.encrypt_frame)).pack(pady=10, fill="x")
        ttk.Button(frame, text="Encrypt with Specific Key", command=lambda: self.show_frame(self.encrypt_with_key_frame)).pack(pady=10, fill="x")
        ttk.Button(frame, text="Decrypt", command=lambda: self.show_frame(self.decrypt_frame)).pack(pady=10, fill="x")
        return frame

    def create_encrypt_frame(self, master):
        frame = ttk.Frame(master)
        ttk.Label(frame, text="Enter Password to Encrypt:", font=("Arial", 12)).pack(pady=10)
        self.encrypt_entry_password = ttk.Entry(frame, show="*")
        self.encrypt_entry_password.pack(pady=5, fill="x", padx=10)
        ttk.Checkbutton(frame, text="Show Password", variable=self.show_password, command=self.toggle_password_visibility).pack(pady=5, padx=10, anchor="w")
        ttk.Label(frame, text="Generated Encryption Key:", font=("Arial", 12)).pack(pady=10)
        self.encrypt_key_display = tk.Text(frame, height=3, state=tk.DISABLED)
        self.encrypt_key_display.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Key", command=lambda: self.copy_to_clipboard(self.encrypt_key_display.get(1.0, tk.END).strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Button(frame, text="Encrypt", command=self.encrypt_button_click).pack(pady=10, fill="x", padx=10)
        ttk.Label(frame, text="Encrypted Output:", font=("Arial", 12)).pack(pady=10)
        self.encrypt_output = tk.Text(frame, height=3)
        self.encrypt_output.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Encrypted", command=lambda: self.copy_to_clipboard(self.encrypt_output.get(1.0, tk.END).strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Button(frame, text="Back to Menu", command=lambda: self.show_frame(self.main_menu_frame)).pack(pady=15)
        return frame

    def create_encrypt_with_key_frame(self, master):
        frame = ttk.Frame(master)
        ttk.Label(frame, text="Enter Password to Encrypt:", font=("Arial", 12)).pack(pady=10)
        self.encrypt_with_key_entry_password = ttk.Entry(frame, show="*")
        self.encrypt_with_key_entry_password.pack(pady=5, fill="x", padx=10)
        ttk.Checkbutton(frame, text="Show Password", variable=self.show_password, command=self.toggle_password_visibility).pack(pady=5, padx=10, anchor="w")
        ttk.Label(frame, text="Enter Encryption Key:", font=("Arial", 12)).pack(pady=10)
        self.encrypt_with_key_entry_key = ttk.Entry(frame)
        self.encrypt_with_key_entry_key.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Key", command=lambda: self.copy_to_clipboard(self.encrypt_with_key_entry_key.get().strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Button(frame, text="Encrypt", command=self.encrypt_with_specific_key_button_click).pack(pady=10, fill="x", padx=10)
        ttk.Label(frame, text="Encrypted Output:", font=("Arial", 12)).pack(pady=10)
        self.encrypt_with_key_output = tk.Text(frame, height=3)
        self.encrypt_with_key_output.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Encrypted", command=lambda: self.copy_to_clipboard(self.encrypt_with_key_output.get(1.0, tk.END).strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Button(frame, text="Back to Menu", command=lambda: self.show_frame(self.main_menu_frame)).pack(pady=15)
        return frame

    def create_decrypt_frame(self, master):
        frame = ttk.Frame(master)
        ttk.Label(frame, text="Enter Encrypted Text to Decrypt:", font=("Arial", 12)).pack(pady=10)
        self.decrypt_entry_encrypted = ttk.Entry(frame)
        self.decrypt_entry_encrypted.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Encrypted", command=lambda: self.copy_to_clipboard(self.decrypt_entry_encrypted.get().strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Label(frame, text="Enter Decryption Key:", font=("Arial", 12)).pack(pady=10)
        self.decrypt_entry_key = ttk.Entry(frame)
        self.decrypt_entry_key.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Key", command=lambda: self.copy_to_clipboard(self.decrypt_entry_key.get().strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Button(frame, text="Decrypt", command=self.decrypt_button_click).pack(pady=10, fill="x", padx=10)
        ttk.Label(frame, text="Decrypted Output:", font=("Arial", 12)).pack(pady=10)
        self.decrypt_output = tk.Text(frame, height=3)
        self.decrypt_output.pack(pady=5, fill="x", padx=10)
        ttk.Button(frame, text="Copy Decrypted", command=lambda: self.copy_to_clipboard(self.decrypt_output.get(1.0, tk.END).strip())).pack(pady=5, padx=10, anchor="w")
        ttk.Button(frame, text="Back to Menu", command=lambda: self.show_frame(self.main_menu_frame)).pack(pady=15)
        return frame

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.encrypt_entry_password.config(show="")
            self.encrypt_with_key_entry_password.config(show="")
        else:
            self.encrypt_entry_password.config(show="*")
            self.encrypt_with_key_entry_password.config(show="*")

    def copy_to_clipboard(self, text):
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "Text copied to clipboard!")
        except pyperclip.PyperclipException:
            messagebox.showerror("Error", "Clipboard functionality not available. Please install 'pyperclip'.")

    def encrypt_button_click(self):
        password = self.encrypt_entry_password.get()
        if not password:
            messagebox.showerror("Input Error", "Please enter a password to encrypt.")
            return

        generated_key = self.generate_key()
        self.encrypt_key_display.config(state=tk.NORMAL)
        self.encrypt_key_display.delete(1.0, tk.END)
        self.encrypt_key_display.insert(tk.END, generated_key)
        self.encrypt_key_display.config(state=tk.DISABLED)

        key_bytes = generated_key.encode()
        encrypted = self.encrypt_with_key(password, key_bytes)
        self.encrypt_output.delete(1.0, tk.END)
        self.encrypt_output.insert(tk.END, encrypted)

    def encrypt_with_specific_key_button_click(self):
        password = self.encrypt_with_key_entry_password.get()
        key = self.encrypt_with_key_entry_key.get()

        if not password:
            messagebox.showerror("Input Error", "Please enter a password to encrypt.")
            return
        if not key:
            messagebox.showerror("Input Error", "Please enter the encryption key.")
            return

        try:
            key_bytes = key.encode()
            f = Fernet(key_bytes) # Validate key format
            encrypted = self.encrypt_with_key(password, key_bytes)
            self.encrypt_with_key_output.delete(1.0, tk.END)
            self.encrypt_with_key_output.insert(tk.END, encrypted)
        except Exception as e:
            messagebox.showerror("Key Error", f"Invalid Fernet key format.\nError: {e}")

    def decrypt_button_click(self):
        encrypted_input = self.decrypt_entry_encrypted.get()
        key = self.decrypt_entry_key.get()

        if not encrypted_input:
            messagebox.showerror("Input Error", "Please enter encrypted text to decrypt.")
            return
        if not key:
            messagebox.showerror("Input Error", "Please enter the decryption key.")
            return

        try:
            key_bytes = key.encode()
            decrypted = self.decrypt_password(encrypted_input, key_bytes)
            if decrypted is not None:
                self.decrypt_output.delete(1.0, tk.END)
                self.decrypt_output.insert(tk.END, decrypted)
        except Exception as e:
            messagebox.showerror("Key Error", f"Invalid Fernet key format.\nError: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoTool(root)
    root.mainloop()
