"""
Employee Directory Manager
==========================
A beginner-friendly, menu-driven console application to manage employee records.

Key Python Concepts Used:
- Dictionaries: Store all employee records using Employee ID as the unique key.
- Tuples: Store immutable date values (Birth Date and Joining Date) as (Year, Month, Day).
- Input Validation & Exception Handling: Keep the program safe from invalid inputs.
"""

from datetime import date
import re


# ---------------------------------------------------------------------------
# Helper Functions for Formatting and Input Validation
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    """Print a clean, framed section header in the console."""
    width = 64
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def format_date_tuple(date_tuple: tuple[int, int, int]) -> str:
    """
    Convert a (year, month, day) tuple into a readable YYYY-MM-DD string.
    Example: (1995, 4, 18) -> "1995-04-18"
    """
    year, month, day = date_tuple
    return f"{year:04d}-{month:02d}-{day:02d}"


def validate_employee_id(emp_id: str) -> str:
    """
    Validate and normalize an Employee ID.
    Rules: Must be 3 to 15 alphanumeric characters (e.g., EMP001).
    """
    cleaned = emp_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{3,15}", cleaned):
        raise ValueError(
            "Employee ID must be 3-15 characters using only letters and numbers (e.g., EMP001)."
        )
    return cleaned


def validate_text_field(value: str, field_name: str, allow_digits: bool = False) -> str:
    """
    Validate a non-empty text field such as Name, Department, or Role.
    """
    cleaned = " ".join(value.strip().split())
    if len(cleaned) < 2:
        raise ValueError(f"{field_name} must be at least 2 characters long.")
    if not allow_digits and any(char.isdigit() for char in cleaned):
        raise ValueError(f"{field_name} cannot contain numbers.")
    return cleaned


def validate_email(email: str) -> str:
    """Validate basic email address format (example: name@company.com)."""
    cleaned = email.strip().lower()
    if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", cleaned):
        raise ValueError("Please enter a valid email address (e.g., user@company.com).")
    return cleaned


def validate_phone(phone: str) -> str:
    """
    Validate a phone number containing 10 to 15 digits.
    Spaces, dashes, and an optional leading '+' are accepted.
    """
    cleaned = phone.strip()
    digits_only = re.sub(r"[\s\-()]", "", cleaned)
    if digits_only.startswith("+"):
        digits_check = digits_only[1:]
    else:
        digits_check = digits_only

    if not digits_check.isdigit() or not (10 <= len(digits_check) <= 15):
        raise ValueError("Phone number must contain 10 to 15 digits.")
    return digits_only


def validate_salary(salary_text: str) -> float:
    """Convert salary input into a positive floating-point number."""
    try:
        salary = float(salary_text.strip().replace(",", ""))
    except ValueError as exc:
        raise ValueError("Salary must be a valid number (e.g., 65000).") from exc

    if salary <= 0:
        raise ValueError("Salary must be greater than 0.")
    return round(salary, 2)


def parse_date_to_tuple(date_text: str, field_name: str) -> tuple[int, int, int]:
    """
    Parse a YYYY-MM-DD date string and return it as a tuple: (year, month, day).
    Using a tuple ensures the stored date parts stay fixed in order.
    """
    cleaned = date_text.strip()
    parts = cleaned.split("-")
    if len(parts) != 3:
        raise ValueError(f"{field_name} must follow YYYY-MM-DD format (e.g., 1998-05-21).")

    try:
        year, month, day = (int(part) for part in parts)
        # datetime.date checks calendar rules (e.g., leap years, days in month).
        parsed_date = date(year, month, day)
    except ValueError as exc:
        raise ValueError(f"Invalid calendar date for {field_name}. Use YYYY-MM-DD.") from exc

    if parsed_date > date.today():
        raise ValueError(f"{field_name} cannot be in the future.")

    return (year, month, day)


def validate_date_relationship(
    birth_tuple: tuple[int, int, int], joining_tuple: tuple[int, int, int]
) -> None:
    """
    Ensure the joining date is logically valid relative to the birth date.
    """
    birth_dt = date(*birth_tuple)
    joining_dt = date(*joining_tuple)

    if joining_dt <= birth_dt:
        raise ValueError("Joining Date must be later than Birth Date.")

    # Calculate age in full years on the joining date.
    age_at_joining = (
        joining_dt.year
        - birth_dt.year
        - ((joining_dt.month, joining_dt.day) < (birth_dt.month, birth_dt.day))
    )
    if age_at_joining < 18:
        raise ValueError("Employee must be at least 18 years old on the Joining Date.")


