# Skylines exporter
Enabling export of data from skylines as backup, saving to disc. This script exports
- user_info.json: user information
- flights_info.json: all flights + (some) metadata
- flights_info_extended.json: all flights + all metadata (including comments)
- igcs: igc files belonging to flights

## Motivation
Skylines is no longer actively maintained. To prevent loosing valuable flight logs, this script has been created.

Currently WeGlide is very popular, but i haven't encountered an easy export function on their site, so using the weglide-migrator is not enough.

## Usage
- `pip install -r requirements.txt` (probably best in venv)
- Create .env file (example in .env.example)
- Insert user_id and token from network tab
- `python script.py`

## Inspiration
- https://github.com/Turbo87/skylines-weglide-migrator
