"""
test_habits.py - Unit Tests for Habit Tracker

This file contains pytest unit tests for the habit tracking application.
Tests cover habit creation, streak calculation, analytics, and database operations.

Run tests with: pytest test_habits.py
"""

import pytest
import os
from datetime import datetime, timedelta
from habit import Habit, Periodicity
from database import DatabaseManager
from tracker import HabitTracker
from analytics import Analytics


# ==========================================
# FIXTURES
# ==========================================

@pytest.fixture
def test_db():
    """
    Create a temporary test database.
    Cleans up after tests complete.
    """
    db_path = "data/test_habits.db"
    
    # Create database
    db = DatabaseManager(db_path)
    
    yield db
    
    # Cleanup: remove test database file
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def tracker(test_db):
    """
    Create a HabitTracker instance with clean test database.
    """
    return HabitTracker(test_db)


@pytest.fixture
def daily_habit():
    """
    Create a sample daily habit for testing.
    """
    return Habit("Test Daily Habit", Periodicity.DAILY)


@pytest.fixture
def weekly_habit():
    """
    Create a sample weekly habit for testing.
    """
    return Habit("Test Weekly Habit", Periodicity.WEEKLY)


# ==========================================
# HABIT CLASS TESTS
# ==========================================

def test_habit_creation(daily_habit):
    """Test that a habit can be created with correct attributes."""
    assert daily_habit.name == "Test Daily Habit"
    assert daily_habit.periodicity == Periodicity.DAILY
    assert len(daily_habit.completions) == 0
    assert daily_habit.created_date is not None


def test_habit_complete_task(daily_habit):
    """Test that completing a task adds a completion timestamp."""
    initial_count = len(daily_habit.completions)
    
    daily_habit.complete_task()
    
    assert len(daily_habit.completions) == initial_count + 1
    assert isinstance(daily_habit.completions[0], datetime)


def test_habit_complete_task_with_timestamp(daily_habit):
    """Test completing a task with a specific timestamp."""
    test_time = datetime.now().now().replace(month=4, day=15, hour=10, minute=30, second=0)
    
    daily_habit.complete_task(test_time)
    
    assert len(daily_habit.completions) == 1
    assert daily_habit.completions[0] == test_time


def test_habit_multiple_completions(daily_habit):
    """Test that multiple completions are sorted chronologically."""
    times = [
        datetime.now().now().replace(month=4, day=15, hour=10, minute=0, second=0),
        datetime.now().now().replace(month=4, day=13, hour=10, minute=0, second=0),  # Earlier date
        datetime.now().now().replace(month=4, day=14, hour=10, minute=0, second=0),
    ]
    
    for time in times:
        daily_habit.complete_task(time)
    
    assert len(daily_habit.completions) == 3
    # Check that they're sorted
    assert daily_habit.completions[0] < daily_habit.completions[1] < daily_habit.completions[2]


# ==========================================
# DATABASE TESTS
# ==========================================

def test_database_save_habit(test_db):
    """Test saving a habit to the database."""
    habit = Habit("Database Test Habit", Periodicity.DAILY)
    habit_id = test_db.save_habit(habit)
    
    assert habit_id is not None
    assert isinstance(habit_id, int)
    assert habit_id > 0


def test_database_load_habits(test_db):
    """Test loading habits from the database."""
    # Save two habits
    habit1 = Habit("Habit 1", Periodicity.DAILY)
    habit2 = Habit("Habit 2", Periodicity.WEEKLY)
    
    test_db.save_habit(habit1)
    test_db.save_habit(habit2)
    
    # Load all habits
    loaded_habits = test_db.load_all_habits()
    
    assert len(loaded_habits) == 2
    assert loaded_habits[0].name == "Habit 1"
    assert loaded_habits[1].name == "Habit 2"


def test_database_save_completion(test_db):
    """Test saving a completion to the database."""
    habit = Habit("Test Habit", Periodicity.DAILY)
    habit_id = test_db.save_habit(habit)
    
    test_time = datetime.now().now().replace(month=4, day=15, hour=10, minute=0, second=0)
    test_db.save_completion(habit_id, test_time)
    
    # Load and verify
    loaded_habits = test_db.load_all_habits()
    assert len(loaded_habits[0].completions) == 1
    assert loaded_habits[0].completions[0] == test_time


