# School Bag Manager
### A simple command-line tool to help students manage their school bag. It tracks your weekly timetable and tells you exactly which books to pack for today or tomorrow.
---
### Features
- Multi-user support
- Weekly timetable (Monday - Friday)
- Book tracking per subject (textbook + notebook)
- Daily bag update, shows what to add, remove and keep
- Persistent storage via a local JSON database
---
### Getting Started
<b>Requirements</b>
- Python 3.7+
- colorama

<b>Installation</b>
```
git clone https://github.com/yehan-mov/school-bag-manager.git
cd school-bag-manager
pip install colorama
python main.py
```
---
### Usage
On launch, you can add a user or select an existing one. From the user menu:
| Option | Description |
| ------ | ----------- |
| Today's Plan | Shows what to add/remove/keep in your bag for today |
| Tomorrow's Plan | Shows what to pack tonight for tomorrow |
| Add Subject | Register a new subject (auto creates textbook + notebook) |
| Add to Timetable | Schedule a subject on a specific day |
---
### Project Structure
```
school-bag-manager/
├── main.py          # Main application
├── database.json    # Auto-generated local database (gitignored)
└── README.md
```
---
### Notes
- ```database.json``` is created automatically on first run, keep it in the same folder as ```main.py```
- If the database gets corrupted, it will reset automatically
- Only weekdays (Mon-Fri) are supported (support for Sat is excpeted)
---
### License
This project is open source and free to use.
