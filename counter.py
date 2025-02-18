from datetime import datetime, timedelta
import sqlite3

class Counter:
    """
    Represents a habit counter with methods for tracking and managing habit streaks.
    """

    def __init__(self, name, description, periodicity, habit_id=None, last_completed=None):
        """
        Initializes a Counter object.

        Args:
            name (str): The name of the habit.
            description (str): A brief description of the habit.
            periodicity (str): The frequency of the habit (e.g., "daily", "weekly", "monthly").
            habit_id (int, optional): The ID of the habit in the database. Defaults to None.
            last_completed (datetime, optional): The last date the habit was completed. Defaults to None.
        """
        self.id = habit_id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now()
        self.last_completed = last_completed

    def store(self, db):
        """
        Stores the habit in the database.

        Args:
            db (sqlite3.Connection): The database connection object.

        Raises:
            ValueError: If the database connection is None.
        """
        if db is None:
            raise ValueError("Database connection is required.")

        try:
            cur = db.cursor()
            cur.execute('''INSERT INTO tracker (name, description, periodicity, creation_date, last_completed)
                            VALUES (?, ?, ?, ?, ?)''',
                        (self.name, self.description, self.periodicity, self.creation_date, self.last_completed))
            db.commit()
            self.id = cur.lastrowid
            print(f"Stored habit with ID: {self.id}")
        except sqlite3.IntegrityError:
            print(f"Counter '{self.name}' already exists.")
        except sqlite3.Error as e:
            print(f"An error occurred while storing the counter: {e}")

    def increment(self, db, increment_date=None):
        """
        Increments the habit counter in the database.

        Args:
            db (sqlite3.Connection): The database connection object.
            increment_date (str, optional): The date the habit was completed (YYYY-MM-DD). Defaults to None (today).
        """
        if increment_date is None:
            increment_date = datetime.now()
        else:
            increment_date = datetime.strptime(increment_date, "%Y-%m-%d")

        cur = db.cursor()

        if self.is_streak_valid(increment_date):
            cur.execute('''INSERT INTO counter (habit_id, increment_date) VALUES (?, ?)''', (self.id, increment_date))
        else:
            cur.execute('''DELETE FROM counter WHERE habit_id = ?''', (self.id,))
            cur.execute('''INSERT INTO counter (habit_id, increment_date) VALUES (?, ?)''', (self.id, increment_date))

        cur.execute('''UPDATE tracker SET last_completed = ? WHERE id = ?''',
                    (increment_date, self.id))
        db.commit()
        self.last_completed = increment_date
        print(f"Habit {self.name} (ID: {self.id}) completed successfully on {increment_date}!")

    def is_streak_valid(self, current_date):
        """
        Checks if the current date is a valid continuation of the habit streak.

        Args:
            current_date (datetime): The date to check.

        Returns:
            bool: True if the date is a valid continuation, False otherwise.
        """
        if not self.last_completed:
            return False

        if self.periodicity == "daily":
            return (current_date - self.last_completed) <= timedelta(days=1)
        elif self.periodicity == "weekly":
            return (current_date - self.last_completed) <= timedelta(weeks=1)
        elif self.periodicity == "monthly":
            return (current_date - self.last_completed) <= timedelta(days=30)  #approximation
        return False

    def reset(self, db):
        """
        Resets the habit counter by deleting all entries from the counter table.

        Args:
            db (sqlite3.Connection): The database connection object.
        """
        try:
            cur = db.cursor()
            cur.execute('''DELETE FROM counter WHERE habit_id = ?''', (self.id,))
            db.commit()
        except sqlite3.IntegrityError:
            print("Invalid counter name.")

    def count(self, db):
        """
        Counts the number of times the habit has been completed.

        Args:
            db (sqlite3.Connection): The database connection object.

        Returns:
            int: The number of times the habit has been completed.
        """
        cur = db.cursor()
        query = '''SELECT COUNT(*) FROM counter WHERE habit_id = ?'''
        cur.execute(query, (self.id,))
        result = cur.fetchone()[0]
        return result

    def remove(self, db):
        """
        Removes the habit from the tracker and counter tables.

        Args:
            db (sqlite3.Connection): The database connection object.

        Raises:
            ValueError: If the database connection is None.
        """
        if db is None:
            raise ValueError("Database connection is required.")

        try:
            cur = db.cursor()
            cur.execute('''DELETE FROM tracker WHERE name = ?''', (self.name,))
            cur.execute('''DELETE FROM counter WHERE habit_id = ?''', (self.id,))
            db.commit()
            print(f"Habit '{self.name}' removed successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while removing the habit: {e}")
