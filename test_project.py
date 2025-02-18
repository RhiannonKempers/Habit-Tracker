import pytest
from analyse import calculate_best_streak, calculate_worst_streak
from counter import Counter
from db import get_streak_counter, get_db


class TestHabitTracker:
    """Test suite for the Habit Tracker application."""

    def setup_method(self):
        """
        Set up the test environment before each test method.

        This method:
        1. Connects to a test database
        2. Clears existing data from the counter and tracker tables
        3. Creates and stores two test habits
        """
        self.db = get_db('test.db')
        if self.db is None:
            raise ValueError("Failed to establish database connection")

        cur = self.db.cursor()
        cur.execute("DELETE FROM counter")
        cur.execute("DELETE FROM tracker")
        self.db.commit()

        self.habit1 = Counter("test_habit_1", "test_desc_1", "daily")
        self.habit2 = Counter("test_habit_2", "test_desc_2", "weekly")

        self.habit1.store(self.db)
        self.habit2.store(self.db)

        print(f"Habit1 ID: {self.habit1.id}")
        print(f"Habit2 ID: {self.habit2.id}")

    def test_streak_calculation(self):
        """
        Test the streak calculation functionality.

        This test:
        1. Increments habits with specific dates
        2. Verifies streak counts
        3. Tests best and worst streak calculations
        """
        # Increment habit1 with multiple dates
        for date in ["2025-01-30", "2025-02-01", "2025-02-03", "2025-02-04"]:
            self.habit1.increment(self.db, date)

        # Increment habit2 with a single date
        self.habit2.increment(self.db, "2025-01-30")

        # Retrieve and print streak information for habit1
        test_streak = get_streak_counter(self.db, "test_habit_1")
        print(f"Habit ID: {test_streak.id}")
        print(f"Habit Name: {test_streak.name}")
        print(f"Habit Count: {test_streak.count(self.db)}")

        # Perform a direct database query to verify the count
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) FROM counter WHERE habit_id = ?", (test_streak.id,))
        direct_count = cur.fetchone()[0]
        print(f"Direct database count: {direct_count}")

        # Assert that the streak count is correct
        assert test_streak.count(self.db) == 2, "Streak count for habit1 should be 2"

        # Test the best streak calculation
        best_streak = calculate_longest_streak(self.db)
        assert best_streak.name == "test_habit_1", "Best streak should be test_habit_1"
        assert best_streak.count(self.db) == 2, "Best streak count should be 2"

        # Test the worst streak calculation
        worst_streak = calculate_shortest_streak(self.db)
        assert worst_streak.name == "test_habit_2", "Worst streak should be test_habit_2"
        assert worst_streak.count(self.db) == 1, "Worst streak count should be 1"

    def teardown_method(self):
        """Clean up after each test method by closing the database connection."""
        if self.db:
            self.db.close()
