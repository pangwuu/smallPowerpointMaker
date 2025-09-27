import os, sys
from bible_passage import bible_passage_auto
from slide_builders import create_from_template, create_bulletin_slide, create_offering_slide, create_starting_slides, create_title_and_text_slide, create_title_slide, add_title_with_image_on_right, append_song_to_powerpoint
from helpers import get_next_sunday_auto, kill_powerpoint, find_song_names, parse_roster_row, is_running_in_ci
import PIL
from fuzzywuzzy import process
from song_finder import fetch_lyrics_auto
from dotenv import load_dotenv

# Global variable to store relative path information
scripts_folder = os.path.dirname(__file__)
load_dotenv()

def main():
    '''
    Creates a powerpoint with the required structure for BCCC from scratch. 
    The powerpoint will be saved in the folder "Complete slides" with a filename of the date which is selected by the user
    
    Powerpoints have the structure
    Title
    No phones
    A number of worship songs
    Bible reading intro
    Bible verses
    Announcements
    Tithing details
    Prayer points
    Mingle time slide
    '''

    print("Starting auto-script...")
    font_sizes_large = {'title': 40, 'song': 27, 'bible reading': 23, 'tithing': 16}
    font_sizes_medium = {'title': 50, 'song': 33, 'bible reading': 32, 'tithing': 23}
    font_sizes_small = {'title': 70, 'song': 53, 'bible reading': 43, 'tithing': 32}

    complete_ppt, template_path = create_from_template()
    roster_sheet_link = os.environ.get('ROSTER_SHEET_LINK')
    if not roster_sheet_link:
        print("No roster link provided, check the ROSTER_SHEET_LINK environment variable")
        sys.exit(2)

    # Get the file name of the newly created file
    saved_file_name = get_next_sunday_auto()
    spreadsheet_date = get_next_sunday_auto("%d-%b-%Y")
    sunday_data = parse_roster_row(spreadsheet_date, roster_sheet_link)
    print(f"Settings: {saved_file_name}, {sunday_data}")

    # Determine if we are going to add a communion slide (First sunday of every month)
    day_num = 0
    try:
        day_num = int(saved_file_name[-2:])
    except:
        print("Could not determine if this was the first sunday of the month, continuing")
    
    # Used later for communion slide
    communion = (1 <= day_num) and (day_num <= 7)
        
    powerpoint_path = f'{scripts_folder}/{saved_file_name}.pptx'.replace('/Scripts/', '/Complete slides/')

    if os.path.exists(powerpoint_path):
        print("Warning: {powerpoint_path} already exists, this will be overwritten")
        
    template_name = os.path.basename(template_path)
    
    used_font = font_sizes_medium
    if template_name.startswith('small'):
        used_font = font_sizes_small
    elif template_name.startswith('med'):
        used_font = font_sizes_medium
    elif template_name.startswith('large'):
        used_font = font_sizes_large
        
    complete_ppt = create_starting_slides(complete_ppt, used_font['title'], used_font['title'] - 10)

    song_names = find_song_names(f'{scripts_folder}/../')
    searched_songs = []
    print(song_names)
    
    for song in sunday_data["songs"]:
        if song.title() in song_names:
            searched_songs.append(song)
        else:
            # Use fuzzywuzzy process.extract to find matches if you enter in a typo
            results = process.extract(song, song_names, limit=10)
                
            # Filter results based on a similarity threshold
            threshold = 90
            filtered_songs = [result for result, score in results if score >= threshold]
            if len(filtered_songs) > 0:
                # The first song is *probably* correct, one would hope...
                searched_songs.append(filtered_songs[0])
            else:
                print(f"Info: Fetching lyrics for {song}...")
                lyrics = fetch_lyrics_auto(song, "")
                if lyrics and len(lyrics) > 0 and lyrics != "Lyrics not available for this song.":
                    searched_songs.append(song)
                else:
                    print(f"Warning: Could not find lyrics for {song}, skipping...")
    print(searched_songs)
    
    # Add all the songs to the powerpoint
    for song in searched_songs:
        if len(song) > 0:
            complete_ppt = append_song_to_powerpoint(song, complete_ppt, used_font['title'], used_font['song'])

    if communion:
        try:
            complete_ppt = add_title_with_image_on_right(complete_ppt, "Holy Communion", 'Communion', used_font['title'] - 10)
        except PIL.UnidentifiedImageError:
            # An error sometimes occurs (I have no idea why) when the image cannot be found. 
            # In this case just create a simple text slide without the image
            print("Warning: Could not find communion image, continuing without image")
            # complete_ppt = create_title_slide('Holy Communion', '', complete_ppt, used_font['title'])

    # Bible passage slide/s
    complete_ppt = add_title_with_image_on_right(complete_ppt, 'Bible reading', 'Bible', used_font['title'] - 10)

    # Get Bible passage text
    verse_references = []
    for reference in [sunday_data["passage"]]:

        verses = bible_passage_auto(reference)
        print(verses)

        try:
            verse_reference = reference.strip().lower().title()
            for verse in verses:
                # Create a verse slide for each verse 'group'
                complete_ppt = create_title_and_text_slide(verse_reference, verse, complete_ppt, used_font['title'], used_font['bible reading'])
            verse_references.append(verse_reference)

        except TypeError:
            print('No bible passage found - trying again! (n to exit)')
    
    create_bulletin_slide(complete_ppt.slides[0], complete_ppt, saved_file_name, searched_songs, verse_references, sunday_data["speaker"], sunday_data["topic"])

    '''
    TODO - Low priority. Create functionality to add custom announcements (maybe use the offering slide)
    '''

    # Announcements slide
    complete_ppt = create_title_slide('Announcements', '', complete_ppt, used_font['title'])
    
    # Tithing slide
    complete_ppt = create_offering_slide(complete_ppt, used_font['title'], used_font['tithing'])

    # Prayer points slide (identical to announcements)
    complete_ppt = create_title_slide('Prayer points', '', complete_ppt, used_font['title'])

    # Mingle time slide
    if os.path.exists(f'{scripts_folder}/../Images/Mingle/'):
        complete_ppt = add_title_with_image_on_right(complete_ppt, 'Mingle time!', 'Mingle', used_font['title'] - 10)
    else:
        complete_ppt = create_title_slide('Mingle time!', '', complete_ppt, used_font['title'])

    # Blindly overwrite file, may need to check if this has the potential to corrupt a file
    if os.path.exists(powerpoint_path):
        print("Overwriting existing file...")
        kill_powerpoint()
    complete_ppt.save(powerpoint_path)

    if not is_running_in_ci():
        if os.path.exists(powerpoint_path):
            if sys.platform.startswith('darwin'):  # macOS
                os.system(f'open "{powerpoint_path}"')
            elif sys.platform.startswith('win'):  # Windows
                os.startfile(powerpoint_path)
            elif sys.platform.startswith('linux'):  # Linux
                os.system(f'xdg-open "{powerpoint_path}"')
            else:
                print("Unsupported platform")
        else:
            print(f"File not found: {powerpoint_path}")
        
if __name__ == "__main__":
    main()