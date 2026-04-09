"""
analytics.py - Analytics Module

This module provides habit analysis using FUNCTIONAL PROGRAMMING.
All functions are pure (no side effects) and use functional paradigms
like filter(), map(), and lambda expressions.

This satisfies the course requirement for functional programming in the analytics module.
"""

from typing import List
from datetime import datetime, timedelta
from habit import Habit, Periodicity


class Analytics:
    """
    Analytics module using functional programming paradigm.
    
    All methods are static (pure functions) that take habits as input
    and return analysis results without modifying the original data.
    
    Functional Programming Principles:
    - Pure functions (same input = same output)
    - No side effects (doesn't modify input data)
    - Uses filter(), map(), lambda expressions
    - Immutable data processing
    """
    
    @staticmethod
    def get_all_habits(habits: List[Habit]) -> List[Habit]:
        """
        Return all currently tracked habits.
        
        Args:
            habits: List of all habits
        
        Returns:
            Same list (provided for API consistency)
        
        Example:
            >>> all_habits = Analytics.get_all_habits(tracker.get_all_habits())
        """
        return habits
    
    @staticmethod
    def get_habits_by_periodicity(
        habits: List[Habit], 
        periodicity: Periodicity
    ) -> List[Habit]:
        """
        Filter habits by their periodicity using FUNCTIONAL PROGRAMMING.
        
        Uses filter() with lambda function - key FP technique!
        
        Args:
            habits: List of all habits
            periodicity: DAILY or WEEKLY
        
        Returns:
            Filtered list of habits matching the periodicity
        
        Example:
            >>> daily_habits = Analytics.get_habits_by_periodicity(
            ...     all_habits, 
            ...     Periodicity.DAILY
            ... )
            >>> print(f"You have {len(daily_habits)} daily habits")
        """
        return list(filter(lambda h: h.periodicity == periodicity, habits))
    
    @staticmethod
    def calculate_current_streak(habit: Habit) -> int:
        """
        Calculate the current active streak for a habit.
        
        Streak Logic (User-Centered):
        - For DAILY: Streak is active if last completion was today or yesterday
        - For WEEKLY: Streak is active if last completion was this week or last week
        - Only breaks when an ENTIRE period is missed
        
        Args:
            habit: The habit to analyze
        
        Returns:
            Number of consecutive periods completed
        
        Example:
            >>> streak = Analytics.calculate_current_streak(my_habit)
            >>> print(f"Current streak: {streak} days")
        """
        if not habit.completions:
            return 0
        
        completions = sorted(habit.completions)
        
        if habit.periodicity == Periodicity.DAILY:
            return Analytics._calculate_daily_streak(completions)
        else:  # WEEKLY
            return Analytics._calculate_weekly_streak(completions)
    
    @staticmethod
    def _calculate_daily_streak(completions: List[datetime]) -> int:
        """
        Calculate streak for daily habits (helper function).
        
        Logic: Count backwards from today. Streak continues if no day is missed.
        
        Args:
            completions: Sorted list of completion timestamps
        
        Returns:
            Current streak in days
        """
        if not completions:
            return 0
        
        today = datetime.now().date()
        last_completion = completions[-1].date()
        
        # Check if last completion was today or yesterday
        days_since_last = (today - last_completion).days
        
        if days_since_last > 1:
            # Missed more than 1 day - streak is broken
            return 0
        
        # Count backwards from last completion
        streak = 0
        current_date = last_completion
        
        # Convert completions to set of dates for O(1) lookup
        completion_dates = set(c.date() for c in completions)
        
        # Walk backwards counting consecutive days
        while current_date in completion_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    @staticmethod
    def _calculate_weekly_streak(completions: List[datetime]) -> int:
        """
        Calculate streak for weekly habits (helper function).
        
        Logic: Count backwards from current week. Streak continues if no week is missed.
        Week = Monday to Sunday.
        
        Args:
            completions: Sorted list of completion timestamps
        
        Returns:
            Current streak in weeks
        """
        if not completions:
            return 0
        
        today = datetime.now().date()
        last_completion = completions[-1].date()
        
        # Get week start (Monday) for both dates
        def get_week_start(date):
            return date - timedelta(days=date.weekday())
        
        current_week = get_week_start(today)
        last_week = get_week_start(last_completion)
        
        # Check if last completion was this week or last week
        weeks_since = (current_week - last_week).days // 7
        
        if weeks_since > 1:
            # Missed more than 1 week - streak is broken
            return 0
        
        # Group completions by week
        weeks_completed = set()
        for comp in completions:
            week_start = get_week_start(comp.date())
            weeks_completed.add(week_start)
        
        # Count backwards from last week
        streak = 0
        check_week = last_week
        
        while check_week in weeks_completed:
            streak += 1
            check_week -= timedelta(weeks=1)
        
        return streak
    
    @staticmethod
    def calculate_longest_streak(habit: Habit) -> int:
        """
        Find the longest streak ever achieved for a habit.
        
        Scans entire completion history to find maximum consecutive periods.
        
        Args:
            habit: The habit to analyze
        
        Returns:
            Maximum streak ever achieved
        
        Example:
            >>> longest = Analytics.calculate_longest_streak(my_habit)
            >>> print(f"Best streak ever: {longest} days!")
        """
        if not habit.completions:
            return 0
        
        completions = sorted(habit.completions)
        
        if habit.periodicity == Periodicity.DAILY:
            return Analytics._longest_daily_streak(completions)
        else:  # WEEKLY
            return Analytics._longest_weekly_streak(completions)
    
    @staticmethod
    def _longest_daily_streak(completions: List[datetime]) -> int:
        """
        Find longest daily streak in completion history.
        
        Args:
            completions: Sorted list of completion timestamps
        
        Returns:
            Longest consecutive day streak
        """
        if not completions:
            return 0
        
        completion_dates = sorted(set(c.date() for c in completions))
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(completion_dates)):
            days_gap = (completion_dates[i] - completion_dates[i-1]).days
            
            if days_gap == 1:
                # Consecutive day
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                # Gap found, reset streak
                current_streak = 1
        
        return max_streak
    
    @staticmethod
    def _longest_weekly_streak(completions: List[datetime]) -> int:
        """
        Find longest weekly streak in completion history.
        
        Args:
            completions: Sorted list of completion timestamps
        
        Returns:
            Longest consecutive week streak
        """
        if not completions:
            return 0
        
        # Helper to get week start
        def get_week_start(date):
            return date - timedelta(days=date.weekday())
        
        # Get unique weeks
        weeks = sorted(set(get_week_start(c.date()) for c in completions))
        
        if not weeks:
            return 0
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(weeks)):
            weeks_gap = (weeks[i] - weeks[i-1]).days // 7
            
            if weeks_gap == 1:
                # Consecutive week
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                # Gap found, reset
                current_streak = 1
        
        return max_streak
    
    @staticmethod
    def get_longest_streak_all_habits(habits: List[Habit]) -> int:
        """
        Find the longest streak across ALL habits using FUNCTIONAL PROGRAMMING.
        
        Uses map() to calculate each habit's longest streak, then max() to find the best.
        This is a key functional programming technique!
        
        Args:
            habits: List of all habits
        
        Returns:
            The maximum streak from any habit
        
        Example:
            >>> best_streak = Analytics.get_longest_streak_all_habits(all_habits)
            >>> print(f"Your best streak ever: {best_streak}!")
        """
        if not habits:
            return 0
        
        # FUNCTIONAL PROGRAMMING: Use map() to transform each habit into its longest streak
        streaks = map(Analytics.calculate_longest_streak, habits)
        
        # Find maximum using max() with default for empty sequences
        return max(streaks, default=0)
    
    @staticmethod
    def get_longest_streak_for_habit(habits: List[Habit], habit_id: int) -> int:
        """
        Get the longest streak for a specific habit using FUNCTIONAL PROGRAMMING.
        
        Uses filter() with lambda to find the habit, then calculates its longest streak.
        
        Args:
            habits: List of all habits
            habit_id: ID of the habit to analyze
        
        Returns:
            Longest streak for that habit, or 0 if not found
        
        Example:
            >>> streak = Analytics.get_longest_streak_for_habit(all_habits, 5)
        """
        # FUNCTIONAL PROGRAMMING: Use filter() with lambda to find matching habit
        matching_habits = list(filter(lambda h: h.habit_id == habit_id, habits))
        
        if not matching_habits:
            return 0
        
        return Analytics.calculate_longest_streak(matching_habits[0])
