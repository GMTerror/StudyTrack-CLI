import mysql.connector
from mysql.connector import Error
import datetime as dt
import os

# Connection to the database

try:
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='studytrack')
except Error as e:
    print(f"Error connecting to the database: {e.msg}")

cursor = cnx.cursor()

# Creating the table if it doesn't exist

tables = {}
tables["study_sessions"] = """CREATE TABLE IF NOT EXISTS study_sessions(Date date, Topic varchar(30), Subject varchar(15), TimeStudied int, Completion int, Remarks text);"""
tables["u_test"] = """CREATE TABLE IF NOT EXISTS upcoming_tests(ExamDate date, Subject varchar(15), Series char(12), Portions text, Status char(3));"""
tables["assignments"] = """CREATE TABLE IF NOT EXISTS assignments(DueDate date, Subject varchar(15), Topic varchar(30), Status char(3));"""

for table in tables:
    try:
        cursor.execute(tables[table])
        cnx.commit()
    except Error as e:
        print(f"Error creating table {table}: {e.msg}")

# Menu
def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("StudyTrack CLI - Main Menu\n")
    print("1. Add Study Session")
    print("2. View Study Sessions")
    print("3. Add Tests")
    print("4. View Upcoming Tests")
    print("5. Add Assignments")
    print("6. View Assignments")
    print("7. Exit\n")
    funs = [add_study_session, view_study_sessions, add_test,
        view_upcoming_tests, add_assignment, view_assignments, print]
    
    try:
        funs[int(input("Select an option (1-7): ")) -1]()
    except (ValueError, IndexError):
        print("\nInvalid Option. Please try again.")
        input("Press ENTER to continue...")
        menu()

# Add Study Session
def add_study_session():
    x = True
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Study Session\n")
        date = input("Date (YYYY-MM-DD) or press ENTER for current date: ")
        if date == "":
            date = dt.date.today().strftime("%Y-%m-%d")
        topic = input("Topic: ")
        subject = input("Subject: ")
        try:
            time_studied = int(input("Time Studied (in hours): "))
            completion = int(input("Completion (%): "))
        except ValueError:
            print("\nPlease enter valid numeric values for Time Studied and Completion.")
            input("Press ENTER to try again...")
            continue
        remarks = input("Remarks: ")

        add_session = ("INSERT INTO study_sessions "
                    "(Date, Topic, Subject, TimeStudied, Completion, Remarks) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
        data_session = (date, topic, subject, time_studied, completion, remarks)

        try:
            cursor.execute(add_session, data_session)
            cnx.commit()
            print("\nStudy session added successfully!")
        except Error as e:
            print(f"\nError adding study session: {e.msg}")
        
        x = False if input("\nPress 1 to add new or Enter to return to the main menu... ") != "1" else True

    menu()

# View Study Sessions
def view_study_sessions():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Study Sessions\n")
    try:
        cursor.execute("SELECT * FROM study_sessions ORDER BY Date DESC")
        data = cursor.fetchmany(10)
        for r in data:
            remarks = r[5] if len(r[5]) < 20 else r[5][:17] + "..."
            print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} hrs | {r[4]}% | {remarks}")
    except Error as e:
        print(f"Error retrieving study sessions: {e.msg}")

    input("\nPress ENTER to return to main menu...")
    menu()

# Add Upcoming Tests
def add_test():
    x = True
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Test\n")
        exam_date = input("Exam Date (YYYY-MM-DD): ")
        subject = input("Subject: ")
        series = input("Series: ")
        portions = input("Portions (comma-seperated topics): ")
        status = input("Status (S/NS/R) [For Studied/Not Studied/Revised]: ")

        add_test = ("INSERT INTO upcoming_tests "
                    "(ExamDate, Subject, Series, Portions, Status) "
                    "VALUES (%s, %s, %s, %s, %s)")
        data_test = (exam_date, subject, series, portions, status)

        try:
            cursor.execute(add_test, data_test)
            cnx.commit()
            print("\nTest added successfully!")
        except Error as e:
            print(f"\nError adding upcoming test: {e.msg}")
        
        x = False if input("\nPress 1 to add new or Enter to return to the main menu... ") != "1" else True

    menu()

# View Upcoming Tests
def view_upcoming_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Upcoming Tests\n")
    today = dt.datetime.now().strftime("%Y-%m-%d")
    mon = (dt.datetime.now() + dt.timedelta(days=31)).strftime("%Y-%m-%d")
    try:
        cursor.execute(f"SELECT * FROM upcoming_tests WHERE ExamDate > '{today}' and ExamDate < '{mon}' ORDER BY ExamDate")
        data = cursor.fetchall()
        for r in data:
            remarks = "Studied" if r[4] == "S" else "Not Studied" if r[4] == "NS" else "Revised"
            print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {remarks}")
    except Error as e:
        print(f"Error retrieving study sessions: {e.msg}")

    input("\nPress ENTER to return to main menu...")
    menu()

# Add Assignments
def add_assignment():
    x = True
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Assignment\n")
        due_date = input("Due Date (YYYY-MM-DD): ")
        subject = input("Subject: ")
        topic = input("Topic: ")
        status = input("Status (S/NS) [For Submitted/Not Submitted]: ")

        add_assign = ("INSERT INTO assignments "
                    "(DueDate, Subject, Topic, Status) "
                    "VALUES (%s, %s, %s, %s)")
        data_assign = (due_date, subject, topic, status)

        try:
            cursor.execute(add_assign, data_assign)
            cnx.commit()
            print("\nAssignment added successfully!")
        except Error as e:
            print(f"\nError adding assignment: {e.msg}")
        
        x = False if input("\nPress 1 to add new or Enter to return to the main menu... ") != "1" else True

    menu()

# View Assignments
def view_assignments():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Assignments\n")
    today = dt.datetime.now().strftime("%Y-%m-%d")
    week = (dt.datetime.now() + dt.timedelta(days=7)).strftime("%Y-%m-%d")
    try:
        cursor.execute(f"SELECT * FROM assignments WHERE DueDate > '{today}' and DueDate < '{week}' ORDER BY DueDate")
        data = cursor.fetchall()
        for r in data:
            remarks = "Submitted" if r[3] == "S" else "Not Submitted"
            print(f"{r[0]} | {r[1]} | {r[2]} | {remarks}")
    except Error as e:
        print(f"Error retrieving assignments: {e.msg}")

    input("\nPress ENTER to return to main menu...")
    menu()

# Main Loop
menu()

cnx.commit()
cnx.close()

"""Add Updating Columns in all functions."""