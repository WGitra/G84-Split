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


def display_spinbox():

    t_box.delete(1.0, tk.END)
    t_box.insert(tk.END,spinbox_value.get())
    print(spinbox_value.get())


def root_config():
    global root
    root = TkinterDnD.Tk()
    root.geometry('380x430')
    root.title('Drop_Box')
    root.attributes('-alpha', 0.9, '-topmost', True)
    root.update()
    root.resizable(False, False)
    root.iconbitmap("drop_icon.ico")




value = 10
root_config()
t_box = tk.Text(root)
t_box.pack(fill=tk.Y)
t_box.drop_target_register(DND_FILES)
t_box.dnd_bind('<<Drop>>',drop)

spinbox_value = tk.StringVar(value=0)
peek_spinbox = tk.Spinbox(root,
                          from_=0,
                          to=value,
                          increment=0.1,
                          textvariable=spinbox_value,
                          command=display_spinbox,
                          width=10,
                          )

button = tk.Button(root)
button.config(text='Split G84')


peek_spinbox.pack()
button.pack(fill=tk.X)


root.mainloop()
