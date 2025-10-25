import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image

MARKER = b'##HTA_START##'
STUB_EXE = 'stub.exe'  # Must be compiled and placed in the same folder

def select_hta_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTA Files", "*.hta")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def select_icon_file():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("ICO Files", "*.ico")])
    if file_path:
        entry_icon.delete(0, tk.END)
        entry_icon.insert(0, file_path)

def convert_png_to_ico(png_path, ico_path):
    try:
        img = Image.open(png_path)
        img.save(ico_path, format='ICO', sizes=[(256, 256)])
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Icon conversion failed: {str(e)}")
        return False

def compile_exe():
    hta_path = entry_file.get()
    icon_path = entry_icon.get()

    if not hta_path or not os.path.isfile(hta_path):
        messagebox.showerror("Error", "Please select a valid .hta file.")
        return

    if not os.path.isfile(STUB_EXE):
        messagebox.showerror("Error", f"Missing stub executable: {STUB_EXE}")
        return

    if icon_path:
        if icon_path.lower().endswith('.png'):
            ico_path = os.path.splitext(icon_path)[0] + '.ico'
            if not convert_png_to_ico(icon_path, ico_path):
                return
        else:
            ico_path = icon_path
    else:
        ico_path = None

    try:
        with open(STUB_EXE, 'rb') as stub_file:
            stub_data = stub_file.read()

        with open(hta_path, 'rb') as hta_file:
            hta_data = hta_file.read()

        output_path = os.path.splitext(hta_path)[0] + '_compiled.exe'
        with open(output_path, 'wb') as output_file:
            output_file.write(stub_data)
            output_file.write(MARKER)
            output_file.write(hta_data)

        if ico_path:
            # Use rcedit to set the icon (rcedit must be available in the system path)
            os.system(f'rcedit "{output_path}" --set-icon "{ico_path}"')

        messagebox.showinfo("Success", f"Executable created: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Compilation failed: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("HTA to Standalone EXE Compiler")

tk.Label(root, text="Select HTA File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_hta_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select Icon File (.png or .ico):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_icon = tk.Entry(root, width=50)
entry_icon.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_icon_file).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Compile to EXE", command=compile_exe).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()