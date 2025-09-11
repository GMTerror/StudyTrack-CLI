import mysql.connector
from mysql.connector import Error
import datetime as dt
import os
import random

# Creating the database
try:
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
except Error as e:
    print(f"Error connecting to the server: {e.msg}")

cursor = cnx.cursor()

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS studytrack")
except Error as e:
    print(f"Error creating the database: {e.msg}")

cnx.commit()
cnx.close()

# Connection to the database
try:
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='studytrack')
except Error as e:
    print(f"Error connecting to the database: {e.msg}")

cursor = cnx.cursor()

# Creating the table if it doesn't exist
tables = {}
tables["study_sessions"] = """CREATE TABLE IF NOT EXISTS study_sessions(Date date, Topic varchar(30), Subject varchar(15), TimeStudied int, Completion int, Remarks text);"""
tables["tests"] = """CREATE TABLE IF NOT EXISTS tests(ExamDate date, Subject varchar(15), Series char(12), Portions text, Status char(3), MarksObtained int, TotalMarks int);"""
tables["assignments"] = """CREATE TABLE IF NOT EXISTS assignments(DueDate date, Subject varchar(15), Topic varchar(30), Status char(3));"""
tables["syllabus"] = """CREATE TABLE IF NOT EXISTS syllabus(Subject varchar(15) PRIMARY KEY, Chapters text)"""

for table in tables:
    try:
        cursor.execute(tables[table])
        cnx.commit()
    except Error as e:
        print(f"Error creating table {table}: {e.msg}")

# Menu
def menu():
    td, ua = fetch_sub()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("StudyTrack CLI - Main Menu\n")
    if td == "N/A":
        print("First add the syllabus to get subject suggestions here using the 9th option.")
    else:
        print("Today's Subject: ", td)
    if ua != "N/A":
        print("Upcoming Assignment: ", ua)
    print()
    print("1. Progress Report")
    print("2. Add Study Session")
    print("3. View Study Sessions")
    print("4. Add Tests")
    print("5. View Upcoming Tests")
    print("6. View Completed and Marks Added Tests")
    print("7. Add Test Marks")
    print("8. Add Assignments")
    print("9. View Assignments")
    print("10. Add Syllabus (to be done once every semester)")
    print("11. View Syllabus")
    print("12. Exit\n")
    funs = [progress, add_study_session, view_study_sessions, add_test,
        view_upcoming_tests, view_all_tests, add_marks, add_assignment, view_assignments, add_syllabus, view_syllabus, print]
    
    try:
        funs[int(input("Select an option (1-12): ")) -1]()
    except (ValueError, IndexError):
        print("\nInvalid Option. Please try again.")
        input("Press ENTER to continue...")
        menu()

