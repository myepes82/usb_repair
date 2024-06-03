import os
import subprocess
import sys
import tempfile
import locale
import ctypes

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
        "admin_required": "Se necesitan permisos de administrador para continuar.",
        "admin_error_title": "Permisos necesarios",
        "select_language": "Seleccionar Idioma (es/en): "
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
        "admin_required": "Administrator privileges are required to continue.",
        "admin_error_title": "Permissions required",
        "select_language": "Select Language (es/en): "
    }
}

language = "es"

def detect_language():
    global language
    system_language = input("Select Language (es/en): ").strip().lower()
    if system_language == 'es':
        language = 'es'
    else:
        language = 'en'

def translate(key):
    return translations[language].get(key, key)

def is_admin():
    try:
        return os.getuid() == 0  # Unix-like systems
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()  # Windows

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result.check_returncode()
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e.stderr}")
        return e

def get_usb_disks():
    if os.name == 'nt':
        command = 'wmic logicaldisk where "drivetype=2" get deviceid'
    else:
        command = "lsblk -o NAME,TRAN | grep usb | awk '{print \"/dev/\" $1}'"
    result = run_command(command)
    usb_disks = result.stdout.split()[1:] if os.name == 'nt' else result.stdout.split()
    return usb_disks

def create_diskpart_script(disk, script_path):
    with open(script_path, "w") as f:
        f.write(f"select volume {disk}\n")
        f.write("clean\n")
        f.write("create partition primary\n")
        f.write("select partition 1\n")
        f.write("active\n")
        f.write("format fs=fat32 quick\n")
        f.write("assign\n")
        f.write("exit\n")

def repair_usb(disk):
    if os.name == 'nt':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            create_diskpart_script(disk, tmp.name)
            command = f"diskpart /s {tmp.name}"
    else:
        command = f"sudo mkfs.vfat -F 32 {disk}"
    result = run_command(command)
    if os.name == 'nt':
        os.remove(tmp.name)
    return result.stdout

def main():
    detect_language()
    
    if not is_admin():
        if os.name == 'nt':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            print(translate("admin_required"))
        sys.exit()

    usb_disks = get_usb_disks()
    if not usb_disks:
        print("No USB disks found.")
        sys.exit(1)

    print(translate("list_disks_msg"))
    for i, disk in enumerate(usb_disks):
        print(f"{i + 1}: {disk}")

    try:
        disk_index = int(input(translate("input_disk_number"))) - 1
        if disk_index < 0 or disk_index >= len(usb_disks):
            print("Invalid disk index.")
            sys.exit(1)
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    disk = usb_disks[disk_index]
    output = repair_usb(disk)
    print(output)

    print(translate("completed"))

if __name__ == "__main__":
    main()
