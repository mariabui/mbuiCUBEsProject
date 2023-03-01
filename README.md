## Maria Bui
[CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission)

## Install and Run Directions
Run the ```main.py``` file.

## What the Project Does
The program uses the Wufoo API to download the entries data from a Wufoo form by sending an HTTP GET request, converting the HTTP GET response into JSON, and extracting the entries data from JSON. The entries data are saved to a text file and a database. The entries from the database are displayed in a GUI.

## Database Layout
The database contains an entries table that stores the entries data. The entries table consists of 24 columns with 21 of them corresponding to the fields in the [CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission) form. The remaining 3 columns correspond to the entry ID, creation date, and creator. For columns that correspond to checkbox fields, an entry has a value of 'Y' if the field was selected and 'N' otherwise.

## GUI Layout
When the GUI launches, a 'Choose One' window opens and prompts the user to click the corresponding button to choose to either:
1. update the data in the database, or 
2. run the data visualization.

The GUI remains running after updating the data in the database.

After an option is chosen, the 'Choose One' window closes and 3 windows open:
1. an 'Entries List' window on the left that displays the entries in a list,
2. an 'Entry Data' window in the center that displays the complete entry data of the selected entry from the list, and
3. a 'Claim' window OR a 'User Data' window on the right.

The 'Entries List' window shows a preview of each entry by displaying its associated id, first name, last name, and organization name and has a 'Quit' button in the bottom right corner. If the user has chosen to update the data in the database, the 'Entries List' window will display an updated list of entries.

The first entry in the list is selected and displayed in the 'Entry Data' window by default. Editing is disabled for the data fields in the 'Entry Data' window.

When an unclaimed entry is selected, the 'Claim' window is shown and prompts the user to provide their email, first name, last name, title, and department to claim the entry.

When a claimed entry is selected, the 'User Data' window is shown and displays the associated claimer's email, first name, last name, title, and department that they have provided.

## What Is Missing from the Project
None.