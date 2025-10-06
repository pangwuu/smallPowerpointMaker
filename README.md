## To find the slides for this week
1. Go to [the website which holds generated powerpoints](https://pangwuu.github.io/smallPowerpointMaker/).
2. If that fails, attempt to locate the file under `Complete slides` (for Linux and MacOS) or `Scripts` (for Windows)
3. Find the file with the filename of today's date (should be right at the bottom)
4. When opening the file using Microsoft PowerPoint, you might only see a bunch of empty slides. This can be due to Slide Master view being used, so follow the below steps to self-diagnose:
   - In the topmost tab, if you see a "Slide Master" tab then you are using Slide Master View.
   - Go to the "View" tab and select Normal.
   - This will switch to Normal View where the expected slides should now be visible.

## If you have other issues
Check the troubleshooting steps [here](https://pangwuu.github.io/smallPowerpointMaker/TROUBLESHOOTING.html).

## To set up GitHub Actions automation pipeline
1. Clone or fork this repo
2. In GitHub, ensure workflows are enabled under Settings > Actions > General > Actions permissions
2. In GitHub, create a new environment called `prod` under Settings > Environments
3. Add the following secrets into the `prod` environment:
   - `CCLI_URL`: URL of a Google Sheets document mapping song names & their CCLI numbers
   - `GENIUS_TOKEN`: API token for the LyricsGenius REST API to add new songs.
   - `GEMINI_API_KEY`: API key for the Google Gemini API. An optional method used to translate song lyrics as used by combined service. If needed, you can generate a new key [here](https://aistudio.google.com/api-keys).
4. Add the following variables into the `prod` environment:
   - `CCLI_NUM`: CCLI number of the organisation using the generated PowerPoint files
   - `ROSTER_SHEET_LINK`: The link which holds the roster for service. 
5. In GitHub, the Actions tab should show available workflows.
6. If you wish to deploy the GitHub Pages site, make sure to enable pages under Settings > Pages > Build and Deployment. Select the `source` to be `GitHub Actions`.

## Notes
- Requires `lyricsgenius` with version 3.2.0 or higher
- For translated versions, requires `googletrans` AND/OR a Google Gemini API key