import random
import string
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import locale

class PasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        
        
        self.favorites_file = "favorites_passwords.json"
        self.lang_file = "localization.json"
        
        
        self.current_language = self.detect_language()
        self.localization = self.load_localization()
        
       
        self.length = tk.IntVar(value=12)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        
        
        self.favorites = self.load_favorites()
        
        self.create_widgets()
        self.update_language()
    
    def detect_language(self):
        
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale and ('ru' in system_locale.lower() or 'rus' in system_locale.lower()):
                return 'ru'
            else:
                return 'en'
        except:
            return 'en'
    
    def load_localization(self):
        
        if os.path.exists(self.lang_file):
            try:
                with open(self.lang_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading localization: {e}")
                return {}
        else:
            return {}
    
    def get_text(self, key):
        
        return self.localization.get(self.current_language, {}).get(key, key)
    
    def toggle_language(self):
        
        self.current_language = 'en' if self.current_language == 'ru' else 'ru'
        self.update_language()
    
    def update_language(self):
        
        self.recreate_widgets()
    
    def recreate_widgets(self):
        
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        
        self.create_widgets()
    
    def load_favorites(self):
        
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_favorites(self):
        
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save favorites: {str(e)}")
            return False
    
    def create_widgets(self):
        
        title_label = tk.Label(self.root, text=self.get_text("title"), 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        
        lang_btn = tk.Button(self.root, text=self.get_text("language_btn"), 
                            command=self.toggle_language, bg="#9C27B0", 
                            fg="white", font=("Arial", 8))
        lang_btn.pack(pady=(0, 10))
        
        
        length_frame = tk.Frame(self.root)
        length_frame.pack(pady=5, fill="x", padx=20)
        
        tk.Label(length_frame, text=self.get_text("length_label"), font=("Arial", 10)).pack(side="left")
        length_spinbox = tk.Spinbox(length_frame, from_=4, to=50, textvariable=self.length, 
                                   width=5, font=("Arial", 10))
        length_spinbox.pack(side="left", padx=(10, 0))
        
        
        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Checkbutton(options_frame, text=self.get_text("uppercase"), 
                      variable=self.use_uppercase, font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text=self.get_text("lowercase"), 
                      variable=self.use_lowercase, font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text=self.get_text("digits"), 
                      variable=self.use_digits, font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text=self.get_text("symbols"), 
                      variable=self.use_symbols, font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text=self.get_text("exclude_ambiguous"), 
                      variable=self.exclude_ambiguous, font=("Arial", 10)).pack(anchor="w")
        
        
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=15)
        
        generate_btn = tk.Button(buttons_frame, text=self.get_text("generate_btn"), 
                                command=self.generate_password, bg="#4CAF50", 
                                fg="white", font=("Arial", 10, "bold"))
        generate_btn.pack(side="left", padx=5)
        
        self.favorite_btn = tk.Button(buttons_frame, text=self.get_text("add_favorite_btn"), 
                                     command=self.add_to_favorites, bg="#FF9800", 
                                     fg="white", font=("Arial", 10))
        self.favorite_btn.pack(side="left", padx=5)
        self.favorite_btn.config(state="disabled")
        
        show_favorites_btn = tk.Button(buttons_frame, text=self.get_text("show_favorites_btn"), 
                                      command=self.show_favorites, bg="#2196F3", 
                                      fg="white", font=("Arial", 10))
        show_favorites_btn.pack(side="left", padx=5)
        
        
        self.password_var = tk.StringVar()
        password_frame = tk.Frame(self.root)
        password_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(password_frame, text=self.get_text("password_label"), 
                font=("Arial", 10)).pack(anchor="w")
        
        password_entry = tk.Entry(password_frame, textvariable=self.password_var, 
                                 font=("Arial", 12), state="readonly", 
                                 readonlybackground="white")
        password_entry.pack(fill="x", pady=(5, 0))
        
        
        copy_btn = tk.Button(self.root, text=self.get_text("copy_btn"), 
                            command=self.copy_to_clipboard, bg="#2196F3", 
                            fg="white", font=("Arial", 10))
        copy_btn.pack(pady=10)
        
        
        strength_frame = tk.Frame(self.root)
        strength_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(strength_frame, text=self.get_text("strength_label"), 
                font=("Arial", 10)).pack(anchor="w")
        
        self.strength_label = tk.Label(strength_frame, text="", 
                                      font=("Arial", 10, "bold"))
        self.strength_label.pack(anchor="w")
        
        
        self.last_saved_label = tk.Label(self.root, text="", 
                                        font=("Arial", 9), fg="green")
        self.last_saved_label.pack(pady=5)
    
    def generate_password(self):
        
        try:
            length = self.length.get()
            
            if length < 4:
                messagebox.showerror("Error", self.get_text("min_length_error"))
                return
            
            
            characters = ""
            
            if self.use_uppercase.get():
                characters += string.ascii_uppercase
            if self.use_lowercase.get():
                characters += string.ascii_lowercase
            if self.use_digits.get():
                characters += string.digits
            if self.use_symbols.get():
                characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            
            if self.exclude_ambiguous.get():
                ambiguous = "0O1lI"
                characters = ''.join(c for c in characters if c not in ambiguous)
            
            if not characters:
                messagebox.showerror("Error", self.get_text("select_chars_error"))
                return
            
            
            password = ''.join(random.choice(characters) for _ in range(length))
            
            
            password = self.ensure_character_types(password, characters)
            
            self.password_var.set(password)
            self.update_strength_indicator(password)
            self.favorite_btn.config(state="normal")
            self.last_saved_label.config(text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def ensure_character_types(self, password, characters):
        
        password_list = list(password)
        
        
        required_chars = []
        
        if self.use_uppercase.get():
            if not any(c in string.ascii_uppercase for c in password_list):
                required_chars.append(random.choice(string.ascii_uppercase))
        
        if self.use_lowercase.get():
            if not any(c in string.ascii_lowercase for c in password_list):
                required_chars.append(random.choice(string.ascii_lowercase))
        
        if self.use_digits.get():
            if not any(c in string.digits for c in password_list):
                required_chars.append(random.choice(string.digits))
        
        if self.use_symbols.get():
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in symbols for c in password_list):
                required_chars.append(random.choice(symbols))
        
        
        for char in required_chars:
            if password_list:
                index = random.randint(0, len(password_list) - 1)
                password_list[index] = char
        
        return ''.join(password_list)
    
    def update_strength_indicator(self, password):
        
        strength = self.calculate_password_strength(password)
        
        if strength < 3:
            color = "red"
            text = self.get_text("weak")
        elif strength < 5:
            color = "orange"
            text = self.get_text("medium")
        else:
            color = "green"
            text = self.get_text("strong")
        
        self.strength_label.config(text=f"{text} ({strength}/6)", fg=color)
    
    def calculate_password_strength(self, password):
        
        score = 0
        
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        
        
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        
        return score
    
    def copy_to_clipboard(self):
        
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", self.get_text("copied"))
        else:
            messagebox.showwarning("Warning", self.get_text("generate_first"))
    
    def add_to_favorites(self):
        
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", self.get_text("generate_first"))
            return
        
        
        favorite_entry = {
            "password": password,
            "length": len(password),
            "strength": self.calculate_password_strength(password),
            "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        }
        
        
        self.favorites.append(favorite_entry)
        
        
        if self.save_favorites():
            self.last_saved_label.config(text=self.get_text("saved_to_favorites").format(len(self.favorites)))
            messagebox.showinfo("Success", f"Password added to favorites!\nTotal in favorites: {len(self.favorites)}")
        else:
            messagebox.showerror("Error", "Could not save to favorites!")
    
    def show_favorites(self):
        
        if not self.favorites:
            messagebox.showinfo("Favorites", self.get_text("favorites_empty"))
            return
        
        
        favorites_window = tk.Toplevel(self.root)
        favorites_window.title(self.get_text("favorites_title"))
        favorites_window.geometry("700x500")
        favorites_window.resizable(True, True)
        
        
        list_frame = tk.Frame(favorites_window)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        columns = (self.get_text("date_added"), self.get_text("length"), self.get_text("strength"), self.get_text("password"))
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        
        tree.heading(self.get_text("date_added"), text=self.get_text("date_added"))
        tree.heading(self.get_text("length"), text=self.get_text("length"))
        tree.heading(self.get_text("strength"), text=self.get_text("strength"))
        tree.heading(self.get_text("password"), text=self.get_text("password"))
        
        
        tree.column(self.get_text("date_added"), width=120)
        tree.column(self.get_text("length"), width=50, anchor="center")
        tree.column(self.get_text("strength"), width=50, anchor="center")
        tree.column(self.get_text("password"), width=300)
        
        
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        
        for item in reversed(self.favorites):  
            strength_text = f"{item['strength']}/6"
            tree.insert("", 0, values=(item['date'], item['length'], strength_text, item['password']))
        
        
        buttons_frame = tk.Frame(favorites_window)
        buttons_frame.pack(pady=10)
        
        
        def copy_selected():
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                password = item['values'][3]  
                favorites_window.clipboard_clear()
                favorites_window.clipboard_append(password)
                messagebox.showinfo("Success", self.get_text("copied"), parent=favorites_window)
            else:
                messagebox.showwarning("Warning", self.get_text("select_to_copy"), parent=favorites_window)
        
        copy_btn = tk.Button(buttons_frame, text=self.get_text("copy_selected"), 
                            command=copy_selected, bg="#2196F3", fg="white")
        copy_btn.pack(side="left", padx=5)
        
        
        def delete_selected():
            selection = tree.selection()
            if selection:
                if messagebox.askyesno("Confirmation", self.get_text("confirm_delete"), parent=favorites_window):
                    item = tree.item(selection[0])
                    date = item['values'][0]
                    password = item['values'][3]
                    
                    
                    for i, fav in enumerate(self.favorites):
                        if fav['date'] == date and fav['password'] == password:
                            del self.favorites[i]
                            break
                    
                    
                    self.save_favorites()
                    tree.delete(selection[0])
                    self.last_saved_label.config(text=self.get_text("favorites_updated").format(len(self.favorites)))
                    messagebox.showinfo("Success", self.get_text("deleted_success"), parent=favorites_window)
            else:
                messagebox.showwarning("Warning", self.get_text("select_to_delete"), parent=favorites_window)
        
        delete_btn = tk.Button(buttons_frame, text=self.get_text("delete_selected"), 
                              command=delete_selected, bg="#f44336", fg="white")
        delete_btn.pack(side="left", padx=5)
        
        
        def clear_all():
            if messagebox.askyesno("Confirmation", self.get_text("confirm_clear"), parent=favorites_window):
                self.favorites.clear()
                self.save_favorites()
                tree.delete(*tree.get_children())
                self.last_saved_label.config(text=self.get_text("favorites_updated").format(len(self.favorites)))
                messagebox.showinfo("Success", self.get_text("cleared_success"), parent=favorites_window)
        
        clear_btn = tk.Button(buttons_frame, text=self.get_text("clear_all"), 
                             command=clear_all, bg="#ff9800", fg="white")
        clear_btn.pack(side="left", padx=5)
        
        
        def on_double_click(event):
            item = tree.identify('item', event.x, event.y)
            if item:
                values = tree.item(item, 'values')
                password = values[3]
                favorites_window.clipboard_clear()
                favorites_window.clipboard_append(password)
                
                status_label = tk.Label(favorites_window, text=self.get_text("double_click_copy"), fg="green")
                status_label.pack()
                favorites_window.after(1000, status_label.destroy)
        
        tree.bind("<Double-1>", on_double_click)
    
    def run(self):
        
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()