# Progress Report
def progress():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Progress Report\n")
    print("\nStudy Sessions Summary:-\n")
    try:
        cursor.execute("SELECT Subject, SUM(TimeStudied), AVG(Completion) FROM study_sessions GROUP BY Subject")
        data = cursor.fetchall()
        for r in data:
            print(f"{r[0]}: {r[1]} total hrs | {r[2]}% avg completion")
    except Error as e:
        print(f"Error retrieving study sessions summary: {e.msg}\n")

    print("\nTests Summary:-\n")
    try:
        cursor.execute("SELECT Subject, AVG(MarksObtained / TotalMarks) FROM tests GROUP BY Subject")
        data = cursor.fetchall()
        for r in data:
            print(f"{r[0]}: {r[1] * 100}% avg marks")
    except Error as e:
        print(f"Error retrieving test summary: {e.msg}\n")

    print("\nAssignments Summary:-\n")
    try:
        cursor.execute("SELECT count(*) FROM assignments")
        total = cursor.fetchall()[0][0]
        if total == 0:
            print("No assignments added yet.")
        else:
            cursor.execute("SELECT count(*) FROM assignments WHERE Status = 'S'")
            over = cursor.fetchall()[0][0]
            cursor.execute("SELECT count(*) FROM assignments WHERE Status = 'NS' and DueDate < CURDATE()")
            overdue = cursor.fetchall()[0][0]
            print(f"Assignments Submitted: {over}/{total} | {round((over/total)*100, 2)}%")
            print("Assignments Overdue:", overdue)
        
    except Error as e:
        print(f"Error retrieving assignment summary: {e.msg}\n")

    input("\nPress ENTER to return to the main menu...")
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
        subject = input("Subject: ").capitalize().strip()
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
        for r in range(len(data)):
            remarks = data[r][5] if len(data[r][5]) < 20 else data[r][5][:17] + "..."
            print(f"{r+1}. {data[r][0]} | {data[r][1]} | {data[r][2]} | {data[r][3]} hrs | {data[r][4]}% | {remarks}")
    except Error as e:
        print(f"Error retrieving study sessions: {e.msg}")

    c = input("\nPress 1 to UPDATE or ENTER to return to main menu...")
    if c != "1":
        menu()
    else:
        try:
            ss = int(input("Select the study session (number) to update: "))
            to_update = data[ss-1]
        except (ValueError, IndexError):
            print("\nPlease enter a valid option.")
            input("Press ENTER to try again...")
            view_study_sessions()

        os.system('cls' if os.name == 'nt' else ' clear')
        print("Update Study Session\n")
        choice = input("Do you want to remove this study session? (y/n): ")
        if choice == "y":
            try:
                cursor.execute("DELETE FROM study_sessions WHERE Date = %s AND Topic = %s AND Subject = %s AND Remarks = %s", (to_update[0], to_update[1], to_update[2], to_update[5]))
                cnx.commit()
                print("\nStudy session removed successfully!")
            except Error as e:
                print(f"\nError removing study session: {e.msg}")
            input("\nPress ENTER to return...")
            view_study_sessions()
        
        print("Press ENTER to keep the current value.")
        remarks = to_update[5] if len(to_update[5]) < 20 else to_update[5][:17] + "..."
        print(f"Selected: {to_update[0]} | {to_update[1]} | {to_update[2]} | {to_update[3]} hrs | {to_update[4]}% | {remarks}") 
        
        date = input("Date (YYYY-MM-DD): ")
        topic = input("Topic: ")
        subject = input("Subject: ").capitalize().strip()
        try:
            time_studied = int(input("Time Studied (in hours): "))
            completion = int(input("Completion (%): "))
        except ValueError:
            print("\nPlease enter valid numeric values for Time Studied and Completion.")
            input("Press ENTER to try again...")
            view_study_sessions()
        remarks = input("Remarks: ")
        query = ("UPDATE study_sessions SET Date = %s, Topic = %s, Subject = %s, TimeStudied = %s, Completion = %s, Remarks = %s WHERE Date = %s AND Topic = %s AND Subject = %s AND Remarks = %s")
        data_query = (date if date != "" else to_update[0], topic if topic != "" else to_update[1],
                      subject if subject != "" else to_update[2], time_studied if time_studied != "" else to_update[3],
                      completion if completion != "" else to_update[4], remarks if remarks != "" else to_update[5],
                      to_update[0], to_update[1], to_update[2], to_update[5])

        try:
            cursor.execute(query, data_query)
            cnx.commit()
            print("\nStudy Session updated successfully!")
        except Error as e:
            print(f"\nError updating Study Session: {e.msg}")
        input("Press ENTER to return...")
        view_study_sessions()

# Add Upcoming Tests
def add_test():
    x = True
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Test\n")
        exam_date = input("Exam Date (YYYY-MM-DD): ")
        subject = input("Subject: ").capitalize().strip()
        series = input("Series: ").upper()
        portions = input("Portions (comma-seperated topics): ")
        status = input("Status (S/NS/R) [For Studied/Not Studied/Revised]: ").upper()

        add_test = ("INSERT INTO tests "
                    "(ExamDate, Subject, Series, Portions, Status) "
                    "VALUES (%s, %s, %s, %s, %s)")
        data_test = (exam_date, subject, series, portions, status)

        try:
            cursor.execute(add_test, data_test)
            cnx.commit()
            print("\nTest added successfully!")
        except Error as e:
            print(f"\nError adding test: {e.msg}")
        
        x = False if input("\nPress 1 to add new or Enter to return to the main menu... ") != "1" else True

    menu()

