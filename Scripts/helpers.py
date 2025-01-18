"""
Module containing various helper functions for creating powerpoints
"""
import subprocess
import platform
import os
import re
from datetime import datetime, timedelta
from song_finder import fetch_lyrics
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Global variable to store relative path information
scripts_folder = os.path.dirname(__file__)
input_file_folder = f'{scripts_folder}/../input_files'

def kill_powerpoint():
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


def calculate_nth_sunday(current_date, n):
    '''
    Calculates the date of the nth sunday from the current date
    '''
    days_until_sunday = (6 - current_date.weekday()) % 7  # Days until the next Sunday
    days_until_nth_sunday = days_until_sunday + (n - 1) * 7  # Days until the nth Sunday
    next_nth_sunday = current_date + timedelta(days=days_until_nth_sunday)
    return next_nth_sunday

def get_next_sunday(number=10):
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

def get_next_sunday_auto(output_time_format="%Y_%m_%d", number=10, user_input=2):
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

def parse_roster_row(date, roster_sheet_link):
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

def find_song_names(directory):
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
                    return fetch_lyrics(search_term)
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
