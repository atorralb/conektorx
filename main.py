#Based on Spring Boot 3 RestClient
#Variable mapping    
#uri
#contentType: MediaType.APPLICATION_JSON
#headers:
#   setBearerAuth
#   set

import tkinter as tk
from tkinter import ttk

def select_option(event=None):
    selected = variable.get()
    label.config(text=f"You selected: {selected}")
root = tk.Tk()
root.title("REST request")
#method: post, get, put, del
options = ["post", "get", "put", "delete"]

variable = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=variable)
dropdown['values'] = options
dropdown.current(0)  # Set default selected option
dropdown.pack(padx=10, pady=10)

button = tk.Button(root, text="Get Selected Option", command=select_option)
button.pack(padx=10, pady=5)

label = tk.Label(root, text="Select an option")
label.pack(padx=10, pady=5)

root.mainloop()
