## Maria Bui
[CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission)

## Install and Run Directions
Run ```main.py``` to launch the program.

When running the automated tests in ```test_file.py```, run the tests in order from the top of the file to the bottom as some tests depend and build on previous tests. For example, the test that verifies an existing user's data is autofilled when they submit their email, ```test_existing_user_data_population```, and the test that verifies a claimer's data is displayed when their claimed entry is selected, ```test_claimer_data_population```, both depend and build on a previous test, ```test_user_creation```, in which a user and claim are saved to the test database. Additionally, the test database file, ```test_db.sqlite```, must be removed after tests are completed and before tests are executed again to reset the test database.

## What the Project Does
The program is a GUI that allows users to claim CUBES projects. It uses the Wufoo API to download the entries data from a Wufoo form by sending an HTTP GET request, converting the HTTP GET response into JSON, and extracting the entries data from JSON. The entries data are saved to a database. The entries data from the database are displayed in the GUI. Users can input their own information to claim their selected entries. An entry can only be claimed once, but a user can claim multiple entries.

## Database Layout
The database contains an entries table that stores the entries data. The entries table consists of 24 columns with 21 of them corresponding to the fields in the [CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission) form. The remaining 3 columns correspond to the entry ID, creation date, and creator. For columns that correspond to checkbox fields, an entry has a value of *Y* if the field was selected and *N* otherwise.

## GUI Layout
The GUI consists of 5 windows:
1. ```Update or Run```
   * Opens on program launch.
   * Prompts the user to choose to either update the data in the database or run the data visualization.
   * Closes after the user chooses an option. GUI remains running after updating the data in the database.
2. ```Entries List```
   * Located on the left of the screen.
   * Displays the entries in a list. If the user has chosen to update the data in the database, an updated list of entries is displayed.
   * Shows a preview of each entry by displaying its associated id, first name, last name, and organization name.
   * Claimed entries have a dark red text color.
   * Has a *Quit* button in the bottom right corner.
   * Selects Entry 1 by default.
3. ```Entry Data```
   * Located to the right of the ```Entries List``` window.
   * Displays the complete entry data of the selected entry from the list. 
   * Editing is disabled for the data fields.
   * Displays Entry 1's data by default.
4. ```Claim```
   * Located to the right of the ```Entry Data``` window.
   * Prompts the user to input their email, first name, last name, title, and department to claim the selected entry.
   * Shows when an unclaimed entry is selected.
   * Displays by default if Entry 1 has not been claimed.
5. ```User Data```
   * Located to the right of the ```Entry Data``` window.
   * Displays the selected entry's claimer's email, first name, last name, title, and department.
   * Shows when a claimed entry is selected.
   * Displays Entry 1's claimer by default if Entry 1 has been claimed.

## Detailed Manual Test Plan
[Click here for a detailed manual test plan (with pictures) to explain what should happen when the graphical elements are invoked.](https://docs.google.com/document/d/1zk0iSlQMeo-QUfFKDz57KuuU5-b7ajrnxbD603LRIis/edit?usp=sharing)

## What Is Missing from the Project
None.