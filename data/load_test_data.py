"""
load_test_data.py - Test Fixture Data Loader

This script loads 5 predefined habits with 4 weeks of completion data.
This data is used for testing and demonstration purposes.

Data Period: December 26, 2025 - January 22, 2026 (4 weeks / 28 days)
"""

from datetime import datetime, timedelta
from database import DatabaseManager
from tracker import HabitTracker
from habit import Periodicity


# Base date for test data: December 26, 2025
BASE_DATE = datetime(2025, 12, 26, 8, 0, 0)


def load_test_data(tracker: HabitTracker, clear_existing: bool = False) -> None:
    """
    Load 5 predefined habits with 4 weeks of test data.
    
    Habits:
    1. "Drink 8 glasses of water" (daily) - 25/28 completions (89%)
    2. "Exercise 30 minutes" (daily) - 20/28 completions (71%)
    3. "Read for 20 minutes" (daily) - 28/28 completions (100% - perfect!)
    4. "Weekly meal prep" (weekly) - 3/4 completions (75%)
    5. "Clean the house" (weekly) - 4/4 completions (100% - perfect!)
    
    Args:
        tracker: HabitTracker instance to load data into
        clear_existing: If True, clears all existing data first
    """
    if clear_existing:
        print("⚠️  Clearing existing data...")
        tracker.db_manager.clear_all_data()
        tracker.load_habits()  # Refresh from empty database
    
    print("\n📊 Loading 5 predefined habits with 4 weeks of test data...\n")
    
    # ==========================================
    # HABIT 1: Drink 8 glasses of water (DAILY)
    # ==========================================
    # Pattern: Very consistent - 25/28 days completed (89% success)
    # Missing: Days 8, 15, 23 (0-indexed: 7, 14, 22)
    print("1️⃣  Creating 'Drink 8 glasses of water' (daily)...")
    
    habit1 = tracker.create_habit("Drink 8 glasses of water", Periodicity.DAILY)
    habit1.created_date = BASE_DATE
    
    for day in range(28):
        if day not in [7, 14, 22]:  # Skip these days
            completion_time = BASE_DATE + timedelta(days=day, hours=10, minutes=30)
            tracker.complete_habit_task(habit1.habit_id, completion_time)
    
    print(f"   ✅ Added 25 completions (89% completion rate)")
    
    # ==========================================
    # HABIT 2: Exercise 30 minutes (DAILY)
    # ==========================================
    # Pattern: Inconsistent - 20/28 days (71% success)
    # Shows broken streaks and irregular patterns
    print("\n2️⃣  Creating 'Exercise 30 minutes' (daily)...")
    
    habit2 = tracker.create_habit("Exercise 30 minutes", Periodicity.DAILY)
    habit2.created_date = BASE_DATE
    
    completed_days = [0, 2, 3, 4, 5, 6, 7, 8, 11, 13, 14, 15, 17, 18, 19, 22, 23, 24, 25, 26]
    for day in completed_days:
        completion_time = BASE_DATE + timedelta(days=day, hours=18, minutes=0)
        tracker.complete_habit_task(habit2.habit_id, completion_time)
    
    print(f"   ✅ Added 20 completions (71% completion rate, irregular streaks)")
    
    # ==========================================
    # HABIT 3: Read for 20 minutes (DAILY)
    # ==========================================
    # Pattern: PERFECT! 28/28 days (100% success)
    # Demonstrates a perfect streak
    print("\n3️⃣  Creating 'Read for 20 minutes' (daily)...")
    
    habit3 = tracker.create_habit("Read for 20 minutes", Periodicity.DAILY)
    habit3.created_date = BASE_DATE
    
    for day in range(28):
        completion_time = BASE_DATE + timedelta(days=day, hours=21, minutes=0)
        tracker.complete_habit_task(habit3.habit_id, completion_time)
    
    print(f"   ✅ Added 28 completions (100% - PERFECT STREAK! 🔥)")
    
    # ==========================================
    # HABIT 4: Weekly meal prep (WEEKLY)
    # ==========================================
    # Pattern: 3/4 weeks completed (75% success)
    # Missed week 3
    print("\n4️⃣  Creating 'Weekly meal prep' (weekly)...")
    
    habit4 = tracker.create_habit("Weekly meal prep", Periodicity.WEEKLY)
    habit4.created_date = BASE_DATE
    
    weekly_completions = [
        BASE_DATE + timedelta(days=0, hours=14, minutes=0),   # Week 1 - Thursday
        BASE_DATE + timedelta(days=10, hours=15, minutes=30), # Week 2 - Sunday
        # Week 3 - MISSED
        BASE_DATE + timedelta(days=24, hours=13, minutes=0),  # Week 4 - Saturday
    ]
    
    for completion in weekly_completions:
        tracker.complete_habit_task(habit4.habit_id, completion)
    
    print(f"   ✅ Added 3 completions (75% - missed week 3)")
    
    # ==========================================
    # HABIT 5: Clean the house (WEEKLY)
    # ==========================================
    # Pattern: PERFECT! 4/4 weeks (100% success)
    # Always completed on Saturdays
    print("\n5️⃣  Creating 'Clean the house' (weekly)...")
    
    habit5 = tracker.create_habit("Clean the house", Periodicity.WEEKLY)
    habit5.created_date = BASE_DATE
    
    weekly_completions = [
        BASE_DATE + timedelta(days=2, hours=10, minutes=0),   # Week 1 - Saturday
        BASE_DATE + timedelta(days=9, hours=10, minutes=0),   # Week 2 - Saturday
        BASE_DATE + timedelta(days=16, hours=10, minutes=0),  # Week 3 - Saturday
        BASE_DATE + timedelta(days=23, hours=10, minutes=0),  # Week 4 - Saturday
    ]
    
    for completion in weekly_completions:
        tracker.complete_habit_task(habit5.habit_id, completion)
    
    print(f"   ✅ Added 4 completions (100% - PERFECT WEEKLY STREAK! 🏆)")
    
    # Reload habits to reflect all changes
    tracker.load_habits()
    
    print("\n" + "="*60)
    print("✅ TEST DATA LOADED SUCCESSFULLY!")
    print("="*60)
    print(f"Total habits: 5")
    print(f"Data period: Dec 26, 2025 - Jan 22, 2026 (4 weeks)")
    print(f"\nData includes:")
    print(f"  - 3 daily habits (2 with varied patterns, 1 perfect)")
    print(f"  - 2 weekly habits (1 with missed week, 1 perfect)")
    print(f"  - Perfect streaks, broken streaks, and various completion rates")
    print("="*60 + "\n")


def main():
    """
    Run this script directly to load test data.
    
    Usage:
        python load_test_data.py
    """
    print("\n🔧 Test Data Loader")
    print("="*60)
    
    # Initialize database and tracker
    db = DatabaseManager("data/habits.db")
    tracker = HabitTracker(db)
    
    # Ask user if they want to clear existing data
    if tracker.get_habits_count() > 0:
        print(f"\n⚠️  Database currently has {tracker.get_habits_count()} habits.")
        response = input("Clear existing data before loading test data? (yes/no): ").strip().lower()
        clear_existing = (response == "yes")
    else:
        clear_existing = False
    
    # Load test data
    load_test_data(tracker, clear_existing)
    
    print("💡 Tip: Run 'python main.py' to start the habit tracker!")


if __name__ == "__main__":
    main()
