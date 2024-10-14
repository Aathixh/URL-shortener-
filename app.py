import tkinter as tk
import pyshorteners
from tkinter import messagebox
import pyperclip

root = tk.Tk()
root.title("URL Shortener")
root.geometry("400x300")
root.resizable(False, False)


class shortener:
    def shorten_url():
        long_url = url_entry.get()
        if not long_url:
            messagebox.showwarning("Input Error", "Please enter a URL!")
            return
        try:
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(long_url)
            result_label.config(text=f"Shortened URL: {short_url}")
        except Exception as e:
            messagebox.showerror("Error", "Failed to shorten URL. Please try again!")


    def copy_to_clipboard():
        short_url = result_label.cget("text").replace("Shortened URL: ", "")
        if short_url:
            pyperclip.copy(short_url)
            messagebox.showinfo("Copied", "Shortened URL copied to clipboard!")

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

# Copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=shortnerObj.copy_to_clipboard, font=("Arial", 12), bg="lightgreen")
copy_button.pack(pady=10)


root.mainloop()