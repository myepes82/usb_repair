# Repair USB

## Description
`Repair USB` is a tool designed to repair USB drives. It lists available USB disks and allows users to clean and format the selected disk.

## Usage

### Clone the repository
git clone https://github.com/myepes82/usb_repair.git
cd usb_repair

### Create and activate a virtual environment

#### On Windows
python -m venv venv
call venv\Scripts\activate.bat

#### On Linux/macOS
python3 -m venv venv
source venv/bin/activate

### Install the dependencies
pip install -r requirements.txt

### Run the tool
python main.py

## Example
When running the tool, you will be prompted to select a language (`es` for Spanish or `en` for English). Then, the tool will list the available USB disks and ask you to select one to repair.

### Windows Example
C:\Users\YourUser\usb_repair> python main.py
Select Language (es/en): en
Listing available disks...
1: D:
2: E:
Enter the USB disk number to repair: 1
Process completed.

### Linux/macOS Example
youruser@yourmachine:~/usb_repair$ python3 main.py
Select Language (es/en): en
Listing available disks...
1: /dev/sdb
2: /dev/sdc
Enter the USB disk number to repair: 1
Process completed.

## Requirements
- Python 3.10 or higher
