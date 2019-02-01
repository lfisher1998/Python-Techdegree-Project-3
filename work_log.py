import csv
import os
import datetime
import re

# display intro message
intro_message = 'Hello there!'


def menu():
    # print a message that greets user and gives options
    print("Here are your options: \n 1. Add an entry \n 2. Look up previous entry \n")
    # ask user for input on which option they would like
    choice = input("What would you like to do? Please enter a number with its corresponding option:")
    # if they choose 1, move to the add_entry function
    if choice == '1':
        add_entry()
    # if they choose 2, move to the search_entries function
    if choice == '2':
        search_entries()
    # if they type anything other than 1 or 2, display error message, restart the function and prompt user
    else:
        print("Oh no! That is an invalid number. Please try again.")
        menu()


def add_entry():
    # initialize all parameters of add_entry for user to input and change them
    task_name = None
    task_time = None
    task_notes = None
    task_date = None
    while not task_name:
        # input the task name
        task_name = input("Please enter a task name: ")

    while not task_time:
        # ask user for the task time, if they enter something other than a number, make them enter again and show error
        try:
            task_time = int(input("Please enter the time spent on the task with a number value(in minutes): "))
        except ValueError:
            print("Oh no! That is an invalid number. Please try again.")
    # ask user to enter notes, if there is no notes, tell user to hit Enter
    task_notes = input("Enter task notes here(if there is none, please press Enter.) ")
    # set the date to the current date when the entry is entered
    task_date = datetime.datetime.now().strftime('%m/%d/%Y')
    # create an entries csv file to be filled with new entries
    with open("entries.csv", "a+", newline='') as entry_file:
        fields = ['Task Name', 'Task Time', 'Task Notes', 'Task Date']
        entry_writer = csv.DictWriter(entry_file, fieldnames=fields)
        # if the file has just been created, first write the field headers
        if os.stat("entries.csv").st_size == 0:
            entry_writer.writeheader()

        # place new entry as a dictionary in its own row
        entry_writer.writerow(
            {'Task Name': task_name, 'Task Time': task_time, 'Task Notes': task_notes, 'Task Date': task_date}
        )
    add_again = input("The task information was added! Would you like to add another? [y]es, [n]o: ")
    if add_again.lower() == 'y':
        add_entry()
    else:
        menu()


def search_entries():
    # when the user wants to search for an entry, these are the options displayed
    print("These are your options for searching:\n"
          "1. Search by Date\n"
          "2. Search by the Time Spent on task\n"
          "3. Search by Exact Search\n"
          "4. Search by Pattern\n"
          "5. Return to Main Menu\n"
          )
    # ask for user input
    search_choice = input("Please type your decision with its corresponding number (Ex. 1, 2, 3): ")
    # Search by date option
    if search_choice == '1':
        search_by_date()
    # Search by time option
    if search_choice == '2':
        search_by_time()
    # Search by exact match option
    if search_choice == '3':
        search_by_exact()
    # Search by exact pattern or expression
    if search_choice == '4':
        search_by_pattern()
    # Go back to main menu option
    if search_choice == '5':
        menu()
    # if they type anything other than the provided options, an error message appears to try again
    else:
        print("Oh no! That is an invalid number. Please try again.\n")
        search_entries()


def input_date(user_input):
    # ask for the user to input a date in the proper format
    print("In order to search the date, please enter your date in the format MM/DD/YYYY")
    # while the user has not entered a date, prompt them and check for errors
    while len(user_input) == 0:
        try:
            date_string = input("Please enter your date for searching: ")
            user_input.append(datetime.datetime.strptime(date_string, '%m/%d/%Y'))
        except ValueError:
            print("Please enter a date in the correct format MM/DD/YYYY")


