import sqlite3

from counter import Counter

def get_db(name='main.db'):
    """
    Connects to the SQLite database, creating tables if they don't exist.

    Args:
        name (str, optional): The name of the database file. Defaults to 'main.db'.

    Returns:
        sqlite3.Connection: The database connection object.  Returns None if connection fails.
    """
    try:
        db = sqlite3.connect(name)
        cur = db.cursor()

        # Create the tracker table if it doesn't exist
        cur.execute('''CREATE TABLE IF NOT EXISTS tracker
                        (id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE,
                        description TEXT,
                        periodicity TEXT,
                        creation_date TEXT,
                        last_completed TEXT)''')

        # Create the counter table if it doesn't exist
        cur.execute('''CREATE TABLE IF NOT EXISTS counter
                        (id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        increment_date TEXT,
                        FOREIGN KEY (habit_id) REFERENCES tracker(id))''')

        # Check if the 'last_completed' column exists in the tracker table; if not, add it
        cur.execute("PRAGMA table_info(tracker)")
        columns = [column[1] for column in cur.fetchall()]
        if 'last_completed' not in columns:
            cur.execute("ALTER TABLE tracker ADD COLUMN last_completed TEXT")

        db.commit()
        return db

    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None  # Important: Return None to indicate failure

def add_habit(db, name, description, periodicity):
    """
    Adds a new habit to the tracker table.

    Args:
        db (sqlite3.Connection): The database connection object.
        name (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (str): The periodicity of the habit (e.g., 'daily', 'weekly', 'monthly').

    Raises:
        ValueError: If the database connection is None.
    """
    if db is None:
        raise ValueError("Database connection is required.")

    try:
        cur = db.cursor()
        cur.execute('''INSERT INTO tracker (name, description, periodicity) VALUES (?, ?, ?)''', (name, description, periodicity))
        db.commit()
    except sqlite3.Error as e:
        print(f"Error adding habit: {e}")

def get_habits(db):
    """
    Retrieves a list of all habit names from the tracker table.

    Args:
        db (sqlite3.Connection): The database connection object.

    Returns:
        list: A list of habit names (strings).
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM tracker")
    return [row[0] for row in cur.fetchall()]

def get_habits_periodicity(db, periodicity):
    """
    Retrieves a list of habit names with a specific periodicity.

    Args:
        db (sqlite3.Connection): The database connection object.
        periodicity (str): The periodicity to filter by (e.g., 'daily', 'weekly', 'monthly').

    Returns:
        list: A list of habit names (strings) with the specified periodicity.
    """
    cur = db.cursor()
    cur.execute('''SELECT name FROM tracker WHERE periodicity = ?''', (periodicity,))
    rows = cur.fetchall()
    return [row[0] for row in rows]

def get_streak_counter(db, name):
    """
    Retrieves a Counter object from the database based on the habit name.

    Args:
        db (sqlite3.Connection): The database connection object.
        name (str): The name of the habit.

    Returns:
        Counter: A Counter object representing the habit, or None if the habit is not found.
    """
    cur = db.cursor()
    cur.execute('''SELECT * FROM tracker WHERE name = ?''', (name,))
    habit_data = cur.fetchone()

    if habit_data:
        return Counter(habit_data[1], habit_data[2], habit_data[3], habit_id=habit_data[0], last_completed=habit_data[5])
    else:
        return None
