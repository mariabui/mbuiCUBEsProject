## Maria Bui
[CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission)

## Install and Run Directions
Run ```main.py``` to launch the program.

When running the automated tests in ```test_file.py```, run the tests in order from the top of the file to the bottom as some tests depend and build on previous tests. For example, ```test_existing_user_data_population``` and ```test_claimer_data_population``` depend and build on ```test_user_creation``` saving a new user and their claim to the database. Similarly, the test database file, ```test_db.sqlite```, should be removed after tests are completed and before tests are executed again to reset the database.

## What the Project Does
The program uses the Wufoo API to download the entries data from a Wufoo form by sending an HTTP GET request, converting the HTTP GET response into JSON, and extracting the entries data from JSON. The entries data are saved to a text file and a database. The entries from the database are displayed in a GUI.

## Database Layout
The database contains an entries table that stores the entries data. The entries table consists of 24 columns with 21 of them corresponding to the fields in the [CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission) form. The remaining 3 columns correspond to the entry ID, creation date, and creator. For columns that correspond to checkbox fields, an entry has a value of *Y* if the field was selected and *N* otherwise.

## GUI Layout
The GUI consists of 5 windows:
1. ```Update or Run```
   * Opens on program startup.
   * Prompts the user to choose to either update the data in the database or run the data visualization.
   * GUI remains running after updating the data in the database.
2. ```Entries List```
   * Located on the left of the screen.
   * Displays the entries in a list. If the user has chosen to update the data in the database, an updated list of entries is displayed.
   * Shows a preview of each entry by displaying its associated id, first name, last name, and organization name.
   * Claimed entries have red text color.
   * Has a *Quit* button in the bottom right corner.
3. ```Entry Data```
   * Located in the center of the screen.
   * Displays the complete entry data of the selected entry from the list. The first entry in the list is selected and displayed by default.
   * Editing is disabled for the data fields.
4. ```Claim```
   * Located on the right of the screen.
   * Prompts the user to provide their email, first name, last name, title, and department to claim the selected entry.
   * Shows when an unclaimed entry is selected.
5. ```User Data```
   * Located on the right of the screen.
   * Displays the selected entry's claimer's email, first name, last name, title, and department that they have provided.
   * Shows when a claimed entry is selected.

## Detailed Manual Test Plan
[Click here for a detailed manual test plan (with pictures) to explain what should happen when the graphical elements are invoked.](https://docs.google.com/document/d/1zk0iSlQMeo-QUfFKDz57KuuU5-b7ajrnxbD603LRIis/edit?usp=sharing)

## What Is Missing from the Project
None.