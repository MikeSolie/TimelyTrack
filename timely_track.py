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
            file.write('Total Time Worked:\n')

#####
# function: save_project
# purpose: saves projects to a file
# inputs: project name to be saved
#####
def save_project(name):
    with open('projects.txt', 'a') as file:
        file.write(name + '\n')

#####
# purpose: to clear the screen when switching menus
#####
def clear_screen():
    os.system(('cls' if os.name == 'nt' else 'clear'))

#####
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
# purpose: to list projects in terminal
# inputs: none
#####
def list_projects():
    with open('projects.txt', 'r') as file:
        projects = file.readlines()
    # return list of project names w/o newline chars
    return [project.strip() for project in projects]

#####
# purpose: logs user time inputs and applies timestamps
# inputs: project and hours
#####
def log_time(project, hours, date=None):
    if date is None:
        # Get current date if date parameter is not provided
        date = datetime.date.today().strftime('%Y-%m-%d')
    # Get timestamp
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Create entry with timestamp and project name
    entry = f'{date} - {project}: {hours} hours'

    # Ask the user if they want to add a comment
    comment_choice = input('\nDo you want to add a comment? (y/n)\n~>').lower()

    if comment_choice == 'y':
        comment = input('Enter your comment\n~>')
        entry += f' - {comment}'

    entry += '\n'

    # Write the entry to the time log file
    with open('time_log.txt', 'a') as file:
        file.write(entry)

#####
# purpose: saves New Project/project info 
# inputs: project name
#####
def new_project():
    clear_screen()
    print('-' * len(f'  New Project  ') + f'\n  New Project')
    print('-' * len(f'  New Project  '))
    name = input(' Enter project name\n~>')
    save_project(name)
    clear_screen()

#####
# purpose: provides menu to select and add time to existing projects
# inputs: menu options, comments and time
#####
def existing_project():
    while True:
        # Clear the screen
        clear_screen()

        projects = list_projects()
        print('-' * len(f'  Projects Menu  ') + f'\n  Projects Menu')
        print('-' * len(f'  Projects Menu  '))
        for i, project in enumerate(projects, start=1):
            print(f'{i}. {project}')

        print('H. Historic Time Entry')
        print('0. Back to Main Menu')
        print('-' * len(f'  Projects Menu  '))
        
        choice = input("Select a project, 'H' for historic time entry, or '0' to go back\n~>")

        if choice == '0':
            # Clear the screen before breaking out of the loop
            clear_screen()
            break
        elif choice.upper() == 'H':
            manual_time_entry()
        else:
            try:
                choice = int(choice)
                if 1 <= choice <= len(projects):
                    selected_project = projects[choice - 1]

                    # Ask the user if they want to start a timer or enter time manually
                    timer_choice = input(f"Do you want to start a timer for '{selected_project}'? (y/n)\n~>").lower()

                    if timer_choice == 'y':
                        # Start the timer
                        start_time = time.time()
                        print('-' * len('  Timer started. Press Enter to stop the timer  '))
                        print('Timer started. Press Enter to stop the timer.')

                        while True:
                            # Calculate elapsed time and round to 2 decimal places
                            elapsed_time = round((time.time() - start_time) / 3600, 2)

                            # Output elapsed time in real-time
                            print(f'\rElapsed Time: {elapsed_time} hours', end='', flush=True)

                            # Check if Enter key is pressed
                            if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                                print('\n' + '-' * len('  Timer started. Press Enter to stop the timer  '))
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
                        hours = float(input('Enter hours worked\n~>'))
                        log_time(selected_project, round(hours, 2))  # Round the entered hours to 2 decimal places
                    else:
                        print("Invalid choice. Please enter 'y' or 'n'\n~>")
                else:
                    print('Invalid choice. Please try again.')
            except ValueError:
                print('Invalid input. Please enter a number.')

#####
# purpose: provides option to manually enter time from previous 3 days
# inputs: time and comments
#####
def manual_time_entry():
    while True:
        # Clear the screen
        clear_screen()

        print('-' * len(f'  Manual Time Entry  ') + f'\n  Manual Time Entry')
        print('-' * len(f'  Manual Time Entry  '))
        print('Choose a date for manual time entry')
        print('1. Today')
        print('2. Yesterday')
        print('3. Two days ago')
        print('4. Three days ago')
        print('0. Back to Projects Menu\n')

        choice = input('Select an option\n~>')

        if choice == '0':
            # Clear the screen before breaking out of the loop
            clear_screen()
            break
        elif choice in ['1', '2', '3', '4']:
            try:
                selected_date = datetime.date.today() if choice == '1' else \
                                datetime.date.today() - datetime.timedelta(days=int(choice))
                selected_date_str = selected_date.strftime('%Y-%m-%d')

                # Clear the screen
                clear_screen()

                projects = list_projects()
                print('-' * len(f'  Projects  ') + f'\n  Projects')
                print('-' * len(f'  Projects  '))
                for i, project in enumerate(projects, start=1):
                    print(f'{i}. {project}')

                print('\n0. Back to Previous Menu')

                project_choice = input("Select a Project to manually enter time, or '0' to go back\n~>")

                if project_choice == '0':
                    # Clear the screen before going back to the previous menu
                    clear_screen()
                    continue
                else:
                    try:
                        project_choice = int(project_choice)
                        if 1 <= project_choice <= len(projects):
                            selected_project = projects[project_choice - 1]

                            # Prompt the user to enter hours worked
                            hours = float(input(f" Enter hours worked for '{selected_project}' on {selected_date_str}\n~>"))
                            log_time(selected_project, round(hours, 2), selected_date_str)  # Round the entered hours to 2 decimal places

                            # Clear the screen after logging time
                            clear_screen()
                        else:
                            print('Invalid choice. Please try again.')
                    except ValueError:
                        print('Invalid input. Please enter a number.')

            except ValueError:
                print('Invalid choice. Please enter a valid option.')
        else:
            print('Invalid choice. Please select a valid option.')

