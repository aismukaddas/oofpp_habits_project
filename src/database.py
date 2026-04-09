"""
database.py - DatabaseManager Module

This file handles all SQLite database operations.
It saves and loads habits, manages completions, and ensures data integrity.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from habit import Habit, Periodicity


class DatabaseManager:
    """
    Manages all database operations using SQLite.
    
    This class abstracts all SQL operations so other parts of the code
    don't need to know about database details.
    
    Database Schema:
        - habits table: stores habit metadata
        - completions table: stores every time a habit was completed
    
    Example:
        >>> db = DatabaseManager("habits.db")
        >>> habit_id = db.save_habit(my_habit)
        >>> all_habits = db.load_all_habits()
    """
    
    def __init__(self, db_path: str = "data/habits.db"):
        """
        Initialize database connection and create tables if needed.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """
        Create the database tables if they don't exist.
        
        Creates two tables:
        1. habits - stores habit information
        2. completions - stores completion records with CASCADE DELETE
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL CHECK(periodicity IN ('daily', 'weekly')),
                created_date TEXT NOT NULL
            )
        ''')
        
        # Create completions table with foreign key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completions (
                completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_completions_habit 
            ON completions(habit_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_completions_date 
            ON completions(completion_date)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_habit(self, habit: Habit) -> int:
        """
        Save a new habit to the database.
        
        Args:
            habit: The Habit object to save
        
        Returns:
            The auto-generated habit_id from the database
        
        Example:
            >>> habit = Habit("Exercise", Periodicity.DAILY)
            >>> habit_id = db.save_habit(habit)
            >>> print(f"Saved with ID: {habit_id}")
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO habits (name, periodicity, created_date)
            VALUES (?, ?, ?)
        ''', (
            habit.name,
            habit.periodicity.value,
            habit.created_date.isoformat()
        ))
        
        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return habit_id
    
    def save_completion(self, habit_id: int, timestamp: datetime) -> None:
        """
        Record a habit completion in the database.
        
        Args:
            habit_id: ID of the habit that was completed
            timestamp: When it was completed
        
        Example:
            >>> db.save_completion(habit_id=5, timestamp=datetime.now())
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO completions (habit_id, completion_date)
            VALUES (?, ?)
        ''', (habit_id, timestamp.isoformat()))
        
        conn.commit()
        conn.close()
    
    def load_all_habits(self) -> List[Habit]:
        """
        Load all habits from the database with their completion history.
        
        Returns:
            List of Habit objects with all their completions
        
        Example:
            >>> habits = db.load_all_habits()
            >>> for habit in habits:
            >>>     print(f"{habit.name}: {len(habit.completions)} completions")
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load all habits
        cursor.execute('SELECT habit_id, name, periodicity, created_date FROM habits')
        habit_rows = cursor.fetchall()
        
        habits = []
        for row in habit_rows:
            habit_id, name, periodicity_str, created_date_str = row
            
            # Load completions for this habit
            cursor.execute('''
                SELECT completion_date FROM completions 
                WHERE habit_id = ?
                ORDER BY completion_date
            ''', (habit_id,))
            
            completion_rows = cursor.fetchall()
            completions = [
                datetime.fromisoformat(comp[0]) 
                for comp in completion_rows
            ]
            
            # Create Habit object
            habit = Habit(
                name=name,
                periodicity=Periodicity(periodicity_str),
                habit_id=habit_id,
                created_date=datetime.fromisoformat(created_date_str),
                completions=completions
            )
            habits.append(habit)
        
        conn.close()
        return habits
    
    def delete_habit(self, habit_id: int) -> bool:
        """
        Delete a habit and all its completions from the database.
        
        CASCADE DELETE ensures all related completions are automatically removed.
        
        Args:
            habit_id: ID of the habit to delete
        
        Returns:
            True if habit was deleted, False if not found
        
        Example:
            >>> if db.delete_habit(5):
            >>>     print("Habit deleted successfully")
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if habit exists
        cursor.execute('SELECT habit_id FROM habits WHERE habit_id = ?', (habit_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Delete habit (completions will be cascade deleted)
        cursor.execute('DELETE FROM habits WHERE habit_id = ?', (habit_id,))
        
        conn.commit()
        conn.close()
        return True
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """
        Load a single habit by its ID.
        
        Args:
            habit_id: The ID of the habit to load
        
        Returns:
            Habit object if found, None otherwise
        """
        all_habits = self.load_all_habits()
        for habit in all_habits:
            if habit.habit_id == habit_id:
                return habit
        return None
    
    def clear_all_data(self) -> None:
        """
        Delete all habits and completions (for testing purposes).
        
        WARNING: This removes ALL data from the database!
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM completions')
        cursor.execute('DELETE FROM habits')
        
        conn.commit()
        conn.close()