def prompt_with_validation(prompt_text: str, validator, default_value=None):
    """
    Repeatedly prompt the user until valid input is entered.
    If default_value is provided, pressing Enter keeps the existing value.
    """
    while True:
        try:
            raw_input = input(prompt_text)
            if default_value is not None and raw_input.strip() == "":
                return default_value
            return validator(raw_input)
        except ValueError as error:
            print(f"  [Invalid Input] {error}")


# ---------------------------------------------------------------------------
# Sample Data Setup
# ---------------------------------------------------------------------------

def load_sample_employees() -> dict[str, dict]:
    """
    Create and return initial sample employee records.
    Dictionary Key   -> Employee ID (str)
    Dictionary Value -> Employee details (dict), with Birth Date and Joining Date as tuples.
    """
    return {
        "EMP001": {
            "name": "Aarav Sharma",
            "department": "Engineering",
            "role": "Senior Software Engineer",
            "email": "aarav.sharma@company.com",
            "phone": "9876543210",
            "salary": 92000.00,
            "birth_date": (1994, 4, 18),      # Tuple: (Year, Month, Day)
            "joining_date": (2020, 6, 15),    # Tuple: (Year, Month, Day)
        },
        "EMP002": {
            "name": "Priya Nair",
            "department": "Human Resources",
            "role": "HR Manager",
            "email": "priya.nair@company.com",
            "phone": "9823456789",
            "salary": 78000.00,
            "birth_date": (1991, 11, 5),      # Tuple: (Year, Month, Day)
            "joining_date": (2019, 3, 1),     # Tuple: (Year, Month, Day)
        },
        "EMP003": {
            "name": "Rohan Verma",
            "department": "Finance",
            "role": "Financial Analyst",
            "email": "rohan.verma@company.com",
            "phone": "9911223344",
            "salary": 68500.00,
            "birth_date": (1996, 8, 22),      # Tuple: (Year, Month, Day)
            "joining_date": (2022, 1, 10),    # Tuple: (Year, Month, Day)
        },
        "EMP004": {
            "name": "Sneha Kulkarni",
            "department": "Design",
            "role": "UI/UX Designer",
            "email": "sneha.kulkarni@company.com",
            "phone": "9765432109",
            "salary": 74000.00,
            "birth_date": (1995, 2, 14),      # Tuple: (Year, Month, Day)
            "joining_date": (2021, 9, 20),    # Tuple: (Year, Month, Day)
        },
    }


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------

def display_employee_card(emp_id: str, record: dict) -> None:
    """Print detailed information for a single employee."""
    print("\n" + "-" * 50)
    print(f"  Employee ID  : {emp_id}")
    print(f"  Full Name    : {record['name']}")
    print(f"  Department   : {record['department']}")
    print(f"  Role         : {record['role']}")
    print(f"  Email        : {record['email']}")
    print(f"  Phone        : {record['phone']}")
    print(f"  Salary       : ${record['salary']:,.2f}")
    print(f"  Birth Date   : {format_date_tuple(record['birth_date'])}  (Tuple: {record['birth_date']})")
    print(f"  Joining Date : {format_date_tuple(record['joining_date'])}  (Tuple: {record['joining_date']})")
    print("-" * 50)


# ---------------------------------------------------------------------------
# CRUD Operations
# ---------------------------------------------------------------------------

