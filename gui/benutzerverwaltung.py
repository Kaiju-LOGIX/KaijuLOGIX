import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt
from repository import BenutzerRepository

class BenutzerLoginFenster(tk.Toplevel):
    def __init__(self, master=None, on_login_success=None):
        super().__init__(master)
        self.title("Benutzeranmeldung")
        self.geometry("300x200")
        self.on_login_success = on_login_success
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Benutzername:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_username = ttk.Entry(frame)
        self.entry_username.grid(row=0, column=1, pady=5)
        ttk.Label(frame, text="Passwort:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_password = ttk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)
        btn_login = ttk.Button(frame, text="Anmelden", command=self.login)
        btn_login.grid(row=2, column=0, columnspan=2, pady=10)
    
    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showerror("Fehler", "Bitte Benutzername und Passwort eingeben.")
            return
        repo = BenutzerRepository()
        # Direktes Repository-Verfahren (alternativ: einen eigenen Login-Repository-Methoden implementieren)
        with repo._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password, role FROM benutzer WHERE username = ? LIMIT 1", (username,))
            row = cursor.fetchone()
        if row is None:
            messagebox.showerror("Fehler", "Benutzername existiert nicht.")
            return
        user_id, stored_hashed, role = row
        if stored_hashed is None:
            messagebox.showerror("Fehler", "Kein Passwort hinterlegt.")
            return
        if bcrypt.checkpw(password.encode("utf-8"), stored_hashed):
            messagebox.showinfo("Erfolg", f"Angemeldet als {username} ({role})")
            if self.on_login_success:
                self.on_login_success(username, role)
            self.destroy()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort.")

class BenutzerVerwaltungFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Benutzerverwaltung")
        self.geometry("700x400")
        self.current_user = None
        self.current_role = None
        self.repo = BenutzerRepository()
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)
        btn_login = ttk.Button(top_frame, text="Anmelden (Demo)", command=self.open_login)
        btn_login.pack(side=tk.LEFT, padx=5)
        self.crud_frame = ttk.Frame(top_frame)
        self.crud_frame.pack(side=tk.LEFT, padx=20)
        self.btn_add = ttk.Button(self.crud_frame, text="Hinzufügen", command=self.add_user, state="disabled")
        self.btn_add.grid(row=0, column=0, padx=5)
        self.btn_edit = ttk.Button(self.crud_frame, text="Bearbeiten", command=self.edit_user, state="disabled")
        self.btn_edit.grid(row=0, column=1, padx=5)
        self.btn_delete = ttk.Button(self.crud_frame, text="Löschen", command=self.delete_user, state="disabled")
        self.btn_delete.grid(row=0, column=2, padx=5)
        self.btn_refresh = ttk.Button(self.crud_frame, text="Aktualisieren", command=self.load_data, state="disabled")
        self.btn_refresh.grid(row=0, column=3, padx=5)
        self.tree = ttk.Treeview(self, columns=("id", "username", "role"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Benutzername")
        self.tree.heading("role", text="Rolle")
        self.tree.column("id", width=50)
        self.tree.column("username", width=200)
        self.tree.column("role", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def open_login(self):
        def on_login_success(username, role):
            self.current_user = username
            self.current_role = role
            if role.lower() == "admin":
                self.set_crud_buttons_state("normal")
            else:
                self.btn_add.config(state="disabled")
                self.btn_delete.config(state="disabled")
                self.btn_edit.config(state="normal")
                self.btn_refresh.config(state="normal")
        BenutzerLoginFenster(self, on_login_success=on_login_success)
    
    def set_crud_buttons_state(self, state):
        self.btn_add.config(state=state)
        self.btn_delete.config(state=state)
        self.btn_edit.config(state=state)
        self.btn_refresh.config(state=state)
    
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        users = self.repo.get_all_users()
        for user in users:
            self.tree.insert("", tk.END, values=user)
    
    def add_user(self):
        BenutzerAddFenster(self, self.repo, on_save=self.load_data)
    
    def edit_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie einen Benutzer zum Bearbeiten aus.")
            return
        item = self.tree.item(selected[0])
        user_data = item["values"]
        BenutzerEditFenster(self, self.repo, user_data, on_save=self.load_data)
    
    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie einen Benutzer zum Löschen aus.")
            return
        item = self.tree.item(selected[0])
        user_id = item["values"][0]
        confirm = messagebox.askyesno("Bestätigung", "Soll dieser Benutzer wirklich gelöscht werden?")
        if confirm:
            self.repo.delete_user(user_id)
            messagebox.showinfo("Erfolg", "Benutzer wurde gelöscht.")
            self.load_data()

class BenutzerAddFenster(tk.Toplevel):
    def __init__(self, master, repo, on_save=None):
        super().__init__(master)
        self.title("Benutzer hinzufügen")
        self.repo = repo
        self.on_save = on_save
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Benutzername:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_username = ttk.Entry(frame)
        self.entry_username.grid(row=0, column=1, pady=5)
        ttk.Label(frame, text="Passwort:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_password = ttk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Rolle:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.role_cb = ttk.Combobox(frame, values=["admin", "user"], state="readonly")
        self.role_cb.grid(row=2, column=1, pady=5)
        self.role_cb.current(1)
        btn_save = ttk.Button(frame, text="Speichern", command=self.save_user)
        btn_save.grid(row=3, column=0, columnspan=2, pady=10)
    
    def save_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.role_cb.get().strip()
        if not username or not password or not role:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt sein.")
            return
        try:
            self.repo.insert_user(username, password, role)
            messagebox.showinfo("Erfolg", "Benutzer wurde hinzugefügt.")
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen des Benutzers: {e}")

class BenutzerEditFenster(tk.Toplevel):
    def __init__(self, master, repo, user_data, on_save=None):
        super().__init__(master)
        self.title("Benutzer bearbeiten")
        self.repo = repo
        self.on_save = on_save
        self.user_id = user_data[0]
        self.create_widgets(user_data)
    
    def create_widgets(self, user_data):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Benutzername:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_username = ttk.Entry(frame)
        self.entry_username.grid(row=0, column=1, pady=5)
        self.entry_username.insert(0, user_data[1])
        ttk.Label(frame, text="Rolle:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.role_cb = ttk.Combobox(frame, values=["admin", "user"], state="readonly")
        self.role_cb.grid(row=1, column=1, pady=5)
        self.role_cb.set(user_data[2])
        btn_save = ttk.Button(frame, text="Speichern", command=self.save_changes)
        btn_save.grid(row=2, column=0, columnspan=2, pady=10)
    
    def save_changes(self):
        username = self.entry_username.get().strip()
        role = self.role_cb.get().strip()
        if not username or not role:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt sein.")
            return
        try:
            self.repo.update_user(self.user_id, username, role)
            messagebox.showinfo("Erfolg", "Benutzer wurde aktualisiert.")
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren des Benutzers: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BenutzerVerwaltungFenster(root)
    root.mainloop()