def test_database_delete_habit(test_db):
    """Test deleting a habit and its completions (CASCADE DELETE)."""
    habit = Habit("To Delete", Periodicity.DAILY)
    habit_id = test_db.save_habit(habit)
    
    # Add completion
    test_db.save_completion(habit_id, datetime.now())
    
    # Delete habit
    success = test_db.delete_habit(habit_id)
    assert success is True
    
    # Verify it's gone
    loaded_habits = test_db.load_all_habits()
    assert len(loaded_habits) == 0


# ==========================================
# TRACKER TESTS
# ==========================================

def test_tracker_create_habit(tracker):
    """Test creating a habit through the tracker."""
    habit = tracker.create_habit("Tracker Test", Periodicity.DAILY)
    
    assert habit.habit_id is not None
    assert habit.name == "Tracker Test"
    assert len(tracker.get_all_habits()) == 1


def test_tracker_complete_habit_task(tracker):
    """Test completing a habit task through the tracker."""
    habit = tracker.create_habit("Complete Test", Periodicity.DAILY)
    
    success = tracker.complete_habit_task(habit.habit_id)
    
    assert success is True
    
    # Verify completion was saved
    tracker.load_habits()  # Refresh from database
    updated_habit = tracker.get_habit_by_id(habit.habit_id)
    assert len(updated_habit.completions) == 1


def test_tracker_delete_habit(tracker):
    """Test deleting a habit through the tracker."""
    habit = tracker.create_habit("Delete Test", Periodicity.DAILY)
    habit_id = habit.habit_id
    
    success = tracker.delete_habit(habit_id)
    
    assert success is True
    assert tracker.get_habit_by_id(habit_id) is None


# ==========================================
# ANALYTICS TESTS - STREAK CALCULATION
# ==========================================

def test_analytics_daily_streak_perfect():
    """Test calculating a perfect daily streak."""
    habit = Habit("Perfect Daily", Periodicity.DAILY)
    
    # Complete for 7 consecutive days
    base_date = datetime.now().now().replace(month=4, day=10, hour=10, minute=0, second=0)
    for day in range(7):
        habit.complete_task(base_date + timedelta(days=day))
    
    streak = Analytics.calculate_current_streak(habit)
    assert streak == 7


def test_analytics_daily_streak_broken():
    """Test that a broken daily streak returns 0."""
    habit = Habit("Broken Daily", Periodicity.DAILY)
    
    # Last completion was 3 days ago (broken)
    three_days_ago = datetime.now() - timedelta(days=3)
    habit.complete_task(three_days_ago)
    
    streak = Analytics.calculate_current_streak(habit)
    assert streak == 0


def test_analytics_daily_streak_active():
    """Test that streak is active if completed yesterday."""
    habit = Habit("Active Daily", Periodicity.DAILY)
    
    # Complete yesterday and today
    yesterday = datetime.now() - timedelta(days=1)
    today = datetime.now()
    
    habit.complete_task(yesterday)
    habit.complete_task(today)
    
    streak = Analytics.calculate_current_streak(habit)
    assert streak == 2


def test_analytics_weekly_streak():
    """Test calculating a weekly streak."""
    habit = Habit("Weekly Test", Periodicity.WEEKLY)
    
    # Complete for 3 consecutive weeks
    base_date = datetime.now().now().replace(month=4, day=6, hour=10, minute=0, second=0)  # Monday
    for week in range(3):
        habit.complete_task(base_date + timedelta(weeks=week))
    
    streak = Analytics.calculate_current_streak(habit)
    assert streak == 3


def test_analytics_longest_streak():
    """Test finding the longest streak."""
    habit = Habit("Longest Test", Periodicity.DAILY)
    
    # Create pattern: 5 days, gap, 3 days, gap, 7 days
    base_date = datetime.now().now().replace(month=4, day=1, hour=10, minute=0, second=0)
    
    # First streak: 5 days
    for day in range(5):
        habit.complete_task(base_date + timedelta(days=day))
    
    # Gap (day 5)
    
    # Second streak: 3 days
    for day in range(7, 10):
        habit.complete_task(base_date + timedelta(days=day))
    
    # Gap (day 10)
    
    # Third streak: 7 days (longest)
    for day in range(12, 19):
        habit.complete_task(base_date + timedelta(days=day))
    
    longest = Analytics.calculate_longest_streak(habit)
    assert longest == 7


