import tkinter as tk
from tkinterdnd2 import  DND_FILES, TkinterDnD

def drop(event):
    file = root.tk.splitlist(event.data)
    for data in file:
        display_content(data)
        
def display_content(file_path):

    with open(file_path, 'r') as data:
        content = data.read()
    t_box.delete(1.0, tk.END)
    t_box.insert(tk.END, content)
    
def root_config():
    global root
    root = TkinterDnD.Tk()
    root.geometry('480x320')
    root.title('Drop_Box')
    root.attributes('-alpha', 0.65, '-topmost', True)
    root.update()
    root.resizable(False, False)
    root.iconbitmap("drop_icon.ico")

root_config()
t_box = tk.Text(root)
t_box.pack(fill=tk.X)
t_box.drop_target_register(DND_FILES)
t_box.dnd_bind('<<Drop>>',drop)

root.mainloop()
