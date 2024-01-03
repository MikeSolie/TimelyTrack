##################################################
# Mike Solie                                     #
# Project/Client Tracker                         #
#                                                #
# Description:                                   #
# Uses terminal menu to provide users with a UI  #
# to easily track billable time. Writes user     #
# input to a file and can be tracked in the      #
# terminal without needing to open the file.     #
##################################################

#####
# import os to use the operating system for the filepath
# import datetime to timestamp entries
# import time for track time worked
#####
import os
import datetime
import time
import msvcrt
#####
# function: check_files
# purpose: to check if files exist
# inputs: none
#####
def check_files():
    if not os.path.exists('projects.txt'):
        # create an empty projects file
        with open('projects.txt', 'w') as file:
            pass

    if not os.path.exists('time_log.txt'):
        # create a time log file with initial line
        with open('time_log.txt', 'w') as file:
            file.write("Total Time Worked:\n")

#####
# function: save_project
# purpose: saves projects to a file
# inputs: project name to be saved
#####
def save_project(name):
    with open('projects.txt', 'a') as file:
        file.write(name + '\n')

#####
# function: clear_screen
# purpose: to clear the screen when switching menus
#####

def clear_screen():
    os.system(('cls' if os.name == 'nt' else 'clear'))

#####
# function: delete_project
# purpose: deletes projects from file
# inputs: project name to be deleted
#####
def delete_project(name):
    with open('projects.txt', 'r') as file:
        lines = file.readlines()

    with open('projects.txt', 'w') as file:
        # write lines except one to be deleted
        for line in lines:
            if line.strip() != name:
                file.write(line)

#####
# function: list_projects
# purpose: to list projects in terminal
# inputs: none
#####
def list_projects():
    with open('projects.txt', 'r') as file:
        projects = file.readlines()
    # return list of project names w/o newline chars
    return [project.strip() for project in projects]

#####
# function: log_time
# purpose: logs user time inputs and applies timestamps
# inputs: project and hours
#####
def log_time(project, hours):
    # get timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # create entry with timestamp
    entry = f'{timestamp} - {project}: {hours} hours\n'
    
    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()

    total_time_flag = False
    if time_log and 'Total Time Worked' in time_log[-1]:
        total_time_flag = True

    with open('time_log.txt', 'a') as file:
        # write entry to file
        if not total_time_flag:
            file.write(entry)
        else:
            file.write(f'{entry}\n')

#####
# function: new_client
# purpose: saves new client/project info 
# inputs: client name
#####
def new_client():
    clear_screen()
    name = input("Enter client name: ")
    save_project(name)
    clear_screen()

#####
# function: existing_client
# purpose: provides menu to select and add time to existing clients
# inputs: menu options and time
#####
def existing_client():
    while True:
        # Clear the screen
        clear_screen()

        projects = list_projects()
        print("\nExisting Clients:")
        for i, project in enumerate(projects, start=1):
            print(f"{i}. {project}")

        print("0. Back to Main Menu")

        choice = input("Select a client or enter '0' to go back: ")

        if choice == '0':
            # Clear the screen before breaking out of the loop
            clear_screen()
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(projects):
                selected_project = projects[choice - 1]

                # Ask the user if they want to start a timer or enter time manually
                timer_choice = input(f"Do you want to start a timer for '{selected_project}'? (y/n): ").lower()

                if timer_choice == 'y':
                    # Start the timer
                    start_time = time.time()
                    print("Timer started. Press Enter to stop the timer.")

                    while True:
                        # Calculate elapsed time and round to 2 decimal places
                        elapsed_time = round((time.time() - start_time) / 3600, 2)

                        # Output elapsed time in real-time
                        print(f"\rElapsed Time: {elapsed_time} hours", end="", flush=True)

                        # Check if Enter key is pressed
                        if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                            break

                        # Wait for a short interval before checking elapsed time again
                        time.sleep(0.1)

                    # Stop the timer
                    end_time = time.time()
                    elapsed_time = round((end_time - start_time) / 3600, 2)  # Convert seconds to hours and round to 2 decimal places

                    # Log the elapsed time
                    log_time(selected_project, elapsed_time)

                    # Clear the screen after logging time
                    clear_screen()
                elif timer_choice == 'n':
                    # User wants to enter time manually
                    hours = float(input("Enter hours worked: "))
                    log_time(selected_project, round(hours, 2))  # Round the entered hours to 2 decimal places
                else:
                    print("Invalid choice. Please enter 'y' or 'n'.")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#####
# function: delete_client
# purpose: provides option to delete clients
# inputs: menu options to select clients to delete
#####
def delete_client():
    # see existing clients function for code comments
    while True:
        clear_screen()
        projects = list_projects()
        print("\nExisting Clients:")
        for i, project in enumerate(projects, start=1):
            print(f"{i}. {project}")

        print("0. Back to Main Menu")

        choice = input("Select a client to delete or enter '0' to go back: ")

        if choice == '0':
            clear_screen()
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(projects):
                selected_project = projects[choice - 1]
                delete_project(selected_project)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#####
# function: display_time_log
# purpose: to output time log to terminal
# inputs: none
#####
def display_time_log():
    # clear the screen
    clear_screen()

    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()

    if time_log:
        print("\nTime Log:")
        total_time_flag = False
        total_time_worked = {}

        # loop through entries in time log
        for entry in time_log:
            # split each entry into timestamp and data parts
            parts = entry.strip().split(' - ', 1)
            if len(parts) == 2:
                timestamp, entry_data = parts
                if not total_time_flag:
                    # output timestamp and data entry
                    print(f"{timestamp} - {entry_data}")

                    # process "Time Log" entries for calculating totals
                    project, hours = entry_data.split(': ')
                    hours = float(hours.split()[0])
                    if project in total_time_worked:
                        total_time_worked[project] += hours
                    else:
                        total_time_worked[project] = hours

        if total_time_worked:
            print("\nTotal Time Worked:")
            with open('time_log.txt', 'a') as file:
                file.write('\nTotal Time Worked:\n')
                # display and write to the file the total time worked for each project
                for project, hours in total_time_worked.items():
                    print(f"{project}: {hours} hours")
                    file.write(f"{project}: {hours} hours\n")
    else:
        print("\nNo time log entries yet.")

    # wait for user to press any key
    input("\nPress Enter to return to the Main Menu...")
    # clear the screen before returning to the main menu
    clear_screen()


#####
# function: total_time_worked
# purpose: to provide a total of all entries for each client
# inputs: time entries
#####
def total_time_worked_in_file():
    project_times = {}

    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()

    for entry in time_log:
        project, hours = entry.strip().split(': ')
        hours = float(hours.split()[0])

        if project in project_times:
            project_times[project] += hours
        else:
            project_times[project] = hours

    with open('time_log.txt', 'a') as file:
        file.write('\nTotal Time Worked:\n')
        for project, hours in project_times.items():
            file.write(f"{project}: {hours} hours\n")

#####
# function: menu
# purpose: gives users a functional menu in the terminal
# inputs: numbers
#####
def menu():
    while True:
        print("\nMenu:")
        print("1. New Client")
        print("2. Existing Client")
        print("3. Delete Client")
        print("4. View Time Log")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            new_client()
        elif choice == '2':
            existing_client()
        elif choice == '3':
            delete_client()
        elif choice == '4':
            display_time_log()
        elif choice == '5':
            clear_screen()
            break
        else:
            print("Invalid choice. Please try again.")

#####
# function: calls functions
# purpose: runs program 
#####
def main():
    clear_screen()
    check_files()
    menu()

if __name__ == "__main__":
    main()
