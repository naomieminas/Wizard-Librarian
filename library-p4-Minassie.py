"""
    Project: Wizard Librarian
    Name: Naomie Minassie
    Date: 11/15/2024
    Course: CMSC 150: Intro to Computing -- Section 04
    Program Description: Welcome to the Wizard Library! This program sorts and searches a selection of very special books
    based on user input. Curious to find spell books or novels written by Ravenna Ravenscroft? You're in the right place!
    Simply interact with our user-friendly interface and we'll do the heavy-lifting. Happy reading!
"""

#    WRITE YOUR CODE HERE     #
# GOOD LUCK! YOU'VE GOT THIS! #

############          IMPORT AND EXPORT FUNCTIONS         ############

def import_file(filename):
    """Imports book data from a specified file."""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        if filename != "wizard_books.txt":
            ### Fallback to wizard_books.txt ###
            print(f"{filename} not found. Trying wizard_books.txt.")
            return import_file("wizard_books.txt")
        else:
            ### Final fallback if wizard_books.txt is also missing ###
            print("wizard_books.txt not found. Returning an empty list.")
            return []

def export_file(sorted_books, output_file):
    """Exports the sorted books into a specified file."""
    try:
        with open(output_file, 'w') as file:
            for book in sorted_books:
                file.write(f"{book}\n")   # Writes each book on a new line
    except Exception as e:
        ### Catches and reports any unexpected errors ###
        print(f"An error occurred while exporting books: {e}")


###############             SORT FUNCTION          ###################

def sort_books(filename, by="title"):
  """Sorts books by title or author's last name and exports them into a file."""
  books = import_file(filename)  # Load books from the specified file
  if by == "title":        # Sort books alphabetically by title
    sorted_books = sorted(books)
    export_file(sorted_books, "wizard_books_TITLE.txt")
    print("\n*** Books were sorted by title and exported to wizard_books_TITLE.txt ***")
  elif by == "author":    # Sort books alphabetically by the author's last name
    def last_name(book):
        return book.split("- ")[-1].split(" ")[-1]    # Extract author's last name
    sorted_books = sorted(books, key=lambda x: last_name(x))
    export_file(sorted_books, "wizard_books_AUTHOR.txt")
    print("\n*** Books were sorted by author and exported to wizard_books_AUTHOR.txt ***")

##########          SEARCH FUNCTION       #############

def search_books(books, keyword, by="either"):
  """Searches books by title, author, or either."""
  results = set()
  for book in books:
    title, author = book.split(" - ")   # Split book entry into title and author
    # Match based on the selected search mode
    if (by == "either" and (keyword.lower() in title.lower() or keyword.lower() in author.lower())) or \
       (by == "title" and keyword.lower() in title.lower()) or \
       (by == "author" and keyword.lower() in author.lower()):
       results.add(book)
  if results:
    # Determine which file was used for the search
    file_used = "wizard_books.txt" if by == "either" else f"wizard_books_{by.upper()}.txt"
    print(f"\nUsing {file_used} for search.")

    # Display the sorted results
    print("\n--- Search Results ---")
    for book in sorted(results):
      print(book)

    #Display the total number of matches
    print("\n------------------------------------")
    print(f"Total matches: {len(results)}")
  else:
    print("\nSorry! No matches found.")

############         SUBMENU HANDLERS           ###########
def submenu_loop(prompt:str, valid_options:list, action_callback):
  """
  Loop for submenu interactions
  - prompt: The question to ask the user.
  - valid_options: A list of valid inputs.
  - action_callback: A function to execute the selected action.
  """
  while True:
    choice = input(prompt).lower()
    if choice in valid_options:
      if choice == "back":              ### exits the submenu  ###
        return
      action_callback(choice)   # Perform the action for valid input
    else:
      print("\nInvalid input. Please choose from the options given.")


def search_submenu():
    """
    Handles the search submenu logic.
    Allows users to search books by title, author, or both.
    """

    def perform_search(search_method):
        # Determine the file to use based on the search method
        if search_method == "title":
            filename = "wizard_books_TITLE.txt"
        elif search_method == "author":
            filename = "wizard_books_AUTHOR.txt"
        elif search_method == "either":
            filename = "wizard_books.txt"
        else:  ### Invalid Input Conditional  ###
            return

        # Ensures the required, sorted file exists
        try:
            with open(filename, 'r') as file:
                pass
        except FileNotFoundError:
            if search_method == "title":
                sort_books("wizard_books.txt", by="title")
            elif search_method == "author":
                sort_books("wizard_books.txt", by="author")

        # Prompts for a keyword and performs the search
        while True:
            keyword = input(f"\nWhat keyword(s) would you like to search for? [enter keyword or 'back']\n")
            if keyword == "back":  ### return to the previous menu ###
                break
            books = import_file(filename)
            search_books(books, keyword, by=search_method)

    submenu_loop(
        prompt="\nHow would you like to search? [title, author, either, back]: \n",
        valid_options=["title", "author", "either", "back"],
        action_callback=perform_search
    )

def sort_submenu():
  """
  Handles the sort submenu logic.
  Allows users to sort books by title or author.
  """
  def perform_sort(sort_method):
    if sort_method == "title":
      sort_books("wizard_books.txt", by="title")
    elif sort_method == "author":
      sort_books("wizard_books.txt", by="author")
  submenu_loop(
      prompt = "\nHow would you like to sort the books? [title, author, back]: \n",
      valid_options=["title", "author", "back"],
      action_callback=perform_sort
  )

############            USER MENU               ###########
while True:
  choice = input("\nWelcome to the Wizard Library! What would you like to do? [sort, search, exit]: \n").lower()
  if choice == "exit":
    print("\nThanks for visiting the Wizard Library! Hope to see you soon :)")
    break
  elif choice == "sort":
    sort_submenu()
  elif choice == "search":
    search_submenu()
  else:
    print("Invalid input. Please choose 'sort', 'search', or 'exit'.")