# Xatos
Lightweight desktop application point of sale. Run every day sale operations and receive real time feedback of total sales.

Xatos is intended to be use with a bar code reader for product scanning and a printer for ticket printing.

## How to run
### For consumers
Pending...
Go to the release section, select the latest one and download executable.zip, unzip the file and run main.exe, this should get you going!

### For developers
#### Requirements
- python (latest version recommended)
- pdfkit
- Jinja2
- Babel
- tkcalendar

Install Python and all necessary dependencies. For convinience requirements.txt file is provided so once python is installed you can obtain all modules by runing:
'''
pip install -r requirements.txt
'''
Once that's done, the entry point of the program is main.py, start the application by running:
'''
python main.py
'''
#### Additional notes
When first run a script (init.py) will run attempting to create a new instance of the database, if changes to the database are to be made the current instance should be removed for the changes to take place, aditonaly cliUtil.py is intended to run queries directly on the database, this is an alternative for modifications of the structure.
