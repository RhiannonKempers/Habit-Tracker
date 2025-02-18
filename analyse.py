from db import get_habits, get_streak_counter
import sqlite3

def calculate_best_streak(db):
    """
    Calculates the habit with the best (longest) streak.

    Args:
        db (sqlite3.Connection): The database connection object.

    Returns:
        Counter: The habit with the best streak, or None if no habits exist.
    """
    habits = get_habits(db)  # Retrieve all habit names from the database
    best_streak = None  # Initialize the variable to store the best streak

    # Iterate through each habit to find the best streak
    for habit_name in habits:
        habit = get_streak_counter(db, habit_name)  # Retrieve the Counter object for the habit
        if habit:  # Check if the habit exists
            streak = habit.count(db)  # Get the current streak count for the habit
            if best_streak is None or streak > best_streak.count(db):  # Compare the current streak with the best streak found so far
                best_streak = habit  # Update the best streak if the current streak is longer

    return best_streak  # Return the habit with the best streak


def calculate_worst_streak(db):
    """
    Calculates the habit with the worst (shortest) streak.

    Args:
        db (sqlite3.Connection): The database connection object.

    Returns:
        Counter: The habit with the worst streak, or None if no habits exist.
    """
    habits = get_habits(db)  # Retrieve all habit names from the database
    worst_streak = None  # Initialize the variable to store the worst streak

    # Iterate through each habit to find the worst streak
    for habit_name in habits:
        habit = get_streak_counter(db, habit_name)  # Retrieve the Counter object for the habit
        if habit:  # Check if the habit exists
            streak = habit.count(db)  # Get the current streak count for the habit
            if worst_streak is None or streak < worst_streak.count(db):  # Compare the current streak with the worst streak found so far
                worst_streak = habit  # Update the worst streak if the current streak is shorter

    return worst_streak  # Return the habit with the worst streak

def calculate_all_streaks(db):
    """
    Calculates the streak for each habit in the database.

    Args:
        db (sqlite3.Connection): The database connection object.

    Returns:
        dict: A dictionary where keys are habit names and values are their corresponding streak counts.
             Returns an empty dictionary if there are no habits.
    """
    habits = get_habits(db)
    all_streaks = {}

    for habit_name in habits:
        habit = get_streak_counter(db, habit_name)  # Retrieve the Counter object for the habit
        if habit:  # Check if the habit exists (not None)
            streak = habit.count(db)  # Calculate the streak count for the habit
            all_streaks[habit_name] = streak  # Store the streak count in the dictionary, using habit name as the key

    return all_streaks  # Return the dictionary containing streaks for all habits

def calculate_longest_streak_by_periodicity(db, periodicity):
    """
    Calculates the longest streak for habits with a specific periodicity.

    Args:
        db (sqlite3.Connection): The database connection object.
        periodicity (str): The periodicity to filter by ('daily', 'weekly', 'monthly').

    Returns:
        Counter: The habit with the longest streak for the given periodicity,
                 or None if no habits with that periodicity exist.
    """
    habits = get_habits_periodicity(db, periodicity)  # Get habit names with the specified periodicity
    longest_streak_habit = None  # Initialize variable to store the habit with the longest streak
    longest_streak_count = 0  # Initialize variable to store the length of the longest streak

    # Iterate through each habit with the specified periodicity
    for habit_name in habits:
        habit = get_streak_counter(db, habit_name)  # Get the Counter object for the habit
        if habit:
            streak = habit.count(db)  # Calculate the streak count for the habit
            # Check if the current streak is longer than the longest streak found so far
            if streak > longest_streak_count:
                longest_streak_count = streak  # Update the longest streak count
                longest_streak_habit = habit  # Update the habit with the longest streak

    return longest_streak_habit  # Return the habit with the longest streak, or None if no habits exist
