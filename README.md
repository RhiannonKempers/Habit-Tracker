# My Habit Tracker Project
A Habit tracker created for IU course Object Oriented and Functional Programming with python.



## What is it?
A simple python habit tracker with a Command Line Interface. 
You can create, complete, and remove habits easily. Habits can also be displayed or analysed. 


## Installation
1. Clone the repository from GitHub
2. Run this command to stall the requirements
```shell
pip install -r requirements.txt
```

## Using the example data
This app comes with 4 weeks of example data. To load this run the following command in the Command Prompt Terminal

```shell
python example_data.py
```

## Usage
In the Command Prompt Terminal:
```shell
python main.py
```

Use the arrow keys to select from the menu, press enter to select. 

## Files
- `main.py`: contains the cli function which defines the user interface.
- `counter.py`:contains the counter class, which handles habit managing and tracking
- `db.py`: contains the functions that interact with the database
- `analyse.py`:contains the functions that calculate the best and worst streaks 
- `test_project.py`: is the test suite for the application
- `example_data.py`: contains 4 weeks of data

## Analysis
There are 6 analysis options:
- List all habits
- List all habits by periodicity
- Habit with the longest streak
- Habit with the shortest streak
- List all streaks
- Longest streak by periodicty

## Tests
Pytest is included in the requirements, so run the following command to test the app:
````shell
pytest .
````