def create_employee(directory: dict[str, dict]) -> None:
    """Create a new employee record and add it to the dictionary."""
    print_header("ADD NEW EMPLOYEE")

    # 1. Get a unique Employee ID (dictionary key)
    while True:
        emp_id = prompt_with_validation(
            "Enter Employee ID (e.g., EMP005): ", validate_employee_id
        )
        if emp_id in directory:
            print(f"  [Duplicate ID] Employee '{emp_id}' already exists. Try another ID.")
        else:
            break

    # 2. Collect and validate text, contact, and salary details
    name = prompt_with_validation(
        "Enter Full Name: ",
        lambda v: validate_text_field(v, "Full Name"),
    )
    department = prompt_with_validation(
        "Enter Department: ",
        lambda v: validate_text_field(v, "Department", allow_digits=True),
    )
    role = prompt_with_validation(
        "Enter Job Role: ",
        lambda v: validate_text_field(v, "Job Role", allow_digits=True),
    )
    email = prompt_with_validation("Enter Email Address: ", validate_email)
    phone = prompt_with_validation("Enter Phone Number: ", validate_phone)
    salary = prompt_with_validation("Enter Annual Salary ($): ", validate_salary)

    # 3. Collect Birth Date and Joining Date as tuples (YYYY, MM, DD)
    birth_date = prompt_with_validation(
        "Enter Birth Date (YYYY-MM-DD): ",
        lambda v: parse_date_to_tuple(v, "Birth Date"),
    )

    while True:
        joining_date = prompt_with_validation(
            "Enter Joining Date (YYYY-MM-DD): ",
            lambda v: parse_date_to_tuple(v, "Joining Date"),
        )
        try:
            validate_date_relationship(birth_date, joining_date)
            break
        except ValueError as error:
            print(f"  [Invalid Dates] {error}")

    # 4. Store the new employee dictionary under the Employee ID key
    directory[emp_id] = {
        "name": name,
        "department": department,
        "role": role,
        "email": email,
        "phone": phone,
        "salary": salary,
        "birth_date": birth_date,
        "joining_date": joining_date,
    }

    print(f"\n[Success] Employee '{emp_id}' ({name}) added successfully!")


def search_employee(directory: dict[str, dict]) -> None:
    """Search for and view a single employee by Employee ID."""
    print_header("SEARCH / VIEW EMPLOYEE BY ID")

    if not directory:
        print("The employee directory is currently empty.")
        return

    emp_id = prompt_with_validation(
        "Enter Employee ID to search (e.g., EMP001): ", validate_employee_id
    )

    # Dictionary lookup by key (O(1) average time)
    record = directory.get(emp_id)
    if record is None:
        print(f"\n[Not Found] No employee found with ID '{emp_id}'.")
        return

    display_employee_card(emp_id, record)


def view_all_employees(directory: dict[str, dict]) -> None:
    """Display all employees stored in the directory in a formatted table."""
    print_header("ALL EMPLOYEES DIRECTORY")

    if not directory:
        print("No employee records found. Use option 1 to add an employee.")
        return

    header = (
        f"{'ID':<10} {'Name':<20} {'Department':<16} {'Role':<24} "
        f"{'Birth Date':<12} {'Joined':<12} {'Salary':>12}"
    )
    print(header)
    print("-" * len(header))

    # Sort by Employee ID for clean, predictable output
    for emp_id in sorted(directory.keys()):
        emp = directory[emp_id]
        birth_str = format_date_tuple(emp["birth_date"])
        join_str = format_date_tuple(emp["joining_date"])
        print(
            f"{emp_id:<10} {emp['name'][:19]:<20} {emp['department'][:15]:<16} "
            f"{emp['role'][:23]:<24} {birth_str:<12} {join_str:<12} "
            f"${emp['salary']:>11,.2f}"
        )

    print("-" * len(header))
    print(f"Total Employees: {len(directory)}")