# View Upcoming Tests
def view_upcoming_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Upcoming Tests\n")
    today = dt.datetime.now().strftime("%Y-%m-%d")
    mon = (dt.datetime.now() + dt.timedelta(days=31)).strftime("%Y-%m-%d")
    try:
        cursor.execute("SELECT * FROM tests WHERE ExamDate > %s and ExamDate < %s ORDER BY ExamDate", (today, mon))
        data = cursor.fetchall()
        for r in range(len(data)):
            remarks = "Studied" if data[r][4] == "S" else "Not Studied" if data[r][4] == "NS" else "Revised"
            print(f"{r+1}. {data[r][0]} | {data[r][1]} | {data[r][2]} | {data[r][3]} | {remarks}")
    except Error as e:
        print(f"Error retrieving upcoming tests: {e.msg}")

    c = input("\nPress 1 to UPDATE or ENTER to return to main menu...")
    if c != "1":
        menu()
    else:
        try:
            ss = int(input("Select the test (number) to update: "))
            to_update = data[ss-1]
        except (ValueError, IndexError):
            print("\nPlease enter a valid option.")
            input("Press ENTER to try again...")
            view_upcoming_tests()

        os.system('cls' if os.name == 'nt' else ' clear')
        print("Update Test\n")
        choice = input("Do you want to remove this test? (y/n): ")
        if choice == "y":
            try:
                cursor.execute("DELETE FROM tests WHERE ExamDate = %s AND Subject = %s AND Series = %s", (to_update[0], to_update[1], to_update[2]))
                cnx.commit()
                print("\nTest removed successfully!")
            except Error as e:
                print(f"\nError removing test: {e.msg}")
            input("\nPress ENTER to return...")
            view_upcoming_tests()
        
        print("Press ENTER to keep the current value.")
        remarks = "Studied" if to_update[4] == "S" else "Not Studied" if to_update[4] == "NS" else "Revised"
        print(f"Selected: {to_update[0]} | {to_update[1]} | {to_update[2]} | {to_update[3]} | {remarks}") 
        
        exam_date = input("Exam Date (YYYY-MM-DD): ")
        subject = input("Subject: ").capitalize().strip()
        series = input("Series: ").upper()
        portions = input("Portions (comma-seperated topics): ")
        status = input("Status (S/NS/R) [For Studied/Not Studied/Revised]: ").upper()

        query = ("UPDATE tests SET ExamDate = %s, Subject = %s, Series = %s,  Portions = %s, Status = %s WHERE ExamDate = %s AND Subject = %s AND Series = %s")
        data_query = (exam_date if exam_date != "" else to_update[0], subject if subject != "" else to_update[1],
                      series if series != "" else to_update[2], portions if portions != "" else to_update[3],
                      status if status != "" else to_update[4],
                      to_update[0], to_update[1], to_update[2])

        try:
            cursor.execute(query, data_query)
            cnx.commit()
            print("\nTest updated successfully!")
        except Error as e:
            print(f"\nError updating Test: {e.msg}")
        input("Press ENTER to return...")
        view_upcoming_tests()

# View Completed Tests With Marks
def view_all_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Marks Added Tests\n")
    try:
        cursor.execute("SELECT * FROM tests WHERE MarksObtained IS NOT NULL ORDER BY ExamDate")
        data = cursor.fetchall()
        for r in range(len(data)):
            print(f"{r+1}. {data[r][0]} | {data[r][1]} | {data[r][2]} | {data[r][3]} | {data[r][5]}/{data[r][6]} Marks")
    except Error as e:
        print(f"Error retrieving tests: {e.msg}")

    c = input("\nPress 1 to UPDATE or ENTER to return to main menu...")
    if c != "1":
        menu()
    else:
        try:
            ss = int(input("Select the test (number) to update: "))
            to_update = data[ss-1]
        except (ValueError, IndexError):
            print("\nPlease enter a valid option.")
            input("Press ENTER to try again...")
            view_all_tests()

        os.system('cls' if os.name == 'nt' else ' clear')
        print("Update Test\n")
        choice = input("Do you want to remove this test? (y/n): ")
        if choice == "y":
            try:
                cursor.execute("DELETE FROM tests WHERE ExamDate = %s AND Subject = %s AND Series = %s", (to_update[0], to_update[1], to_update[2]))
                cnx.commit()
                print("\nTest removed successfully!")
            except Error as e:
                print(f"\nError removing test: {e.msg}")
            input("\nPress ENTER to return...")
            view_all_tests()
        
        print("Press ENTER to keep the current value.")
        print(f"Selected: {to_update[0]} | {to_update[1]} | {to_update[2]} | {to_update[3]} | {to_update[5]}/{to_update[6]} Marks") 
        
        exam_date = input("Exam Date (YYYY-MM-DD): ")
        subject = input("Subject: ").capitalize().strip()
        series = input("Series: ").upper()
        portions = input("Portions (comma-seperated topics): ")
        try:
            o_marks = int(input("Obtained Marks: "))
            t_marks = int(input("Total Marks (i.e Out of): "))
        except ValueError:
            print("\nPlease enter valid numeric values for marks.")
            input("Press ENTER to try again...")
            view_all_tests()

        query = ("UPDATE tests SET ExamDate = %s, Subject = %s, Series = %s,  Portions = %s, MarksObtained = %s, TotalMarks = %s WHERE ExamDate = %s AND Subject = %s AND Series = %s")
        data_query = (exam_date if exam_date != "" else to_update[0], subject if subject != "" else to_update[1],
                      series if series != "" else to_update[2], portions if portions != "" else to_update[3],
                      o_marks if o_marks != "" else to_update[5], t_marks if t_marks != "" else to_update[6],
                      to_update[0], to_update[1], to_update[2])

        try:
            cursor.execute(query, data_query)
            cnx.commit()
            print("\nTest updated successfully!")
        except Error as e:
            print(f"\nError updating Test: {e.msg}")
        input("Press ENTER to return...")
        view_all_tests()

