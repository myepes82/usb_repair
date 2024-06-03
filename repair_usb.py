import argparse
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Diccionarios para traducción
translations = {
    "es": {
        "list_disks": "Listar Discos",
        "disk_number": "Número del Disco a Reparar:",
        "repair_disk": "Reparar Disco",
        "warning": "Advertencia",
        "enter_disk_number": "Por favor, selecciona un disco.",
        "result": "Resultado",
        "completed": "Proceso completado.",
        "error_windows": "Este script solo funciona en Windows.",
        "list_disks_msg": "Listando discos disponibles...",
        "input_disk_number": "Introduce el número del disco USB a reparar: ",
        "select_language": "Seleccionar Idioma:",
    },
    "en": {
        "list_disks": "List Disks",
        "disk_number": "Disk Number to Repair:",
        "repair_disk": "Repair Disk",
        "warning": "Warning",
        "enter_disk_number": "Please select a disk.",
        "result": "Result",
        "completed": "Process completed.",
        "error_windows": "This script only works on Windows.",
        "list_disks_msg": "Listing available disks...",
        "input_disk_number": "Enter the USB disk number to repair: ",
        "select_language": "Select Language:",
    }
}

# Idioma por defecto
language = "es"

def translate(key):
    return translations[language].get(key, key)

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error ejecutando el comando: {command}\n{result.stderr}")
    return result

def get_usb_disks():
    command = 'wmic logicaldisk where "drivetype=2" get deviceid'
    result = run_command(command)
    usb_disks = result.stdout.split()[1:]  # Ignora el encabezado
    return usb_disks

def create_diskpart_script(disk):
    with open("repair_disk.txt", "w") as f:
        f.write(f"select volume {disk}\n")
        f.write("clean\n")
        f.write("create partition primary\n")
        f.write("select partition 1\n")
        f.write("active\n")
        f.write("format fs=fat32 quick\n")
        f.write("assign\n")
        f.write("exit\n")

def repair_usb(disk):
    create_diskpart_script(disk)
    command = "diskpart /s repair_disk.txt"
    result = run_command(command)
    return result.stdout

def list_disks():
    usb_disks = get_usb_disks()
    disk_list.delete(0, tk.END)
    for disk in usb_disks:
        disk_list.insert(tk.END, disk)

def repair_selected_disk():
    selected_disk = disk_list.curselection()
    if not selected_disk:
        messagebox.showwarning(translate("warning"), translate("enter_disk_number"))
        return

    disk = disk_list.get(selected_disk)
    output = repair_usb(disk)
    messagebox.showinfo(translate("result"), output)

def set_language(selected_lang):
    global language
    language = selected_lang
    update_ui_texts()

def update_ui_texts():
    list_button.config(text=translate("list_disks"))
    repair_button.config(text=translate("repair_disk"))
    disk_label.config(text=translate("disk_number"))
    lang_label.config(text=translate("select_language"))

def main_gui():
    if not os.name == 'nt':
        messagebox.showerror("Error", translate("error_windows"))
        sys.exit(1)

    global list_button, repair_button, disk_label, lang_label, disk_list

    root = tk.Tk()
    root.title("Reparar USB")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    lang_label = tk.Label(frame, text=translate("select_language"))
    lang_label.grid(row=0, column=0, padx=5, pady=5)

    lang_select = ttk.Combobox(frame, values=["es", "en"])
    lang_select.current(0 if language == "es" else 1)
    lang_select.grid(row=0, column=1, padx=5, pady=5)
    lang_select.bind("<<ComboboxSelected>>", lambda e: set_language(lang_select.get()))

    list_button = tk.Button(frame, text=translate("list_disks"), command=list_disks)
    list_button.grid(row=1, column=0, padx=5, pady=5)

    disk_list = tk.Listbox(frame)
    disk_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    disk_label = tk.Label(frame, text=translate("disk_number"))
    disk_label.grid(row=3, column=0, padx=5, pady=5)

    repair_button = tk.Button(frame, text=translate("repair_disk"), command=repair_selected_disk)
    repair_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

    if os.path.exists("repair_disk.txt"):
        os.remove("repair_disk.txt")

    print(translate("completed"))

def main_console():
    if not os.name == 'nt':
        print(translate("error_windows"))
        sys.exit(1)

    usb_disks = get_usb_disks()
    if not usb_disks:
        print("No se encontraron discos USB.")
        sys.exit(1)

    print(translate("list_disks_msg"))
    for i, disk in enumerate(usb_disks):
        print(f"{i + 1}: {disk}")

    disk_index = int(input(translate("input_disk_number"))) - 1
    if disk_index < 0 or disk_index >= len(usb_disks):
        print("Índice de disco no válido.")
        sys.exit(1)

    disk = usb_disks[disk_index]
    output = repair_usb(disk)
    print(output)

    if os.path.exists("repair_disk.txt"):
        os.remove("repair_disk.txt")

    print(translate("completed"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reparar una unidad USB en Windows.")
    parser.add_argument('--gui', action='store_true', help="Usar interfaz gráfica")
    args = parser.parse_args()

    if args.gui:
        main_gui()
    else:
        main_console()
