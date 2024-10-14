import tkinter as tk
import pyshorteners
from tkinter import messagebox, ttk
import pyperclip
import os

root = tk.Tk()
root.title("URL Shortener")
root.geometry("600x500")


# Corrected file path using raw string
history_file = r'D:\URL-shortener-\history_file.txt'

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
            # Save to file
            with open(history_file, "a") as f:
                f.write(f"{self.long_url} | {self.short_url}\n")
            
            # Update table
            history_table.insert("", "end", values=(self.long_url, self.short_url))

            # Disable save button after saving
            save_button.config(state="disabled")
            
            messagebox.showinfo("Success", "URL saved successfully!")
        
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to save URL. Please try again!")

    def copy_to_clipboard(self):
        short_url = result_label.cget("text").replace("Shortened URL: ", "")
        if short_url:
            pyperclip.copy(short_url)
            messagebox.showinfo("Copied", "Shortened URL copied to clipboard!")

    # Function to load URL history from file
    def load_history(self):
        print("Loading history...")
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    long_url, short_url = line.strip().split(" | ")
                    print(f"Loading URL: {long_url} -> {short_url}")
                    history_table.insert("", "end", values=(long_url, short_url))
        else:
            print(f"History file not found: {history_file}")

shortnerObj = shortener()

# Label
tk.Label(root, text="Enter URL to Shorten:", font=("Arial", 14)).pack(pady=10)

# input field
url_entry = tk.Entry(root, width=40, font=("Arial", 12))
url_entry.pack(pady=10)

# Shorten button
shorten_button = tk.Button(root, text="Shorten URL", command=shortnerObj.shorten_url, font=("Arial", 12), bg="lightblue")
shorten_button.pack(pady=10)

# Label to display shortened URL
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Save button
save_button = tk.Button(root, text="Save URL", command=shortnerObj.save_url, font=("Arial", 12), bg="lightgreen", state="disabled")
save_button.pack(pady=10)

# Copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=shortnerObj.copy_to_clipboard, font=("Arial", 12), bg="lightgreen")
copy_button.pack(pady=10)

# History table to show previously shortened URLs
history_frame = tk.Frame(root)
history_frame.pack(pady=20)

history_table = ttk.Treeview(history_frame, columns=("Long URL", "Short URL"), show="headings", height=6)
history_table.pack(side="left")

history_table.heading("Long URL", text="Long URL")
history_table.heading("Short URL", text="Short URL")
history_table.column("Long URL", width=250)
history_table.column("Short URL", width=150)

# Add a scrollbar to the table
scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_table.yview)
scrollbar.pack(side="right", fill="y")
history_table.config(yscrollcommand=scrollbar.set)

# Load history at the start
shortnerObj.load_history()

root.mainloop()