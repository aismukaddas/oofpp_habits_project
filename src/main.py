"""
main.py - Application Entry Point

This is the main file that starts the habit tracker application.
Run this file to start the CLI: python main.py
"""

from database import DatabaseManager
from tracker import HabitTracker
from cli import CLI


def main():
    """
    Main entry point for the Habit Tracker application.
    
    Initializes the database, tracker, and CLI, then starts the interactive menu.
    """
    print("\n🚀 Initializing Habit Tracker...")
    
    # Initialize database
    db = DatabaseManager("data/habits.db")
    
    # Initialize tracker
    tracker = HabitTracker(db)
    
    # Initialize and run CLI
    cli = CLI(tracker)
    
    print(f"✅ Loaded {tracker.get_habits_count()} habits from database")
    
    # Start the interactive menu
    cli.run()


if __name__ == "__main__":
    main()
