import questionary
from counter import Counter
from analyse import calculate_best_streak, calculate_worst_streak
from db import get_db, get_habits_periodicity, get_habits, get_streak_counter

def is_supported_terminal():
    """
    Checks if the script is running in a supported terminal.

    Returns:
        bool: True if the terminal is supported, False otherwise. Currently always True.
    """
    return True


def cli():
    """
    The main command-line interface function.  Handles user interaction and manages habits.
    """
    db = get_db()  # Get the database connection

    if not is_supported_terminal():
        print("This script requires a Windows console (e.g., cmd.exe or PowerShell). Exiting.")
        sys.exit(1)


    while True:  # Main loop for the CLI
        choice = questionary.select(
            "What do you want to do?",
            choices=["Add Habit", "Remove Habit", "Complete Habit", "See Streak", "Analyse", "Exit"]
        ).ask() #Prompt the user to select an action

        if choice == "Add Habit":
            name = questionary.text("What's the name of your counter?").ask() #Get habit name from user
            desc = questionary.text("What's the description of your counter?").ask() #Get habit description
            periodicity = questionary.select(
                "What's the periodicity of your counter?", choices=["daily", "weekly", "monthly"]
            ).ask() #Get habit periodicity
            counter = Counter(name, desc, periodicity) #Create a Counter object
            counter.store(db) #Store the counter in the database
            print(f"Habit {name} added successfully!")

        elif choice == "Remove Habit":
            name = questionary.text("What's the name of your counter?").ask() #Get habit name to remove
            habit = get_streak_counter(db, name) #Retrieve the habit from the database
            if habit:
                habit.remove(db) #Remove the habit from the database
            else:
                print(f"No habit found with name {name}") #Inform user if habit is not found

        elif choice == "Complete Habit":
            habits = get_habits(db) #Get list of all habits
            if not habits:
                print("No habits found. Add a habit first.") #Inform user if no habits exist
                continue  #Skip to the next iteration of the while loop

            name = questionary.select(
                "Which habit would you like to complete?",
                choices=habits #Present user with list of habits to select
            ).ask()

            habit = get_streak_counter(db, name) #Retrieve selected habit from the database
            if habit:
                habit.increment(db) #Increment the habit counter
            else:
                print(f"No habit found with name {name}") #Inform user if habit is not found

        elif choice == "See Streak":
            habits = get_habits(db) #Get list of all habits
            if not habits:
                print("No habits found. Add a habit first.") #Inform user if no habits exist
                continue #Skip to the next iteration of the while loop

            name = questionary.select(
                "Which habit streak would you like to see?",
                choices=habits #Present user with list of habits to select
            ).ask()

            counter = get_streak_counter(db, name) #Retrieve selected habit from the database
            if counter:
                print(f"The current streak for {name} is {counter.count(db)}") #Display the current streak
            else:
                print(f"No habit found with name {name}") #Inform user if habit is not found

        elif choice == "Analyse":
            analysis_choice = questionary.select("What analysis would you like to do?",
                                                 choices=["List all habits", "List habits by periodicity", "Worst habit", "Best habit", "Back"]).ask() #Present user with analysis options
            if analysis_choice == "List all habits":
                habits = get_habits(db) #Retrieve all habits from the database
                print("Habits:")
                for habit in habits:
                    print(habit)
            elif analysis_choice == "List habits by periodicity":
                periodicity = questionary.select("What periodicity would you like to see?", choices=["daily", "weekly", "monthly"]).ask() #Get periodicity from user
                habits = get_habits_periodicity(db, periodicity) #Retrieve habits with selected periodicity
                print(f"Habits with {periodicity} periodicity:")
                for habit in habits:
                    print(habit)
            elif analysis_choice == "Shortest streak":
                habit = calculate_shortest_streak(db)
                if habit:
                    print(f"The shortest streak is {habit.name} with a streak of {habit.count(db)}")
                else:
                    print("No habits found")
            elif analysis_choice == "Longest streak":
                habit = calculate_longest_streak(db)
                if habit:
                    print(f"The Longest streak is {habit.name} with a streak of {habit.count(db)}")
                else:
                    print("No habits found")
            elif analysis_choice == "All streaks":
                all_streaks = calculate_all_streaks(db)  # Retrieve all habit streaks
                if all_streaks:
                    print("All Habit Streaks:")
                    for habit, streak in all_streaks.items():  # Iterate through habit streaks
                        print(f"{habit}: {streak}")
                else:
                    print("No habits found.")
            elif analysis_choice == "Longest streak by periodicity":
                periodicity = questionary.select(
                    "What periodicity would you like to see the longest streak for?",
                    choices=["daily", "weekly", "monthly"]
                ).ask()  # Get periodicity from user
                longest_streak_habit = calculate_longest_streak_by_periodicity(db, periodicity)
                if longest_streak_habit:
                    print(
                        f"The longest streak for {periodicity} habits is {longest_streak_habit.name} with a streak of {longest_streak_habit.count(db)}")
                else:
                    print(f"No {periodicity} habits found.")  # Inform user if no habits with periodicity exist


        elif choice == "Exit":
            print("Goodbye!")
            break

if __name__ == '__main__':
    cli() #Execute the cli function if the script is run directly
