# Role Assignment App

This Python project assigns four rotating roles (Moderator, Notetaker, Timekeeper, Speaker) to a group of people, ensuring that each person gets every role an equal number of times over time.

## Features

- Reads people from `src/people.json`
- Tracks weekly role assignments in `src/weeks.json`
- Ensures fair and balanced distribution of roles
- Prevents people from being assigned two weeks in a row (if possible)

## Usage

1. **Add your people**  
   Edit `src/people.json` and list each person as:
   ```json
   [
     { "name": "Person One" },
     { "name": "Person Two" }
   ]
   ```

2. **Run the script**  
   In the terminal, run:
   ```
   python src/roleapp.py
   ```

3. **View assignments**  
   - The script prints the new week's assignments.
   - All assignments are saved in `src/weeks.json`.

## Requirements

- Python 3.7+
- No external dependencies

## How it works

- The script reads all previous assignments and counts how often each person has had each role.
- For each new week, it tries to pick four people who were not assigned last week.
- Each role is assigned to the person who has done it the least number of times.
- Results are saved and can be reviewed or extended in future runs.

## License
This project is licensed under the MIT License. See the LICENSE file for details.