#####
# purpose: provides option to delete projects
# inputs: menu options to select projects to delete
#####
def delete_projects_menu():
    while True:
        clear_screen()
        projects = list_projects()
        print('-' * len(f'  Delete Projects Menu  ') + f'\n  Delete Projects Menu')
        print('-' * len(f'  Delete Projects Menu  '))
        for i, project in enumerate(projects, start=1):
            print(f'{i}. {project}')

        print('0. Back to Main Menu')
        print('-' * len(f'  Delete Projects Menu  '))

        choice = input('Select a project to delete or enter "0" to go back\n~>')

        if choice == '0':
            clear_screen()
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(projects):
                selected_project = projects[choice - 1]  # Get the selected project name
                delete_project(selected_project)  # Pass the selected project name
                print(f'{selected_project} deleted successfully!')
                input('Press Enter to continue...')
            else:
                print('Invalid choice. Please try again.')
        except ValueError:
            print('Invalid input. Please enter a number.')

#####
# purpose: to output time log to terminal
# inputs: none
#####
def display_time_log():
    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()
    clear_screen()
    
    if time_log:
        total_time_worked = {}
        #grand_totals = {}

        current_date = None
        daily_totals = {}

        for entry in time_log:
            parts = entry.strip().split(' - ', 1)
            if len(parts) == 2:
                timestamp, entry_data = parts
                date = timestamp.split()[0]

                if date != current_date:
                    # Display timestamped entries under 'Time Log' section
                    print('-' * len(f'{date} Time Log') + f'\n{date} Time Log')
                    print('-' * len(f'{date} Time Log'))
                    current_date = date
                    
                    # Reset daily_totals for the new date
                    daily_totals = {}

                # Process 'Time Log' entries for calculating totals
                project, hours = entry_data.split(': ')
                hours = float(hours.split()[0])

                if project in total_time_worked:
                    total_time_worked[project] += hours
                else:
                    total_time_worked[project] = hours

                if project in daily_totals:
                    daily_totals[project] += hours
                else:
                    daily_totals[project] = hours

                # Display timestamped entry
                print(f'{timestamp} - {entry_data}')

    # wait for the user to press any key
    input('\n Press Enter to return to the Previous Menu...')
    # clear the screen before returning to the main menu
    clear_screen()

#####
# purpose: to provide a total of all entries for each project
# inputs: time entries
#####
def display_total_time_worked():
    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()

    clear_screen()

    if not time_log:
        print('\nNo time log entries yet.')
        return

    total_time_worked = {}

    # loop through entries in time log
    for entry in time_log:
        # split each entry into timestamp and data parts
        parts = entry.strip().split(' - ', 1)
        if len(parts) == 2:
            entry_data = parts[1]

            # Process 'Time Log' entries for calculating totals
            project, hours = entry_data.split(': ')
            hours = float(hours.split()[0])

            if project in total_time_worked:
                total_time_worked[project] += hours
            else:
                total_time_worked[project] = hours

    # Display grand totals
    print('-' * len('Total Time Worked') + '\nTotal Time Worked')
    print('-' * len('Total Time Worked'))
    for project, hours in total_time_worked.items():
        print(f'{project}: {hours} hours')
    
    # wait for the user to press any key
    input('\n Press Enter to return to the Previous Menu...')
    # clear the screen before returning to the main menu
    clear_screen()