def search_by_date():
    #  I should be presented with a list of dates with entries and be able to choose one to see entries from
    # contain the dates in a list
    date1 = []
    input_date(date1)
    # store result of search in a list
    result = []
    # open the file to check if there is a match
    with open('entries.csv') as entry_file:
        reader = csv.DictReader(entry_file)
        for row in reader:
            # if there is a match, add it to the result list
            if datetime.datetime.strptime(row['Task Date'], '%m/%d/%Y') == date1[0]:
                result.append(row)
    # if there are no matches in the result list, report no results
    if len(result) == 0:
        print("No results! \n")
        # return back to search options
        search_entries()
    else:
        # otherwise, display the matches in the result list
        display_entries(result)


def search_by_time():
    # initialize the time to make it empty
    task_time = None
    # results in a list
    time_result = []
    print("Time to search!\n")
    while task_time is None:
        # ask the user to input a time in minutes
        task_time = input("Enter a integer value to search (Ex. 1, 25, 45): ")
        try:
            # convert string to an integer
            task_time = int(task_time)
        except ValueError:
            # if they do not enter a correct integer value, display error message
            print("Please enter an integer value.")
            # reinitialize the time to none
            task_time = None
        else:
            task_time = str(task_time)
    # check file for matches
    with open('entries.csv') as entry_file:
        reader = csv.DictReader(entry_file)
        for row in reader:
            if row['Task Time'] == task_time:
                time_result.append(row)
    # if there are no matches, report no results
    if len(time_result) == 0:
        print("No results! \n")
        search_entries()
    else:
        # otherwise, display matches
        display_entries(time_result)


def search_by_exact():
    # initialize
    exact_search = None
    # store results in list
    exact_result = []
    print("Time to search!\n")
    while exact_search is None:
        # ask user for keywords to search
        exact_search = input("Please enter any keywords to search:")
        # if they do not type a keyword, give them an error message
        if exact_search.strip() == '':
            print("You must type something to search.")
            # reinitialize
            exact_search = None
    # check file for matches
    with open('entries.csv') as entry_file:
        reader = csv.DictReader(entry_file)
        for row in reader:
            if (row['Task Name'].find(exact_search) > -1 or
                    row['Task Notes'].find(exact_search) > -1):
                exact_result.append(row)
    # if there is no matches, display no results message
    if len(exact_result) == 0:
        print('No results!\n')
        search_entries()
    # otherwise, display matches
    else:
        display_entries(exact_result)


def search_by_pattern():
    # initialize
    pattern_search = None
    # store matches in a list
    pattern_result = []
    print("Time to search!")
    while pattern_search is None:
        # ask user to input an expression
        pattern_search = input('Please enter an expression to search: ')
        try:
            pattern_search = re.compile(pattern_search)
        except re.error:
            # error message for incorrect input
            print("Please enter an expression.")
            # reinitialize
            pattern_search = None
    # check file for matches
    with open('entries.csv') as entry_file:
        reader = csv.DictReader(entry_file)
        for row in reader:
            # if there is a match in any of the rows, append to the result list
            if (re.search(pattern_search, row['Task Name']) or
                    re.search(pattern_search, row['Task Time']) or
                    re.search(pattern_search, row['Task Notes']) or
                    re.search(pattern_search, row['Task Date'])):
                pattern_result.append(row)
    # if there are no matches, say no results
    if len(pattern_result) == 0:
        print('No results!\n')
        search_entries()
    # otherwise, display the matched results
    else:
        display_entries(pattern_result)


def display_entries(result):
    # initialize a count for how many matches there are
    count = 0
    print("Here are your results!\n")
    # for loop to give each match it's own set of information
    for match in result:
        print("Task Name: {}\n"
              "Task Time: {}\n"
              "Task Notes: {}\n"
              "Task Date: {}\n\n".format(match['Task Name'], match['Task Time'], match['Task Notes'], match['Task Date'])
              )
        # increment the count
        count += 1
    # display the total number of matches using the count variable
    print("Total amount of matches: {}\n".format(count))
    # return back to the search option menu
    search_entries()


if __name__ == "__main__":
    # print intro message
    print(intro_message)
    # start the script from the top
    menu()
