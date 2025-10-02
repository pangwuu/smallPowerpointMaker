# Troubleshooting document

## Help! The powerpoint doesn't seem to be generated.
1. Go to the [repo here](https://github.com/pangwuu/smallPowerpointMaker).
2. Check the actions tab, which should list `All workflows`
3. Check the most recent workflow, and see its status
4. If there has been no runs within the past week - head down to the steps listed in `The workflow didn't seem to have been run`
5. If you see a red X, it means the workflow has failed. Try to see what occured (invalid formatting or something else) and email panghowu@gmail.com with the error.
6. If you see a green workflow run in the past week, try 

### The workflow didn't seem to have been run
1. From the `Actions` tab, click `Create Powerpoint and push to main`
2. There should be a small bar saying 
> This workflow has a `workflow_dispatch` event trigger.
3. If this bar appears, click `Run workflow` at the right
4. Click the green `Run workflow` button to create a workflow manually

### Some parts of the powerpoint seem to be missing
This typically means that there was invalid formatting in the roster sheet. To fix it:
1. Check the spreadsheet to see if there are any invalid songs. These are any songs that are not in the `songs` directory
2. Check if the bible passage is valid and is typo free.
3. Rerun the workflow as highlighted in `The workflow didn't seem to have been run` above.

## How do I add new songs?
1. This is probably the most troublesome part of this program, and is typically easier if you clone the repository and make changes locally. Nevertheless, it is possible to do this online if you follow the instructions very carefully.

> If you need to add a new song on the day, it's probably better to just add it manually.

> These steps are for when you are adding a new song for future uses. Read very carefully.
### Steps for adding new songs using GitHub Web
2. Log into Github on an account with write permissions to this repository. If you'd like to be added as a collaborator email me or raise an issue panghowu@gmail.com
3. Click Add File --> Create new file
4. In the file path above, enter the path as
```smallPowerpointMaker/Songs/[YOUR SONG NAME]/[YOUR SONG NAME]_Lyrics.txt```
> Ensure this is entered correctly. Both file paths shouldn't be case sensitive but be sure to capitalise each word to conform to naming convention

> If you have a variant of a certain song, feel free to add it after to differentiate between songs, such as `In Christ Alone` and `In Christ Alone (Passion)`

> Typing the slashes ensures that **GitHub** creates and commits a new directory to store the text file in, which is what the program expects

5. Enter the Song title as the first line of the file
6. As the second line, keep it empty. Some older files has the CCLI number there but this has since been deprecated and isn't necessary to add for newer songs.
7. Enter the song with sections headers and lyrics. Some tips are below:
> Please ensure that each lyrics are preceeded by its section, such as Chorus, Prechorus, Verse 1, etc

> Each section **MUST** have square brackets surrounding them. This makes the program treat it as something different to song lyrics.

> By default, slides have **4** lines in them. To force a slide break and new slide, add a new section after the last lyric line. 

> Try to ensure each line is less than **60** characters as long lines could overflow when slides are generated

> Do not include any unecessary newlines, as these will be treated as text and hence create blank lines (unless that is what you want!)
8. Press `Commit changes...`
9. If this is a new song and this is being created in advance - click `Create a new branch` and create a description for the change.
10. If this is being created on the day/is an emergency, you probably should just add the song manually using powerpoint.

### Steps for adding new songs using GitHub codespaces or an IDE
1. Clone the repository
2. Add the songs using the format described above
3. Run the `new_powerpoint_maker.py` program manually and input the the name of the new song.
4. When prompted to search for a song - input `y`
5. When prompted to manually add the lyrics, also input `y`
6. From an IDE, this should open the new song file, which you can now add the lyrics in manually. 

> Be sure to follow all the conventions above. Using the program like this should allow inputs to be more consistent.

7. Commit the changes to a new branch and submit a PR. Remember that for the action to recognise the song it needs to first be in the main branch - so merge it if needed.

## What happens if the spreadsheet link changes?
1. The spreadsheet link is an environment variable in the `prod` environment. 
2. Go to Settings > Environments
3. If an environment called `prod` doesn't exist, create it
4. Click into the `prod` environment
5. Under `Environment variables`, click the pencil next to `ROSTER_SHEET_LINK` if the environment variable exists, or `Add environment variable` if it currently does not exist
6. In `value`, paste the link of to the Google sheet that is used for rostering

> Make sure that the Google sheet has view permissions for everybody


## Valid Roster Sheet Format

The script reads a **single row** from the sheet that corresponds to a specific Sunday.

Each row must contain **5 consecutive columns**, with the following required fields:

## Required Columns

| Column | Description              | Format & Example                                                                                                                                                  |
| ------ | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1      | **Date of Service**      | Must match the format `DD-Mon-YYYY` (e.g., `05-Oct-2025`). <br>• No leading zeros in the day (e.g., `5-Oct-2025`, not `05-Oct-2025`). <br>• Must be a **Sunday**. |
| 2      | **Speaker**              | The name of the speaker. <br>• If this cell contains the word `combined`, the script will interpret this as a combined service and translate lyrics.              |
| 3      | **Sermon Title / Topic** | The title or topic of the sermon. <br>Example: `The Good Shepherd`.                                                                                               |
| 4      | **Bible Passage**        | The passage reference. <br>• Any text inside parentheses will be ignored. <br>Example: `John 10:1–18 (NIV)` → stored as `John 10:1–18`.                           |
| 5      | **Worship Songs**        | A list of songs. Can be formatted either: <br>• One per line, or <br>• Comma-separated.                                                                           |

---

## Rows

* Each row represents a different **Sunday’s service**.
* The script identifies the correct row by matching the **date in the first column**.
* Ensure there is **only one row per date**.

---

## Example Roster Table

| Date        | Speaker    | Sermon Title      | Bible Passage | Worship Songs                                           |
| ----------- | ---------- | ----------------- | ------------- | ------------------------------------------------------- |
| 05-Oct-2025 | John Smith | The Good Shepherd | John 10:1–18  | Amazing Grace, How Great Thou Art, In Christ Alone      |
| 12-Oct-2025 | (Combined) Mark Smith   | United in Worship | Psalm 133     | 10,000 Reasons <br> Cornerstone <br> Great Are You Lord |

---
     
## How do I run tests?

> This program has no unit tests. Instead, tests are sanity tests designed to reflect if the final product works as intended. A limited set of songs will be used to validate if everything works fine

1. Clone this repo
2. Ensure that all environment variables are set up properly
3. Set up a virtual environment (optional but recommended)
```bash 
python -m venv <environment_name>
```

4. Activate the virtual environment

`source <environment_name>/bin/activate` On MacOS or Linux

`<environment_name>\Scripts\activate`
On Windows

5. Install required dependencies

```pip install -r REQUIREMENTS.txt```

6. Run `new_powerpoint_maker.py` and when it asks for test mode, input `t`
7. This should create a new directory `TEST` on your local machine, which will store all test files. View each one in order to see if the template looks good. 
