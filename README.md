# Employee Directory Manager

A clean, beginner-friendly, menu-driven Python console application for managing employee records in memory using core Python data structures.

## Features

- **Python Dictionary Storage**: Stores employee records in a dictionary using each unique **Employee ID** (e.g., `EMP001`) as the key.
- **Tuple Date Storage**: Stores **Birth Date** and **Joining Date** as immutable 3-element tuples `(Year, Month, Day)`.
- **Full CRUD Operations**:
  - **Create**: Add a new employee with duplicate ID prevention.
  - **Read / Search**: Search and view a specific employee by Employee ID.
  - **View All**: Display all employees in a neatly formatted console table.
  - **Update**: Modify an employee's details (press `Enter` to keep existing values).
  - **Delete**: Remove an employee record with confirmation prompt.
- **Input Validation & Exception Handling**: Validates IDs, names, emails, phone numbers, salaries, calendar dates, and age-at-joining rules without crashing on bad input.
- **Sample Records Included**: Pre-loaded with 4 sample employee records so you can test immediately.

## Folder Structure

```text
Employee_Directory_Manager/
├── main.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.9+ (uses only Python's built-in standard library: `datetime` and `re`; no external packages or database required).

## How to Run

1. Open a terminal and navigate into the project directory:
   ```bash
   cd Employee_Directory_Manager
   ```
2. Run the application:
   ```bash
   python main.py
   ```
   *(On some systems, use `python3 main.py` or `py main.py`.)*
