# Habit Tracker - DLBDSOOFPP01

A command-line habit tracking application built with Python.  
Phase 2 Portfolio Project — Object Oriented and Functional Programming with Python.

## Project Structure
## Setup

```bash
python3 -m pip install pytest
```

## Usage

```bash
# Load 5 predefined habits with 4 weeks of test data
PYTHONPATH=src python3 data/load_test_data.py

# Run the application
PYTHONPATH=src python3 src/main.py

# Run all tests
PYTHONPATH=src python3 -m pytest tests/test_habits.py -v
```

## Features

- Create and manage daily or weekly habits
- Automatic streak tracking
- Analytics using functional programming (filter, map, lambda)
- SQLite persistence with CASCADE DELETE
- 21 unit tests with 100% pass rate
