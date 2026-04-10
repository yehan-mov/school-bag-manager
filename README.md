# School Bag Manager

A simple command-line tool to help students manage their school bag. It tracks your weekly timetable and tells you exactly which books to pack for today or tomorrow.

## Features
- Multi-user support with username validation
- Period-based weekly timetable (Monday - Friday, up to 8 periods)
- Book tracking per subject (textbook + notebook)
- Daily bag update — shows what to add, remove, and keep
- Fuzzy subject name matching (typo-tolerant)
- Auto-update checker via GitHub Releases
- Persistent storage via a local JSON database

## Getting Started

### Requirements
- Python 3.7+
- colorama
- requests

### Installation
git clone https://github.com/yehan-mov/school-bag-manager.git
cd school-bag-manager
pip install colorama requests
python main.py

## Usage
On launch, select an existing user or go to Settings to add a new one. From the user menu:

| Option | Description |
|---|---|
| Today's Plan | Shows what to add/remove/keep in your bag for today |
| Tomorrow's Plan | Shows what to pack tonight for tomorrow |
| Subject Options | Add, remove, or view all subjects |
| Timetable Options | Add, view, or remove periods from your timetable |
| Settings | Add users, clean up data, view app info |

## Project Structure
```
school-bag-manager/
├── main.py # Entry point
├── core.py # Bag planning logic (today/tomorrow)
├── data.py # Database, timetable and subject management
├── usermenu.py # User, subject and timetable menus
├── utils.py # Utilities (clear screen, update checker)
├── database.json # Auto-generated local database (gitignored)
└── README.md
```

## Notes
- `database.json` is created automatically on first run, keep it in the same folder as the scripts
- If the database gets corrupted it will reset automatically
- Only weekdays (Mon-Fri) are supported
- Short day names are accepted (mon, tue, wed, thu, fri)
- Upgrading from v1.0? Your `database.json` is not compatible with v1.1.0+ due to a timetable format change — you will need to rebuild your timetable

## Changelog
See [Releases](https://github.com/yehan-mov/school-bag-manager/releases) for the full changelog.

## License
This project is open source and free to use.
