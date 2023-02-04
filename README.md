## Maria Bui
[CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission)

## Install and Run Directions
None needed beyond the basics.

## What the Project Does
The program uses the Wufoo API to download the entries data from a Wufoo form by sending an HTTP GET request, converting the HTTP GET response into JSON, and extracting the entries data from JSON. The entries data are saved to a text file and database.

## Database Layout
The database contains an entries table that stores the entries data. The entries table consists of 23 columns with 21 of them corresponding to the fields in the [CUBES Project Proposal Submission](https://mbui.wufoo.com/forms/cubes-project-proposal-submission) form. The remaining 2 columns correspond to the entry ID and creation date. For columns that correspond to checkbox fields, an entry will have a value of 'Yes' if the field was selected and 'No' otherwise.

## What Is Missing from the Project
None.