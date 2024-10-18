import tkinter as tk
import pyshorteners
from tkinter import messagebox, ttk
import pyperclip
import sqlite3
from datetime import datetime
import webbrowser
import threading

root = tk.Tk()
root.title("URL Shortener")
root.geometry("575x400")
root.minsize(575, 400)

# Database setup
db_file = 'history.db'
conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history
             (long_url TEXT, short_url TEXT, timestamp TEXT)''')
conn.commit()

class shortener:
    def __init__(self):
        self.long_url = ""
        self.short_url = ""

    def shorten_url(self):
        self.long_url = url_entry.get()
        if not self.long_url:
            messagebox.showwarning("Input Error", "Please enter a URL!")
            return
        try:
            shortener = pyshorteners.Shortener()
            self.short_url = shortener.tinyurl.short(self.long_url)
            result_label.config(text=f"Shortened URL: {self.short_url}")
            
            # Enable the "Save" button after shortening
            save_button.config(state="normal")

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to shorten URL. Please try again!")

    def save_url(self):
        if not self.long_url or not self.short_url:
            messagebox.showerror("Error", "No URL to save. Please shorten a URL first.")
            return

        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save to database
            c.execute("INSERT INTO history (long_url, short_url, timestamp) VALUES (?, ?, ?)",
                      (self.long_url, self.short_url, current_time))
            conn.commit()
            
            # Update table
            history_table.insert("", "0", values=(self.long_url, self.short_url, current_time))

            # Disable save button after saving
            save_button.config(state="disabled")
            
            messagebox.showinfo("Success", "URL saved successfully!")
        
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to save URL. Please try again!")
    def load_history(self):
        print("Loading history...")
        c.execute("SELECT long_url, short_url, timestamp FROM history")
        rows = c.fetchall()
        for row in rows:
            long_url, short_url, timestamp = row
            print(f"Loading URL: {long_url} -> {short_url} at {timestamp}")
            history_table.insert("", "0", values=(long_url, short_url, timestamp))

    def copy_selected_url(self, event):
        selected_item = history_table.selection()
        if selected_item:
            item = history_table.item(selected_item)
            short_url = item['values'][1]
            pyperclip.copy(short_url)
            messagebox.showinfo("Copied", f"URL copied to clipboard: {short_url}")

shortnerObj = shortener()

# Label, input field, and shorten button in a single line
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

class ButtonEffects:
    def __init__(self, button, active_bg="lightgreen", inactive_bg="lightblue"):
        self.button = button
        self.active_bg = active_bg
        self.inactive_bg = inactive_bg
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.button.config(bg=self.active_bg)

    def on_leave(self, event):
        self.button.config(bg=self.inactive_bg)

def on_entry_change(*args):
    if url_entry.get():
        shorten_button.config(state="normal")
    else:
        shorten_button.config(state="disabled")

tk.Label(input_frame, text="Shorten:", font=("Arial", 14)).pack(side="left", padx=5)
url_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
url_entry.pack(side="left", padx=5)
url_entry_var = tk.StringVar()
url_entry_var.trace_add("write", on_entry_change)
url_entry.config(textvariable=url_entry_var)

shorten_button = tk.Button(input_frame, text="Shorten URL", command=shortnerObj.shorten_url, font=("Arial", 10), bg="lightblue", bd=0, state="disabled")
shorten_button.pack(side="left", padx=5)

# Apply button effects
ButtonEffects(shorten_button)
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

# Label to display shortened URL
result_label = tk.Label(output_frame, text="", font=("Arial", 12), fg="black", cursor="hand2")
result_label.pack(side="left", padx=5)

# Save button
save_button = tk.Button(output_frame, text="Save URL", command=shortnerObj.save_url, font=("Arial", 10), bg="lightgreen", state="disabled", bd=0)
save_button.pack(side="left", padx=5)
ButtonEffects(save_button)
# Function to handle label click
def on_label_click(event):
    def delayed_copy():
        short_url = result_label.cget("text").replace("Shortened URL: ", "")
        if short_url:
            pyperclip.copy(short_url)
            messagebox.showinfo("Copied", "Shortened URL copied to clipboard!")

    # Start a timer to delay the execution of the copy function
    threading.Timer(0.3, delayed_copy).start()

# Function to handle label double-click
def on_label_double_click(event):
    short_url = result_label.cget("text").replace("Shortened URL: ", "")
    if short_url:
        webbrowser.open(short_url)

# Bind click and double-click events to the label
result_label.bind("<Button-1>", on_label_click)
result_label.bind("<Double-1>", on_label_double_click)

# Change label color on hover
def on_label_enter(event):
    result_label.config(fg="blue")

def on_label_leave(event):
    result_label.config(fg="black")

result_label.bind("<Enter>", on_label_enter)
result_label.bind("<Leave>", on_label_leave)

# History table to show previously shortened URLs
history_frame = tk.Frame(root)
history_frame.pack(pady=20)

history_table = ttk.Treeview(history_frame, columns=("Long URL", "Short URL", "Timestamp"), show="headings", height=8)
history_table.pack(side="left")

history_table.heading("Long URL", text="Long URL")
history_table.heading("Short URL", text="Short URL")
history_table.heading("Timestamp", text="Timestamp")
history_table.column("Long URL", width=250)
history_table.column("Short URL", width=150)
history_table.column("Timestamp", width=150)

# Add a scrollbar to the table
scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_table.yview)
scrollbar.pack(side="right", fill="y")
history_table.config(yscrollcommand=scrollbar.set)

history_table.bind("<Double-1>", shortnerObj.copy_selected_url)

# Load history at the start
shortnerObj.load_history()

root.mainloop()
