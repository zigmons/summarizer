# app/ui/settings_window.py
import tkinter as tk
from app.settings import save_api_key, get_api_key


def prompt_for_key():
    root = tk.Tk()
    root.title("Configuração Summarizer")
    tk.Label(root, text="Insira sua API Key:").pack(padx=10, pady=5)
    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=5)
    entry.insert(0, get_api_key() or "")
    def on_ok():
        save_api_key(entry.get().strip())
        root.destroy()
    tk.Button(root, text="OK", command=on_ok).pack(pady=10)
    root.mainloop()
    return get_api_key()