def update_employee(directory: dict[str, dict]) -> None:
    """Update an existing employee's details while keeping unchanged fields intact."""
    print_header("UPDATE EMPLOYEE DETAILS")

    if not directory:
        print("The employee directory is currently empty.")
        return

    emp_id = prompt_with_validation(
        "Enter Employee ID to update: ", validate_employee_id
    )
    if emp_id not in directory:
        print(f"\n[Not Found] No employee found with ID '{emp_id}'.")
        return

    current = directory[emp_id]
    print("\nCurrent Details:")
    display_employee_card(emp_id, current)
    print("Tip: Press Enter without typing anything to keep the current value.\n")

    # Prompt each field with its current value as the default
    new_name = prompt_with_validation(
        f"Full Name [{current['name']}]: ",
        lambda v: validate_text_field(v, "Full Name"),
        default_value=current["name"],
    )
    new_department = prompt_with_validation(
        f"Department [{current['department']}]: ",
        lambda v: validate_text_field(v, "Department", allow_digits=True),
        default_value=current["department"],
    )
    new_role = prompt_with_validation(
        f"Job Role [{current['role']}]: ",
        lambda v: validate_text_field(v, "Job Role", allow_digits=True),
        default_value=current["role"],
    )
    new_email = prompt_with_validation(
        f"Email [{current['email']}]: ",
        validate_email,
        default_value=current["email"],
    )
    new_phone = prompt_with_validation(
        f"Phone [{current['phone']}]: ",
        validate_phone,
        default_value=current["phone"],
    )
    new_salary = prompt_with_validation(
        f"Salary [{current['salary']:.2f}]: ",
        validate_salary,
        default_value=current["salary"],
    )

    current_birth_str = format_date_tuple(current["birth_date"])
    current_join_str = format_date_tuple(current["joining_date"])

    while True:
        new_birth = prompt_with_validation(
            f"Birth Date (YYYY-MM-DD) [{current_birth_str}]: ",
            lambda v: parse_date_to_tuple(v, "Birth Date"),
            default_value=current["birth_date"],
        )
        new_join = prompt_with_validation(
            f"Joining Date (YYYY-MM-DD) [{current_join_str}]: ",
            lambda v: parse_date_to_tuple(v, "Joining Date"),
            default_value=current["joining_date"],
        )
        try:
            validate_date_relationship(new_birth, new_join)
            break
        except ValueError as error:
            print(f"  [Invalid Dates] {error}")

    # Save updated record back into the dictionary
    directory[emp_id] = {
        "name": new_name,
        "department": new_department,
        "role": new_role,
        "email": new_email,
        "phone": new_phone,
        "salary": new_salary,
        "birth_date": new_birth,
        "joining_date": new_join,
    }

    print(f"\n[Success] Employee '{emp_id}' updated successfully!")


def delete_employee(directory: dict[str, dict]) -> None:
    """Delete an employee record from the dictionary after user confirmation."""
    print_header("DELETE EMPLOYEE")

    if not directory:
        print("The employee directory is currently empty.")
        return

    emp_id = prompt_with_validation(
        "Enter Employee ID to delete: ", validate_employee_id
    )
    if emp_id not in directory:
        print(f"\n[Not Found] No employee found with ID '{emp_id}'.")
        return

    display_employee_card(emp_id, directory[emp_id])

    # Confirm before permanently removing from the dictionary
    while True:
        confirm = input(f"Are you sure you want to delete '{emp_id}'? (y/n): ").strip().lower()
        if confirm in ("y", "yes"):
            removed = directory.pop(emp_id)
            print(f"\n[Success] Deleted employee '{emp_id}' ({removed['name']}).")
            return
        if confirm in ("n", "no"):
            print("\n[Cancelled] Delete operation aborted.")
            return
        print("  [Invalid Input] Please enter 'y' for yes or 'n' for no.")


# ---------------------------------------------------------------------------
# Main Menu Loop
# ---------------------------------------------------------------------------

def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "+" + "-" * 48 + "+")
    print("|" + "EMPLOYEE DIRECTORY MANAGER".center(48) + "|")
    print("+" + "-" * 48 + "+")
    print("|  1. Create (Add) New Employee                  |")
    print("|  2. Search / View Employee by ID               |")
    print("|  3. View All Employees                         |")
    print("|  4. Update Employee Details                    |")
    print("|  5. Delete Employee                            |")
    print("|  6. Exit                                       |")
    print("+" + "-" * 48 + "+")


def main() -> None:
    """Entry point for the Employee Directory Manager application."""
    # Initialize the directory dictionary with sample records
    employees = load_sample_employees()

    print_header("WELCOME TO EMPLOYEE DIRECTORY MANAGER")
    print(f"Loaded {len(employees)} sample employee records into memory.")

    # Map menu numbers to functions for clean dispatch
    menu_actions = {
        "1": create_employee,
        "2": search_employee,
        "3": view_all_employees,
        "4": update_employee,
        "5": delete_employee,
    }

    while True:
        try:
            display_menu()
            choice = input("Select an option (1-6): ").strip()

            if choice == "6":
                print("\nThank you for using Employee Directory Manager. Goodbye!")
                break

            action = menu_actions.get(choice)
            if action is None:
                print("\n[Invalid Choice] Please enter a number between 1 and 6.")
                continue

            action(employees)

        except (KeyboardInterrupt, EOFError):
            print("\n\nProgram interrupted. Exiting Employee Directory Manager. Goodbye!")
            break
        except Exception as exc:
            # Catch any unexpected runtime errors without crashing the menu loop
            print(f"\n[Unexpected Error] Something went wrong: {exc}")


if __name__ == "__main__":
    main()