# Add Test Marks
def add_marks():
    x = True
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Test Marks\n")
        cursor.execute("SELECT * FROM tests WHERE MarksObtained IS NULL and ExamDate < CURDATE() ORDER BY ExamDate")
        data = cursor.fetchall()
        for r in range(len(data)):
            print(f"{r+1}. {data[r][0]} | {data[r][1]} | {data[r][2]}")
        se = input("\nSelect the test to add marks or press ENTER to return to the main menu... ")
        if se == "":
            menu()
        try:
            se = int(se)
            to_add = data[se-1]
        except (ValueError, IndexError):
            print("\nPlease enter a valid option.")
            input("Press ENTER to try again...")
            continue
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Test Marks\n")
        print(f"Selected: {to_add[0]} | {to_add[1]} | {to_add[2]}\n")
        try:
            o_marks = int(input("Obtained Marks: "))
            t_marks = int(input("Total Marks (i.e Out of): "))
        except ValueError:
            print("\nPlease enter valid numeric values for marks.")
            input("Press ENTER to try again...")
            continue

        query = ("UPDATE tests SET MarksObtained = %s, TotalMarks = %s, Status = 'C' WHERE ExamDate = %s AND Subject = %s AND Series = %s")
        data_query = (o_marks, t_marks, to_add[0], to_add[1], to_add[2])

        try:
            cursor.execute(query, data_query)
            cnx.commit()
            print("\nMarks added successfully!")
        except Error as e:
            print(f"\nError in adding marks: {e.msg}")

        x = False if input("\nPress 1 to add another test marks or Enter to return to the main menu... ") != "1" else True

# Add Assignments
def add_assignment():
    x = True
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Assignment\n")
        due_date = input("Due Date (YYYY-MM-DD): ")
        subject = input("Subject: ").capitalize().strip()
        topic = input("Topic: ")
        status = input("Status (S/NS) [For Submitted/Not Submitted]: ").upper()

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
        cursor.execute("SELECT * FROM assignments WHERE DueDate < %s and status = 'NS' ORDER BY DueDate", (today,))
        data = cursor.fetchall()
        for r in range(len(data)):
            print(f"{r+1}. {data[r][0]} | {data[r][1]} | {data[r][2]} | Not Submitted - **** OVERDUE ****")
        print("\n")
    except Error as e:
        print(f"Error retrieving overdue assignments: {e.msg}\n")

    oa = data
    loa = len(oa)
    
    try:
        cursor.execute("SELECT * FROM assignments WHERE DueDate > %s and DueDate < %s ORDER BY DueDate", (today, week))
        data = cursor.fetchall()
        for r in range(len(data)):
            remarks = "Submitted" if data[r][3] == "S" else "Not Submitted"
            print(f"{r + loa + 1}. {data[r][0]} | {data[r][1]} | {data[r][2]} | {remarks}")
    except Error as e:
        print(f"Error retrieving assignments: {e.msg}")
    
    data = oa + data

    c = input("\nPress 1 to UPDATE or ENTER to return to main menu...")
    if c != "1":
        menu()
    else:
        try:
            ss = int(input("Select the assignment (number) to update: "))
            to_update = data[ss-1]
        except (ValueError, IndexError):
            print("\nPlease enter a valid option.")
            input("Press ENTER to try again...")
            view_assignments()

        os.system('cls' if os.name == 'nt' else ' clear')
        print("Update Assignment\n")
        choice = input("Do you want to remove this assignment? (y/n): ")
        if choice == "y":
            try:
                cursor.execute("DELETE FROM assignments WHERE DueDate = %s AND Subject = %s AND Topic = %s", (to_update[0], to_update[1], to_update[2]))
                cnx.commit()
                print("\nAssignment removed successfully!")
            except Error as e:
                print(f"\nError removing assignment: {e.msg}")
            input("\nPress ENTER to return...")
            view_assignments()
        
        print("Press ENTER to keep the current value.")
        remarks = "Submitted" if to_update[3] == "S" else "Not Submitted"
        print(f"Selected: {to_update[0]} | {to_update[1]} | {to_update[2]} | {remarks}") 
        
        due_date = input("Due Date (YYYY-MM-DD): ")
        subject = input("Subject: ").capitalize().strip()
        topic = input("Topic: ")
        status = input("Status (S/NS) [For Submitted/Not Submitted]: ").upper()

        query = ("UPDATE assignments SET DueDate = %s, Subject = %s, Topic = %s, Status = %s WHERE DueDate = %s AND Subject = %s AND Topic = %s")
        data_query = (due_date if due_date != "" else to_update[0], subject if subject != "" else to_update[1],
                      topic if topic != "" else to_update[2], status if status != "" else to_update[3],
                      to_update[0], to_update[1], to_update[2])

        try:
            cursor.execute(query, data_query)
            cnx.commit()
            print("\nAssignment updated successfully!")
        except Error as e:
            print(f"\nError updating Assignment: {e.msg}")
        input("Press ENTER to return...")
        view_assignments()