#####
# purpose: display daily totals and comments
# inputs: none
#####      
def display_today_totals():
    today = datetime.date.today().strftime("%Y-%m-%d")

    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()

    clear_screen()

    if not time_log:
        print("\nNo time log entries yet for Today.")
        return

    total_time_worked = {}
    daily_totals = {}
    
    print("-" * len(f"{today} Today's Totals") + f"\n{today} Today's Totals")
    print("-" * len(f"{today} Today's Totals"))
    
    # Loop through entries in time log
    for entry in time_log:
        parts = entry.strip().split(' - ', 1)
        if len(parts) == 2:
            timestamp, entry_data = parts

            # Extract date from timestamp
            date = timestamp.split()[0]

            if date != today:
                continue

            # Process "Time Log" entries for calculating totals
            project_hours, *comment = entry_data.split(' - ')
            project, hours = project_hours.split(': ')
            hours = float(hours.split()[0])

            # Extract comment if present
            comment_text = " ".join(comment).strip() if comment else None

            if project in total_time_worked:
                total_time_worked[project] += hours
            else:
                total_time_worked[project] = hours

            if project in daily_totals:
                daily_totals[project] += hours
            else:
                daily_totals[project] = hours

            # Display project name and hours worked
            print(f"{project}: {hours} hours")
            
            # Display comment if present
            if comment_text:
                print(f"{' ' * len(project)}  ∟ {comment_text}")

    print("\nTotal Hours Worked:", sum(daily_totals.values()), "hours")

    # Wait for the user to press any key
    input('\nPress Enter to return to the Previous Menu...')
    # Clear the screen before returning to the main menu
    clear_screen()


#####
# purpose: display all entries by date
# inputs: none
##### 
def display_historic_totals():
    with open('time_log.txt', 'r') as file:
        time_log = file.readlines()

    clear_screen()

    if not time_log:
        print('\nNo time log entries yet')
        return

    total_time_worked = {}
    daily_totals = {}
    grand_totals = {}

    # Get unique dates from the time log
    unique_dates = set()
    for entry in time_log:
        parts = entry.strip().split(' - ', 1)
        if len(parts) == 2:
            timestamp = parts[0]
            date = timestamp.split()[0]
            unique_dates.add(date)

    # Sort unique dates in descending order
    sorted_dates = sorted(unique_dates, reverse=True)

    # Display historic totals for the last 14 days
    for date in sorted_dates[:14]:
        # loop through entries in time log
        for entry in time_log:
            parts = entry.strip().split(' - ', 1)
            if len(parts) == 2:
                timestamp, entry_data = parts

                # Extract date from timestamp
                entry_date = timestamp.split()[0]

                if entry_date != date:
                    continue

                # Process 'Time Log' entries for calculating totals
                project, hours = entry_data.split(': ')
                hours = float(hours.split()[0])

                if project in total_time_worked:
                    total_time_worked[project] += hours
                else:
                    total_time_worked[project] = hours

                if project in daily_totals:
                    daily_totals[project] += hours
                else:
                    daily_totals[project] = hours

        print('-' * len(f'{date} Historic Totals') + f'\n{date} Historic Totals')
        print('-' * len(f'{date} Historic Totals'))

        # Display daily totals for the date
        for project, hours in daily_totals.items():
            print(f'{project}: {hours} hours')
            grand_totals[project] = grand_totals.get(project, 0) + hours

        # Display total hours worked for the date
        total_hours = sum(daily_totals.values())
        print(f' Total Hours Worked: {total_hours} hours\n')

        # Reset daily totals for the next date
        daily_totals = {}

    # wait for the user to press any key
    input('\n Press Enter to return to the Previous Menu...')
    # clear the screen before returning to the main menu
    clear_screen()

#####
# purpose: display time menu options
# inputs: menu options
##### 
def time_menu():
    clear_screen()
    while True:
        # Menu for user to choose output format
        print('-' * len(f' Time Log Menu  ') + f'\n Time Log Menu ')
        print('-' * len(f' Time Log Menu  '))
        print("1. Today's Totals")
        print('2. Total Time Worked')
        print('3. Historic Totals')
        print('4. Time Log')
        print('0. Back to Main Menu')
        
        choice = input('\nEnter your choice\n~>')

        if choice == '1':
            display_today_totals()
        elif choice == '2':
            display_total_time_worked()
        elif choice == '3':
            display_historic_totals()
        elif choice == '4':
            display_time_log()
        elif choice == '0':
            clear_screen()
            break
        else:
            print('Invalid choice. Please try again.')
#####
# purpose: gives users a functional menu in the terminal
# inputs: numbers
#####
def main_menu():
    while True:
        print('-' * len(f' TimelyTrack Main Menu  ') + f'\n TimelyTrack Main Menu ')
        print('-' * len(f' TimelyTrack Main Menu  '))
        print('1. New Project')
        print('2. Projects')
        print('3. Delete Project')
        print('4. Time Logs')
        print('5. Exit')

        choice = input('\nEnter your choice\n~>')

        if choice == '1':
            new_project()
        elif choice == '2':
            existing_project()
        elif choice == '3':
            delete_projects_menu()
        elif choice == '4':
            time_menu()
        elif choice == '5':
            clear_screen()
            break
        else:
            print('Invalid choice. Please try again.')

#####
# function: calls functions
# purpose: runs program 
#####
def main():
    clear_screen()
    check_files()
    main_menu()


if __name__ == '__main__':
    main()
