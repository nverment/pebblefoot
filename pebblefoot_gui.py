import tkinter as tk
from tkinter import ttk, filedialog
import os

def open_file():
    file = filedialog.askdirectory(mustexist=True)
    if file:
        filepath = os.path.abspath(file)
        tk.Label(root, text="Selected Folder: " + str(filepath), font=('Arial', 11)).grid(row=4, column=0, columnspan=2)


def save_to_file(text):
    with open("headers.txt", "w") as f:  
        f.write(text)


def open_headers():

    def save_headers():
        header_lbl.config(text=headers_text.get("1.0", tk.END))
        save_to_file(headers_text.get("1.0", tk.END))

    headers = tk.Toplevel()
    headers.geometry("800x400")
    headers.title("Header")

    tk.Label(headers, text="Insert the header text here").pack()

    headers_text = tk.Text(headers, width=70, height=10)
    headers_text.pack()

    ttk.Button(headers, text="Save", command=save_headers).pack()

    header_lbl = tk.Label(headers, text="")
    header_lbl.pack()

    headers.mainloop()

    

  


root = tk.Tk()

root.geometry("800x400")
root.title("Pebblefoot")



tk.Label(root, text="Spotify Playlist URL").grid(row=1, column=0)
tk.Label(root, text="Mode (d/t)").grid(row=3, column=0)


v = tk.IntVar()

headers_entry = ttk.Button(root, text="Headers", command=open_headers)
url_entry = tk.Entry(root)
folder_entry = ttk.Button(root, text="Browse", command=open_file)
mode_entry_d = tk.Radiobutton(root, text="d", variable=v, value=1) 
mode_entry_t = tk.Radiobutton(root, text="t", variable=v, value=2)


url_entry.grid(row=1, column=1)
folder_entry.grid(row=2, column=1)
mode_entry_d.grid(row=3, column=1, sticky=tk.W)
mode_entry_t.grid(row=3, column=1, sticky=tk.E)
headers_entry.grid(row=4, column=1,)

root.mainloop()