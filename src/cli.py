"""
cli.py - Command Line Interface Module

This file provides the interactive menu system for users to interact
with the habit tracker through the command line.
"""

from habit import Periodicity
from tracker import HabitTracker
from analytics import Analytics


class CLI:
    """
    Command-Line Interface for the Habit Tracker.
    
    Provides an interactive menu system allowing users to:
    - Create and delete habits
    - Complete habit tasks
    - View all habits
    - Analyze habits (streaks, statistics)
    
    Example:
        >>> cli = CLI(tracker)
        >>> cli.run()  # Starts the interactive menu
    """
    
    def __init__(self, tracker: HabitTracker):
        """
        Initialize the CLI with a habit tracker.
        
        Args:
            tracker: HabitTracker instance to manage habits
        """
        self.tracker = tracker
    
    def run(self) -> None:
        """
        Start the interactive CLI menu loop.
        
        Displays the main menu and processes user choices until exit.
        """
        print("\n" + "="*50)
        print("🎯 WELCOME TO HABIT TRACKER!")
        print("="*50)
        
        while True:
            self._display_main_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                self._create_habit_menu()
            elif choice == "2":
                self._complete_task_menu()
            elif choice == "3":
                self._view_all_habits_menu()
            elif choice == "4":
                self._delete_habit_menu()
            elif choice == "5":
                self._analytics_menu()
            elif choice == "6":
                print("\n👋 Thank you for using Habit Tracker!")
                print("Keep building those habits! 💪\n")
                break
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
            
            input("\nPress Enter to continue...")
    
    def _display_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Create a new habit")
        print("2. Complete a habit task")
        print("3. View all habits")
        print("4. Delete a habit")
        print("5. Analytics & Reports")
        print("6. Exit")
    
    def _create_habit_menu(self) -> None:
        """
        Handle habit creation workflow.
        
        Prompts user for habit name and periodicity, then creates the habit.
        """
        print("\n" + "="*50)
        print("CREATE NEW HABIT")
        print("="*50)
        
        # Get habit name
        name = input("Enter habit name: ").strip()
        if not name:
            print("❌ Habit name cannot be empty.")
            return
        
        # Get periodicity
        print("\nSelect periodicity:")
        print("  1 - Daily (complete every day)")
        print("  2 - Weekly (complete at least once per week)")
        
        period_choice = input("Enter choice (1-2): ").strip()
        
        if period_choice == "1":
            periodicity = Periodicity.DAILY
        elif period_choice == "2":
            periodicity = Periodicity.WEEKLY
        else:
            print("❌ Invalid choice.")
            return
        
        # Create habit
        habit = self.tracker.create_habit(name, periodicity)
        
        print(f"\n✅ Habit '{habit.name}' ({periodicity.value}) created successfully!")
        print(f"   Habit ID: {habit.habit_id}")
    
    def _complete_task_menu(self) -> None:
        """
        Handle task completion workflow.
        
        Shows list of habits, prompts user to select one, then marks it complete.
        """
        print("\n" + "="*50)
        print("COMPLETE A HABIT TASK")
        print("="*50)
        
        habits = self.tracker.get_all_habits()
        
        if not habits:
            print("\n❌ No habits found. Create a habit first!")
            return
        
        # Display habits with current streaks
        print(f"\n{'ID':<5} | {'Habit Name':<35} | {'Period':<8} | Current Streak")
        print("-" * 80)
        
        for habit in habits:
            current_streak = Analytics.calculate_current_streak(habit)
            period = habit.periodicity.value
            streak_unit = "days" if period == "daily" else "weeks"
            streak_text = f"{current_streak} {streak_unit}"
            
            print(f"{habit.habit_id:<5} | {habit.name:<35} | {period:<8} | {streak_text}")
        
        # Get user choice
        try:
            habit_id = int(input("\nEnter habit ID to complete (0 to cancel): ").strip())
            
            if habit_id == 0:
                print("❌ Cancelled.")
                return
            
            # Complete the task
            success = self.tracker.complete_habit_task(habit_id)
            
            if success:
                habit = self.tracker.get_habit_by_id(habit_id)
                new_streak = Analytics.calculate_current_streak(habit)
                period_unit = "days" if habit.periodicity == Periodicity.DAILY else "weeks"
                
                print(f"\n✅ Task completed for '{habit.name}'!")
                print(f"   Current streak: {new_streak} {period_unit}")
                
                # Motivational messages
                if new_streak >= 7 and habit.periodicity == Periodicity.DAILY:
                    print("   🔥 You're on fire! A full week!")
                elif new_streak >= 21 and habit.periodicity == Periodicity.DAILY:
                    print("   🏆 Amazing! 3 weeks strong!")
                elif new_streak >= 4 and habit.periodicity == Periodicity.WEEKLY:
                    print("   🎉 One full month! Keep it up!")
            else:
                print(f"\n❌ Habit ID {habit_id} not found.")
        
        except ValueError:
            print("\n❌ Please enter a valid number.")
    
    def _view_all_habits_menu(self) -> None:
        """
        Display all habits grouped by periodicity.
        """
        print("\n" + "="*50)
        print("ALL HABITS OVERVIEW")
        print("="*50)
        
        habits = self.tracker.get_all_habits()
        
        if not habits:
            print("\n❌ No habits found. Create a habit first!")
            return
        
        # Group by periodicity
        daily = Analytics.get_habits_by_periodicity(habits, Periodicity.DAILY)
        weekly = Analytics.get_habits_by_periodicity(habits, Periodicity.WEEKLY)
        
        # Display daily habits
        if daily:
            print("\n📅 DAILY HABITS:")
            print("─" * 50)
            for habit in daily:
                self._display_habit_details(habit)
        
        # Display weekly habits
        if weekly:
            print("\n📆 WEEKLY HABITS:")
            print("─" * 50)
            for habit in weekly:
                self._display_habit_details(habit)
    
    def _display_habit_details(self, habit) -> None:
        """
        Display detailed information about a single habit.
        
        Args:
            habit: The Habit object to display
        """
        current_streak = Analytics.calculate_current_streak(habit)
        longest_streak = Analytics.calculate_longest_streak(habit)
        period_unit = "days" if habit.periodicity == Periodicity.DAILY else "weeks"
        
        print(f"\n  {habit.habit_id}. {habit.name}")
        print(f"     Created: {habit.created_date.strftime('%Y-%m-%d')}")
        print(f"     Total completions: {len(habit.completions)}")
        
        if current_streak == 0:
            print(f"     Current streak: 0 {period_unit} (needs attention)")
        else:
            print(f"     Current streak: {current_streak} {period_unit}")
        
        print(f"     Longest streak: {longest_streak} {period_unit}")
    
    def _delete_habit_menu(self) -> None:
        """
        Handle habit deletion workflow with confirmation.
        """
        print("\n" + "="*50)
        print("DELETE HABIT")
        print("="*50)
        print("⚠️  WARNING: This will permanently delete the habit and all its history.")
        
        habits = self.tracker.get_all_habits()
        
        if not habits:
            print("\n❌ No habits to delete.")
            return
        
        # Display habits
        print(f"\n{'ID':<5} | {'Habit Name':<35} | Period")
        print("-" * 60)
        for habit in habits:
            print(f"{habit.habit_id:<5} | {habit.name:<35} | {habit.periodicity.value}")
        
        # Get user choice
        try:
            habit_id = int(input("\nEnter habit ID to delete (0 to cancel): ").strip())
            
            if habit_id == 0:
                print("❌ Cancelled.")
                return
            
            habit = self.tracker.get_habit_by_id(habit_id)
            if not habit:
                print(f"\n❌ Habit ID {habit_id} not found.")
                return
            
            # Confirm deletion
            confirm = input(f"\nAre you sure you want to delete '{habit.name}'? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                self.tracker.delete_habit(habit_id)
                print("\n✅ Habit deleted successfully.")
            else:
                print("\n❌ Deletion cancelled.")
        
        except ValueError:
            print("\n❌ Please enter a valid number.")
    
    def _analytics_menu(self) -> None:
        """
        Display analytics submenu with various analysis options.
        """
        while True:
            print("\n" + "="*50)
            print("ANALYTICS & REPORTS")
            print("="*50)
            print("1. View all daily habits")
            print("2. View all weekly habits")
            print("3. Show longest streak (all habits)")
            print("4. Show longest streak for specific habit")
            print("5. Return to main menu")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            habits = self.tracker.get_all_habits()
            
            if choice == "1":
                self._show_habits_by_periodicity(Periodicity.DAILY)
            elif choice == "2":
                self._show_habits_by_periodicity(Periodicity.WEEKLY)
            elif choice == "3":
                self._show_longest_streak_all(habits)
            elif choice == "4":
                self._show_longest_streak_specific(habits)
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice.")
            
            if choice in ["1", "2", "3", "4"]:
                input("\nPress Enter to continue...")
    
    def _show_habits_by_periodicity(self, periodicity: Periodicity) -> None:
        """
        Show all habits of a specific periodicity.
        
        Args:
            periodicity: DAILY or WEEKLY
        """
        period_name = periodicity.value.capitalize()
        print(f"\n=== {period_name} Habits ===\n")
        
        habits = self.tracker.get_all_habits()
        filtered = Analytics.get_habits_by_periodicity(habits, periodicity)
        
        if not filtered:
            print(f"No {period_name.lower()} habits found.")
            return
        
        for habit in filtered:
            current = Analytics.calculate_current_streak(habit)
            longest = Analytics.calculate_longest_streak(habit)
            unit = "days" if periodicity == Periodicity.DAILY else "weeks"
            
            print(f"{habit.habit_id}. {habit.name}")
            print(f"   Current: {current} {unit} | Best: {longest} {unit}")
        
        print(f"\nTotal {period_name.lower()} habits: {len(filtered)}")
    
    def _show_longest_streak_all(self, habits) -> None:
        """
        Show the longest streak across all habits.
        
        Args:
            habits: List of all habits
        """
        print("\n=== Longest Streak (All Habits) ===\n")
        
        if not habits:
            print("No habits found.")
            return
        
        longest = Analytics.get_longest_streak_all_habits(habits)
        
        # Find which habit has this streak
        for habit in habits:
            if Analytics.calculate_longest_streak(habit) == longest:
                period_unit = "days" if habit.periodicity == Periodicity.DAILY else "weeks"
                print(f"🏆 Best Performance: {longest} {period_unit}")
                print(f"   Habit: {habit.name}")
                print(f"   Type: {habit.periodicity.value}")
                break
    
    def _show_longest_streak_specific(self, habits) -> None:
        """
        Show longest streak for a user-selected habit.
        
        Args:
            habits: List of all habits
        """
        if not habits:
            print("\nNo habits found.")
            return
        
        # Show habits
        print(f"\n{'ID':<5} | Habit Name")
        print("-" * 40)
        for habit in habits:
            print(f"{habit.habit_id:<5} | {habit.name}")
        
        try:
            habit_id = int(input("\nEnter habit ID: ").strip())
            longest = Analytics.get_longest_streak_for_habit(habits, habit_id)
            
            habit = self.tracker.get_habit_by_id(habit_id)
            if habit:
                period_unit = "days" if habit.periodicity == Periodicity.DAILY else "weeks"
                print(f"\n=== Streak Analysis for '{habit.name}' ===")
                print(f"\nLongest streak ever: {longest} {period_unit}")
                print(f"Total completions: {len(habit.completions)}")
            else:
                print(f"\n❌ Habit ID {habit_id} not found.")
        
        except ValueError:
            print("\n❌ Please enter a valid number.")
