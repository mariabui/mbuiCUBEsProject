## Maria Bui
[CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission)

## Install and Run Directions
Run the ```main.py``` file.

## What the Project Does
The program uses the Wufoo API to download the entries data from a Wufoo form by sending an HTTP GET request, converting the HTTP GET response into JSON, and extracting the entries data from JSON. The entries data are saved to a text file and a database. The entries from the database are displayed in a GUI.

## Database Layout
The database contains an entries table that stores the entries data. The entries table consists of 24 columns with 21 of them corresponding to the fields in the [CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission) form. The remaining 3 columns correspond to the entry ID, creation date, and creator. For columns that correspond to checkbox fields, an entry has a value of 'Y' if the field was selected and 'N' otherwise.

## GUI Layout
The GUI consists of an 'Entries List' window on the left that displays the entries in a list and an 'Entry Data' window on the right that displays the complete entry data of the selected entry from the list. The 'Entries List' window shows a preview of each entry by displaying its associated id, first name, last name, and organization name and has a 'Quit' button in the bottom right corner. When the GUI launches, the first entry in the list is selected and displayed by default. Editing is disabled for the data fields in the 'Entry Data' window. Consequently, disabled checkbox fields are greyed out.

## What Is Missing from the Project
None.