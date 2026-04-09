"""
tracker.py - HabitTracker Module

This file defines the HabitTracker class that manages all habits.
It coordinates between habit objects and the database.
"""

from typing import List, Optional
from datetime import datetime
from habit import Habit, Periodicity
from database import DatabaseManager


class HabitTracker:
    """
    Manages the collection of all user habits.
    
    This class acts as the coordinator between the Habit objects
    and the DatabaseManager. It provides a clean API for the CLI
    to create, delete, and complete habits.
    
    Example:
        >>> db = DatabaseManager()
        >>> tracker = HabitTracker(db)
        >>> habit = tracker.create_habit("Exercise", Periodicity.DAILY)
        >>> tracker.complete_habit_task(habit.habit_id)
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the tracker with a database manager.
        
        Args:
            db_manager: Instance of DatabaseManager for persistence
        """
        self.db_manager = db_manager
        self.habits: List[Habit] = []
        self.load_habits()  # Load existing habits from database
    
    def create_habit(self, name: str, periodicity: Periodicity) -> Habit:
        """
        Create a new habit and save it to the database.
        
        Args:
            name: Description of the habit
            periodicity: DAILY or WEEKLY
        
        Returns:
            The newly created Habit object with assigned ID
        
        Example:
            >>> habit = tracker.create_habit("Drink water", Periodicity.DAILY)
            >>> print(f"Created habit #{habit.habit_id}")
        """
        # Create new habit object
        habit = Habit(name=name, periodicity=periodicity)
        
        # Save to database and get assigned ID
        habit_id = self.db_manager.save_habit(habit)
        habit.habit_id = habit_id
        
        # Add to in-memory list
        self.habits.append(habit)
        
        return habit
    
    def delete_habit(self, habit_id: int) -> bool:
        """
        Delete a habit by its ID.
        
        Args:
            habit_id: The unique identifier of the habit to delete
        
        Returns:
            True if deleted successfully, False if habit not found
        
        Example:
            >>> if tracker.delete_habit(5):
            >>>     print("Habit deleted!")
            >>> else:
            >>>     print("Habit not found")
        """
        # Remove from database
        success = self.db_manager.delete_habit(habit_id)
        
        # Remove from in-memory list if deletion was successful
        if success:
            self.habits = [h for h in self.habits if h.habit_id != habit_id]
        
        return success
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """
        Retrieve a habit by its ID.
        
        Args:
            habit_id: The unique identifier of the habit
        
        Returns:
            Habit object if found, None otherwise
        
        Example:
            >>> habit = tracker.get_habit_by_id(3)
            >>> if habit:
            >>>     print(habit.name)
        """
        for habit in self.habits:
            if habit.habit_id == habit_id:
                return habit
        return None
    
    def get_all_habits(self) -> List[Habit]:
        """
        Get all currently tracked habits.
        
        Returns:
            List of all Habit objects
        
        Example:
            >>> for habit in tracker.get_all_habits():
            >>>     print(habit.name)
        """
        return self.habits.copy()
    
    def load_habits(self) -> None:
        """
        Load all habits from the database into memory.
        
        This is called during initialization and can be called again
        to refresh the in-memory list from the database.
        
        Example:
            >>> tracker.load_habits()  # Refresh from database
        """
        self.habits = self.db_manager.load_all_habits()
    
    def complete_habit_task(
        self, 
        habit_id: int, 
        timestamp: Optional[datetime] = None
    ) -> bool:
        """
        Mark a habit as completed at a specific time.
        
        Args:
            habit_id: ID of the habit to complete
            timestamp: When it was completed (defaults to now)
        
        Returns:
            True if successful, False if habit not found
        
        Example:
            >>> # Complete habit now
            >>> tracker.complete_habit_task(5)
            
            >>> # Complete habit at specific time (for test data)
            >>> tracker.complete_habit_task(5, datetime(2026, 1, 15, 10, 0))
        """
        habit = self.get_habit_by_id(habit_id)
        
        if not habit:
            return False
        
        # Determine timestamp (use current time if not provided)
        completion_time = timestamp if timestamp else datetime.now()
        
        # Add completion to habit object
        habit.complete_task(completion_time)
        
        # Save completion to database
        self.db_manager.save_completion(habit_id, completion_time)
        
        return True
    
    def get_habits_count(self) -> int:
        """
        Get the total number of tracked habits.
        
        Returns:
            Number of habits currently being tracked
        """
        return len(self.habits)
    
    def __repr__(self) -> str:
        """
        String representation for debugging.
        
        Returns:
            String showing number of habits being tracked
        """
        return f"HabitTracker(habits={len(self.habits)})"
