'''Changing one line of G84 with tapping to many incremental lines with final Z value'''

import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD


def drop(event):
    file = root.tk.splitlist(event.data)
    for data in file:
        display_content(data)


def display_content(file_path):
    global path
    path = file_path
    with open(file_path, 'r') as data:
        content = data.read()
    t_box.delete(1.0, tk.END)
    t_box.insert(tk.END, content)


def drop_files():
    """ This function open nc file and copy its content to new file with given suffix.
    If function find line with G84 code (which mean tapping),
    its split line with Z increment till orginal z_max value.
     """
    try:
        global result
        result = float(spinbox_value.get())

    except ValueError:
            t_box.delete(1.0, tk.END)
            t_box.insert(tk.END, 'Set increment to number!')

    try:
        copy_suffix: str = '_x_mod'
        copy = path[:-3] + copy_suffix
        if path.endswith('.NC'):
            with (open(path, 'r', encoding='UTF-8') as org_file,
                  open(copy + '.nc', 'w', encoding='UTF-8') as copy_file):
                new_list = []
                for line in org_file:
                    if 'G84' in line:
                        n, fun, fun1, r, z, f = line.strip().split(' ')
                        copy_file.writelines('\n')
                        copy_file.write(f'{n} (Podmieniono wartosc {z} na ciag:) \n')

                        z_max = abs(float(z[1:]))
                        current_z = 0
                        while current_z <= z_max:
                            if current_z >= z_max:
                                break
                            result = float(spinbox_value.get())
                            if result <= 0:
                                result = 0.1
                            current_z += result
                            if current_z >= z_max:
                                current_z = z_max

                            new_line = [fun, fun1, r, 'Z-' + str(f'{current_z:.2f}'), f]
                            str_new_line = ' '.join(new_line)
                            copy_file.write(str_new_line)
                            copy_file.writelines('\n')
                            new_list.append(str_new_line)
                        new_list.append('G80\n')
                        copy_file.write('G80\n') #TYLKO JEZELI PO G80 JEST G00
                        current_z = 0
                    elif 'G80' in line:
                        new_list.clear()
                    elif len(new_list) > 0 and not 'G80' in line:
                        copy_file.write(line)
                        for value in new_list:
                            copy_file.write(value + '\n')

                    else:
                        copy_file.write(line)

        with open(copy + '.nc', 'r') as data:
            content = data.read()
        t_box.delete(1.0, tk.END)
        t_box.insert(tk.END, content)

    except NameError as Error:
        t_box.delete(1.0, tk.END)
        t_box.insert(tk.END, '<<Drop File>>')


def message():
    url = 'https://github.com/WGitra?tab=repositories'
    webbrowser.open_new(url)


root = TkinterDnD.Tk()
root.geometry('720x380')
root.title('Drop_G84_Split',)
root.attributes('-alpha', 0.87, '-topmost', True)
root.update()
root.resizable(False, False)
root.iconbitmap("drop_icon.ico")
root.config(background='khaki1')

text_frame = tk.Frame(root)
t_box = tk.Text(text_frame)
scrollbar = tk.Scrollbar(text_frame)

scrollbar.config(command=t_box.yview)
t_box.config(background='SkyBlue3', yscrollcommand=scrollbar.set, width=37, font='Havelica, 14')
t_box.drop_target_register(DND_FILES)
t_box.dnd_bind('<<Drop>>', drop)

spinbox_value = tk.StringVar(value='1')
peek_frame = tk.Frame(root)

peek_label = tk.Label(peek_frame, text='G84 Increment :', font='Havelica, 15', background='khaki1')
peek_spinbox = tk.Spinbox(peek_frame,
                          from_=0.1,
                          to=50,
                          increment=0.1,
                          textvariable=spinbox_value,
                          command='',
                          width=10,
                          background='cyan',
                          font='Havelica, 15')

button = tk.Button(root)
button.config(text='Split G84',
              background='SpringGreen',
              command=drop_files,
              font='Havelica, 15')

url_button = tk.Button(root)
url_button.config(text='WGitara_GitHub',
                   command=message,
                  background='light slate blue')

# Layout
t_box.pack(pady=0, fill=tk.Y, side=tk.LEFT)
scrollbar.pack(pady=0, fill=tk.Y, side=tk.LEFT)
text_frame.pack(side=tk.RIGHT)
peek_frame.pack(pady=20)
peek_spinbox.pack(padx=0, pady=0, fill='both', side=tk.RIGHT)
peek_label.pack(padx=0, ipady=0, fill='both', side=tk.RIGHT)
button.pack(padx=0, pady=120, fill='both')
url_button.pack(side=tk.LEFT)
t_box.insert(tk.END, '<<Drop File>>')
root.mainloop()
