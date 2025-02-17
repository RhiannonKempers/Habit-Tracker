from datetime import datetime, timedelta
import random
from counter import Counter
from db import get_db, get_streak_counter, add_habit

def example_data():
    """
    Populates the database with example habit data, including random completion dates for the past 4 weeks.
    """
    db = get_db()
    cur = db.cursor()

    # Add example habits to the database
    add_habit(db, "Study", "Learn or revise for at least 1hr", "daily")
    add_habit(db, "Laundry", "Wash, dry, fold, and put away a load of laundry", "weekly")
    add_habit(db, "Journaling", "Journal for at least 30 minutes", "daily")
    add_habit(db, "Vacuum", "Vacuum every room in the flat", "weekly")
    add_habit(db, "Dishes", "Wash up all dishes before going to bed", "daily")

    habits = ["Study", "Laundry", "Journaling", "Vacuum", "Dishes"]

    # Iterate through each habit and add completion data for the past 4 weeks
    for habit_name in habits:
        habit = get_streak_counter(db, habit_name)
        if habit:
            today = datetime.now()
            for i in range(4):  # 4 weeks
                if habit.periodicity == "daily":
                    increment_date = today - timedelta(days=i)
                    # Add a random chance to skip a day (75% chance of completion)
                    if random.random() < 0.75:
                        habit.increment(db, increment_date.strftime("%Y-%m-%d"))
                elif habit.periodicity == "weekly":
                    increment_date = today - timedelta(weeks=i)
                    # Add a random chance to skip a week (80% chance of completion)
                    if random.random() < 0.8:
                        habit.increment(db, increment_date.strftime("%Y-%m-%d"))
                elif habit.periodicity == "monthly":
                    # Incrementing monthly habits every 30 days
                    increment_date = today - timedelta(days=i * 30)
                    # Add a random chance to skip a month (70% chance of completion)
                    if random.random() < 0.7:
                        habit.increment(db, increment_date.strftime("%Y-%m-%d"))
        else:
            print(f"Habit '{habit_name}' not found in the database.")

example_data()
