## Maria Bui
[CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission)

## Install and Run Directions
Run the ```main.py``` file.

## What the Project Does
The program uses the Wufoo API to download the entries data from a Wufoo form by sending an HTTP GET request, converting the HTTP GET response into JSON, and extracting the entries data from JSON. The entries data are saved to a text file and a database. The entries from the database are displayed in a GUI.

## Database Layout
The database contains an entries table that stores the entries data. The entries table consists of 24 columns with 21 of them corresponding to the fields in the [CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission) form. The remaining 3 columns correspond to the entry ID, creation date, and creator. For columns that correspond to checkbox fields, an entry has a value of *Y* if the field was selected and *N* otherwise.

## GUI Layout
The GUI consists of 5 windows:
1. *Choose One*
   * Opens on program startup.
   * Prompts the user to choose to either update the data in the database or run the data visualization.
   * GUI remains running after updating the data in the database.
2. *Entries List*
   * Located on the left of the screen.
   * Displays the entries in a list. If the user has chosen to update the data in the database, an updated list of entries is displayed.
   * Shows a preview of each entry by displaying its associated id, first name, last name, and organization name.
   * Has a *Quit* button in the bottom right corner of the window.
3. *Entry Data*
   * Located in the center of the screen.
   * Displays the complete entry data of the selected entry from the list. The first entry in the list is selected and displayed by default.
   * Editing is disabled for the data fields.
4. *Claim*
   * Located on the right of the screen.
   * Prompts the user to provide their email, first name, last name, title, and department to claim the selected entry.
   * When an unclaimed entry is selected, this window is shown.
5. *User Data*
   * Located on the right of the screen.
   * Displays the selected entry's claimer's email, first name, last name, title, and department that they have provided.
   * When a claimed entry is selected, this window is shown.

## What Is Missing from the Project
None.