# ==========================================
# ANALYTICS TESTS - FUNCTIONAL PROGRAMMING
# ==========================================

def test_analytics_filter_by_periodicity():
    """Test filtering habits by periodicity (uses filter())."""
    habits = [
        Habit("Daily 1", Periodicity.DAILY),
        Habit("Weekly 1", Periodicity.WEEKLY),
        Habit("Daily 2", Periodicity.DAILY),
    ]
    
    daily_habits = Analytics.get_habits_by_periodicity(habits, Periodicity.DAILY)
    weekly_habits = Analytics.get_habits_by_periodicity(habits, Periodicity.WEEKLY)
    
    assert len(daily_habits) == 2
    assert len(weekly_habits) == 1
    assert all(h.periodicity == Periodicity.DAILY for h in daily_habits)


def test_analytics_longest_streak_all_habits():
    """Test finding longest streak across all habits (uses map() and max())."""
    habit1 = Habit("Habit 1", Periodicity.DAILY)
    habit2 = Habit("Habit 2", Periodicity.DAILY)
    
    # Habit 1: 3-day streak
    base_date = datetime.now().now().replace(month=4, day=1, hour=10, minute=0, second=0)
    for day in range(3):
        habit1.complete_task(base_date + timedelta(days=day))
    
    # Habit 2: 5-day streak (longest)
    for day in range(5):
        habit2.complete_task(base_date + timedelta(days=day))
    
    longest = Analytics.get_longest_streak_all_habits([habit1, habit2])
    assert longest == 5


def test_analytics_longest_streak_for_specific_habit():
    """Test finding longest streak for a specific habit."""
    habit1 = Habit("Specific 1", Periodicity.DAILY)
    habit1.habit_id = 1
    habit2 = Habit("Specific 2", Periodicity.DAILY)
    habit2.habit_id = 2
    
    # Habit 1: 4-day streak
    base_date = datetime.now().now().replace(month=4, day=1, hour=10, minute=0, second=0)
    for day in range(4):
        habit1.complete_task(base_date + timedelta(days=day))
    
    # Habit 2: 6-day streak
    for day in range(6):
        habit2.complete_task(base_date + timedelta(days=day))
    
    # Get streak for habit 1 specifically
    streak = Analytics.get_longest_streak_for_habit([habit1, habit2], habit_id=1)
    assert streak == 4


def test_analytics_empty_habits_list():
    """Test analytics functions with empty habits list."""
    empty_list = []
    
    assert Analytics.get_longest_streak_all_habits(empty_list) == 0
    assert len(Analytics.get_habits_by_periodicity(empty_list, Periodicity.DAILY)) == 0


# ==========================================
# INTEGRATION TEST
# ==========================================

def test_full_workflow_integration(tracker):
    """
    Integration test: Create habit, complete tasks, analyze streaks.
    Tests the entire workflow from creation to analytics.
    """
    # Create a habit
    habit = tracker.create_habit("Integration Test", Periodicity.DAILY)
    
    # Complete for 5 consecutive days
    base_date = datetime.now().now().replace(month=4, day=10, hour=10, minute=0, second=0)
    for day in range(5):
        tracker.complete_habit_task(habit.habit_id, base_date + timedelta(days=day))
    
    # Reload to get updated data
    tracker.load_habits()
    updated_habit = tracker.get_habit_by_id(habit.habit_id)
    
    # Verify completions
    assert len(updated_habit.completions) == 5
    
    # Verify streak calculation
    streak = Analytics.calculate_longest_streak(updated_habit)
    assert streak == 5
    
    # Verify analytics functions work
    all_habits = tracker.get_all_habits()
    longest = Analytics.get_longest_streak_all_habits(all_habits)
    assert longest == 5