# Add Syllabus
def add_syllabus():
    x = True
    print("This function is to be used once every semester (or year) to add the syllabus for all subjects")
    print("Add all subjects (syllabus just press ENTER if not known)")
    choice = input("Do you want to remove all existing syllabus data? (y/n) [y only in start of year]: ")
    if choice == "y":
        try:
            cursor.execute("DELETE FROM syllabus")
            cnx.commit()
            print("All existing syllabus data removed.")
        except Error as e:
            print(f"Error removing existing syllabus data: {e.msg}")
        input("Press ENTER to continue...")
    while x:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Add Syllabus\n")
        subject = input("Subject: ").capitalize().strip()
        chapters = input("Chapters (comma-seperated): ")

        add_syl = ("INSERT INTO syllabus "
                    "(Subject, Chapters) "
                    "VALUES (%s, %s)")
        data_syl = (subject, chapters)

        try:
            cursor.execute(add_syl, data_syl)
            cnx.commit()
            print("\nSyllabus added successfully!")
        except Error as e:
            print(f"\nError adding syllabus: {e.msg}")
        
        x = False if input("\nPress 1 to add new or Enter to return to the main menu... ") != "1" else True

    menu()

# View Syllabus
def view_syllabus():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Syllabus\n")
    try:
        cursor.execute("SELECT * FROM syllabus ORDER BY Subject")
        data = cursor.fetchall()
        for r in range(len(data)):
            print(f"{r+1}. {data[r][0]} | {data[r][1]}")
    except Error as e:
        print(f"Error retrieving syllabus: {e.msg}")

    c = input("\nPress 1 to UPDATE or ENTER to return to main menu...")
    if c != "1":
        menu()
    else:
        try:
            ss = int(input("Select the subject (number) to update: "))
            to_update = data[ss-1]
        except (ValueError, IndexError):
            print("\nPlease enter a valid option.")
            input("Press ENTER to try again...")
            view_syllabus()

        os.system('cls' if os.name == 'nt' else ' clear')
        print("Update Syllabus\n")
        print("Selected Subject:", to_update[0])
        print("Current Syllabus:", to_update[1])
        chapters = input("New Syllabus (comma-seperated | '' for emptying | /r for removing subject) [Tip: Copy the current and edit]: ")
        query = ("UPDATE syllabus SET Chapters = %s WHERE Subject = %s") if chapters != "/r" else ("DELETE FROM syllabus WHERE Subject = %s")
        data_query = (chapters, to_update[0]) if chapters != "/r" else (to_update[0])

        try:
            cursor.execute(query, data_query)
            cnx.commit()
            print("\nSyllabus updated successfully!")
        except Error as e:
            print(f"\nError updating Syllabus: {e.msg}")
        input("Press ENTER to return...")
        view_syllabus()

# Fetch Subjects
def fetch_sub():
    info = ()
    try:
        cursor.execute("SELECT DISTINCT Subject FROM syllabus")
        subs = [row[0] for row in cursor.fetchall()]
        if len(subs) == 0:
            info += ("N/A",)
        d_subs = subs + random.choices(subs, k=7-len(subs)) if len(subs) < 7 else subs
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        d = {days[i]:d_subs[i] for i in range(7)}
        info += (d[dt.datetime.now().strftime("%A")],)
    except Error as e:
        print(f"Error fetching subjects: {e.msg}")

    try:
        cursor.execute("SELECT DueDate, Subject, Topic FROM assignments WHERE DueDate > CURDATE() and Status = 'NS' ORDER BY DueDate")
        data = cursor.fetchone()
        if len(data) == 0:
            info += ("N/A",)
        else:
            info += (f"{data[1]} - {data[2]} (Due: {data[0]})",)
    except Error as e:
        print(f"Error fetching assignments: {e.msg}")

    return info
    

# Main Loop
menu()

cnx.commit()
cnx.close()