"""
habit.py - Habit Class Module

This file defines the Habit class that represents a single habit.
Each habit has a name, periodicity (daily/weekly), creation date, and completion history.
"""

from enum import Enum
from datetime import datetime
from typing import List, Optional


class Periodicity(Enum):
    """
    Enumeration for habit periodicities.
    Using an enum prevents invalid values and provides type safety.
    """
    DAILY = "daily"
    WEEKLY = "weekly"


class Habit:
    """
    Represents a single habit that a user wants to track.
    
    Attributes:
        habit_id (int): Unique identifier (assigned by database)
        name (str): Description of the habit (e.g., "Drink 8 glasses of water")
        periodicity (Periodicity): Either DAILY or WEEKLY
        created_date (datetime): When the habit was first created
        completions (List[datetime]): All timestamps when the habit was completed
    
    Example:
        >>> habit = Habit("Exercise 30 minutes", Periodicity.DAILY)
        >>> habit.complete_task()  # Marks it as done right now
        >>> print(habit.name)
        Exercise 30 minutes
    """
    
    def __init__(
        self, 
        name: str, 
        periodicity: Periodicity,
        habit_id: Optional[int] = None,
        created_date: Optional[datetime] = None,
        completions: Optional[List[datetime]] = None
    ):
        """
        Initialize a new Habit.
        
        Args:
            name: What the habit is (e.g., "Read for 20 minutes")
            periodicity: DAILY or WEEKLY
            habit_id: Database ID (None for new habits, assigned when saved)
            created_date: When created (defaults to now if not provided)
            completions: List of completion timestamps (defaults to empty list)
        """
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_date = created_date if created_date else datetime.now()
        self.completions = completions if completions else []
    
    def complete_task(self, timestamp: Optional[datetime] = None) -> None:
        """
        Mark the habit as completed at a specific time.
        
        Args:
            timestamp: When the task was completed (defaults to current time)
        
        Example:
            >>> habit.complete_task()  # Completed now
            >>> habit.complete_task(datetime(2026, 1, 15, 10, 30))  # Completed at specific time
        """
        completion_time = timestamp if timestamp else datetime.now()
        self.completions.append(completion_time)
        # Keep completions sorted chronologically for easier streak calculations
        self.completions.sort()
    
    def get_completion_dates(self) -> List[datetime]:
        """
        Get all completion timestamps for this habit.
        
        Returns:
            List of datetime objects when the habit was completed
        """
        return self.completions.copy()
    
    def __repr__(self) -> str:
        """
        String representation for debugging.
        
        Returns:
            String showing habit name, periodicity, and completion count
        """
        return f"Habit(id={self.habit_id}, name='{self.name}', " \
               f"periodicity={self.periodicity.value}, " \
               f"completions={len(self.completions)})"
    
    def __str__(self) -> str:
        """
        User-friendly string representation.
        
        Returns:
            Readable string for displaying to users
        """
        return f"{self.name} ({self.periodicity.value}) - {len(self.completions)} completions"
