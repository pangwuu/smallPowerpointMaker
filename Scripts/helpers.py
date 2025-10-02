"""
Module containing various helper functions for creating powerpoints
"""
import subprocess
import platform
import os
import re
import csv
from datetime import datetime, timedelta
from typing import Set
import webbrowser
from song_finder import fetch_lyrics
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Global variable to store relative path information
scripts_folder = os.path.dirname(__file__)
input_file_folder = f'{scripts_folder}/../input_files'

def kill_powerpoint() -> None:
    '''
    Fixes an issue which occurs when the powerpoint app is already open, and hence the file is not written.
    '''
    # I chatGPTd this.
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "POWERPNT.EXE"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif system_platform in ["Linux", "Darwin"]:  # Linux or macOS
        subprocess.run(["killall", "Microsoft PowerPoint"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        print("Unsupported platform:", system_platform)


def calculate_nth_sunday(current_date: datetime, n: int) -> datetime:
    '''
    Calculates the date of the nth sunday from the current date
    '''
    days_until_sunday = (6 - current_date.weekday()) % 7  # Days until the next Sunday
    days_until_nth_sunday = days_until_sunday + (n - 1) * 7  # Days until the nth Sunday
    next_nth_sunday = current_date + timedelta(days=days_until_nth_sunday)
    return next_nth_sunday

def get_next_sunday(number=10) -> str:
    '''
    Obtains a required number of sundays from the current date
    '''
    while True:
        # Get the current date
        current_date = datetime.today()

        # Calculate and display the first 5 Sundays
        for n in range(1, number + 1):
            next_nth_sunday = calculate_nth_sunday(current_date, n)
            print(f"{n}. {next_nth_sunday.strftime('%Y-%m-%d')}")

        # Allow the user to select a Sunday
        user_input = input(f"Enter the number (1-{number}) to select a Sunday: ")

        try:
            selected_sunday = int(user_input)
            if 1 <= selected_sunday <= number:
                selected_date = calculate_nth_sunday(current_date, selected_sunday)
                print(f"You selected: {selected_date.strftime('%Y-%m-%d')}")
                break
            else:
                print(f"Invalid input. Please enter a number from 1 to {number}.")
                continue
        except ValueError:
            print(f"Invalid input. Please enter a number from 1 to {number}.")
            continue
        

    # Format the date as yy_mm_dd
    return selected_date.strftime("%Y_%m_%d")

def get_next_sunday_auto(output_time_format="%Y_%m_%d", number=10, user_input=1) -> str:
    '''
    Obtains a required number of sundays from the current date
    '''
    while True:
        # Get the current date
        current_date = datetime.today()

        # Calculate and display the first 5 Sundays
        for n in range(1, number + 1):
            next_nth_sunday = calculate_nth_sunday(current_date, n)
            print(f"{n}. {next_nth_sunday.strftime('%Y-%m-%d')}")

        selected_sunday = int(user_input)
        
        try:
            if 1 <= selected_sunday <= number:
                selected_date = calculate_nth_sunday(current_date, selected_sunday)
                print(f"You selected: {selected_date.strftime('%Y-%m-%d')}")
                break
            else:
                print(f"Invalid input. Defaulting to 1")
                selected_sunday = 1
                continue
        except ValueError:
            print(f"Invalid input. Defaulting to 1.")
            selected_sunday = 1
            continue

    # Format the date as yy_mm_dd or some other format
    return selected_date.strftime(output_time_format)

def parse_roster_row(date: str, roster_sheet_link: str) -> dict:
    '''
    Returns a dictionary of data items based on a row in the roster sheet for a particular date
    '''
    with urlopen(roster_sheet_link) as response:
        contents = response.read().decode('utf-8')

    soup = BeautifulSoup(contents, 'html.parser')
    # Find the Google Sheets row element for the specified date
    # The CSS class used to identify this element may be different per row, so just try a bunch of them until one of them is valid
    for s in range(4, 100):
        s4 = soup.find('td', string=date.lstrip('0'), attrs={'class' : f's{s}'})
        if s4:
            break

    td_list = s4.parent.select('td')
    BR_PLACEHOLDER = '||'
    data = {}
    i = 0
    for td in td_list:
        # Need to use a separator to nicely split apart <br> tags in a cell
        item = td.get_text(separator=BR_PLACEHOLDER).strip()
        if i == 0:
            data['date'] = item
        elif i == 1:
            data['speaker'] = item
        elif i == 2:
            data['topic'] = item
        elif i == 3:
            # TODO - add support for different bible editions in normal mode
            data['passage'] = re.sub(r"\(.*\)", "", item)
        elif i == 4:
            data['songs'] = item.split(BR_PLACEHOLDER)
            # Songs might be entered as a comma-separated string, which gets interpreted as a single song
            if len(data['songs']) == 1 and ',' in data['songs'][0]:
                data['songs'] = data['songs'][0].split(',')
        else:
            break
        i += 1
    return data

def get_spreadsheet_to_csv_file(url, file_path):
    '''
    Extracts spreadsheet cell data from a Google Sheets link and downloads them as a CSV file
    '''
    if not url:
        print("Warning: URL is not defined")
        return
    with urlopen(url) as response:
        contents = response.read().decode('utf-8')

    soup = BeautifulSoup(contents, 'html.parser')
    # May need to iterate through class names of format 's\d+'
    cells = soup.find_all('td', attrs={'class' : 's1'})

    # Use UTF-8-BOM encoding to allow for Unicode characters to be written to the file
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
        row_length = 3
        csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        row_data = []
        # Since cells are grabbed as a set of HTML elements, rely on each row having the same
        # number of columns in order to parse the rows correctly
        for cell in cells:
            cell_data = cell.get_text().strip()
            row_data.append(cell_data)
            if len(row_data) >= row_length:
                csv_writer.writerow(row_data)
                row_data = []
    print(f"CSV data is available at {file_path}")

def is_running_in_ci():
    # Reference: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables
    return ('CI' in os.environ and os.environ['CI']) or ('GITHUB_RUN_ID' in os.environ)

def find_song_names(directory: str) -> Set[str]:
    '''
    Finds all unique song .txt files that could be in the directory provided as an argument  
    '''
    last_dirs = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                last_dir = os.path.basename(root)
                last_dirs.add(last_dir)
    return last_dirs

def select_song(matching_songs):
    '''
    Allows the user to select a song based upon all songs that match the user's search request. 
    If nothing matches, the user can choose to add a new song and create a new .txt file for a new song if needed
    matching_songs - A list of all songs the user can select from

    Returns the matching song
    '''

    while True:
        while True:

            search_term = input('Search for a song (n to exit): ').lower().strip()

            if search_term == 'n':
                return False

            # Use filter() with a lambda function to filter exact matching songs
            filtered_songs = list(filter(lambda song: search_term in song.lower().strip(), matching_songs))

            # if len(filtered_songs) == 0:
            #     # Use fuzzywuzzy process.extract to find matches if you enter in a typo
            #     results = process.extract(search_term, matching_songs, limit=10)
                
            #     # Filter results based on a similarity threshold
            #     threshold = 80
            #     filtered_songs = [song for song, score in results if score >= threshold]

            if len(filtered_songs) > 0:
                print("Available songs:")
                for index, song_name in enumerate(filtered_songs, start=1):
                    print(f'{index}: {song_name}')
                break
            else:
                search = input('No matching songs - would you like to search for one?\n(y for yes, a to go again, n to exit): ').lower().strip()
                if search == 'y':
                    try:
                        return fetch_lyrics(search_term)
                    except Exception:
                        print("Invalid Genius token - try fixing your token or manually add the lyrics")
                        manual_add = input("Would you like to manually add the lyrics? (y for yes, n to exit): ").lower().strip()
                        if manual_add == 'y':
                            songs_directory = f"{os.path.dirname(__file__)}/../Songs"
                            new_song_directory = os.path.join(songs_directory, search_term.title())
                            os.makedirs(new_song_directory, exist_ok=True)
                            text_file_path = f"{new_song_directory}/{search_term.title()}_Lyrics.txt"
                            with open(text_file_path, "w") as file:
                                file.write(f'{search_term.title()}\nCCLI license number: 23847389\n[Verse 1]\nSample Lyrics\n[Chorus]\nSample Chorus')
                            webbrowser.open_new_tab("file://" + text_file_path)
                            return search_term.title()
                continue
                
        while True:
            try:
                choice = int(input("Enter the index of the song you want to select\n(-1 to cancel and skip ahead, -2 to search for a different term): "))
                if choice == -1:
                    return False
                elif choice == -2:
                    break
                if 1 <= choice <= len(filtered_songs):
                    return filtered_songs[choice - 1]  # Adjust index to 0-based
                else:
                    print("Invalid index. Please enter a valid index.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
