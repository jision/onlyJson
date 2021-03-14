"""
Name    : only_json.py
Author  : jision
Connect : jisionpc@gmail.com
Time    : 11-03-2021 4:00 PM
Desc    :
"""
import tkinter as tk
from jsonviewer.gui.main_window import Application

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    # Bind keypress event to handle_keypress()
    # app.bind("<Key>", app.handle_keypress())
    app.mainloop()
