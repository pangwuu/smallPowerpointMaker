## To find the slides for this week
1. Go to the "Complete slides" folder
2. Find the file with the filename of today's date (should be right at the bottom)

## To set up GitHub Actions automation pipeline
1. Clone or fork this repo
2. In GitHub, ensure workflows are enabled under Settings > Actions > General > Actions permissions
2. In GitHub, create a new environment called `prod` under Settings > Environments
3. Add the following secrets into the `prod` environment:
   - `CCLI_URL`: URL of a Google Sheets document mapping song names & their CCLI numbers
   - `GENIUS_TOKEN`: API token for the LyricsGenius REST API
4. Add the following variables into the `prod` environment:
   - `CCLI_NUM`: CCLI number of the organisation using the generated PowerPoint files
5. In GitHub, the Actions tab should show available workflows.

## Notes
- Requires `lyricsgenius` with version 3.2.0 or higher
