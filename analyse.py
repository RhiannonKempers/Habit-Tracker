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
