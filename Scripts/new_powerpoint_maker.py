import os, sys
import webbrowser
from bible_passage import bible_passage, get_correct_copyright_message
from slide_builders import create_from_template, create_bulletin_slide, create_offering_slide,create_starting_slides, create_title_and_text_slide, create_title_slide, add_title_with_image_on_right, append_song_to_powerpoint, append_song_to_powerpoint_translated
from helpers import get_next_sunday, kill_powerpoint, find_song_names, select_song 
from test import test
import PIL

# Global variable to store relative path information
scripts_folder = os.path.dirname(__file__)
input_file_folder = f'{scripts_folder}/../input_files'

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

    font_sizes_large = {'title': 40, 'song': 27, 'bible reading': 23, 'tithing': 16}
    font_sizes_medium = {'title': 50, 'song': 33, 'bible reading': 32, 'tithing': 23}
    font_sizes_small = {'title': 70, 'song': 53, 'bible reading': 43, 'tithing': 32}

    # Open up the roster when running
    test_mode = input("Test mode? (t for yes, o to open planning sheet): ").lower().strip()
    if test_mode == 't':
        test()
        return
    
    templete_select = input("Would you like to select a template? (y for yes, any other key for a random template): ")

    complete_ppt, template_path = create_from_template(False, templete_select)
    if "o" in test_mode:
        roster_sheet_link = 'https://docs.google.com/spreadsheets/d/1vgvPxJTzr0o1MUUaGb5AJqG6-WQL1PLzHHrwkAZPjQg/edit?gid=0#gid=0'
        browser = webbrowser.get()
        browser.open(roster_sheet_link, new=0)
    
    translate = False
    language = 'Chinese (Simplified)'
    lang_input = input("Would you like to translate song lyrics? (y for yes, any other key to leave): ")
    if lang_input.strip().lower() == 'y':
        translate = True
        language = input("What language would you like to translate to? (Default: Chinese (Simplified), enter the language if you'd like another language, n to not translate): ")
        if language.lower().strip() == 'n':
            translate = False
            language = None


    # Get the file name of the newly created file
    saved_file_name = get_next_sunday()

    # Determine if we are going to add a communion slide (First sunday of every month)
    day_num = 0
    try:
        day_num = int(saved_file_name[-2:])
    except:
        print("Could not determine if this was the first sunday of the month, continuing")
    
    # Used later for communion slide
    communion = False
    if (1 <= day_num) and (day_num <= 7):
        communion = True
        
    powerpoint_path = f'{scripts_folder}/{saved_file_name}.pptx'.replace('/Scripts/', '/Complete slides/')

    if os.path.exists(powerpoint_path):
        proceed = input('This file already already exists. Proceed anyway? (n to stop, p to preview file)\n').lower().strip()
        if proceed == 'n':
            return
        elif proceed == 'p':
            webbrowser.open(f"file://{powerpoint_path}")

    template_name = os.path.basename(template_path)
    
    if template_name.startswith('small'):
        used_font = font_sizes_small
    elif template_name.startswith('med'):
        used_font = font_sizes_medium
    elif template_name.startswith('large'):
        used_font = font_sizes_large
        
    complete_ppt = create_starting_slides(complete_ppt, used_font['title'], used_font['title'] - 10)

    song_names = find_song_names(f'{scripts_folder}/../')
    searched_songs = []

    # Select all songs
    while True:

        while True:
            result = select_song(song_names)
            if not result:
                break
            elif result != "Lyrics not available for this song.":
                searched_songs.append(result)
        
        # Allows the user to 
        print('Song order: ')
        for index, song in enumerate(searched_songs, start=1):
            print(f'{index}: {song}')
            
        
        confirm = input('Confirm song selection? (n to cancel, a for again, Enter to continue): ').lower().strip()

        if confirm == 'n':
            return
        elif confirm == 'a':
            searched_songs = []
            continue

        break
    
    # Add all the songs to the powerpoint
    if language:
        for song in searched_songs:
            complete_ppt = append_song_to_powerpoint_translated(song, complete_ppt, used_font['title'], used_font['song'], 2, language)
    else:
        for song in searched_songs:
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
    translation = "NIV"
    used_translations = []

    while True:

        verses, reference, translation = bible_passage()
        if translation not in used_translations:
            used_translations.append(translation)

        try:
            verse_reference = reference.strip().lower().title()
            for verse in verses:
                # Create a verse slide for each verse 'group'
                complete_ppt = create_title_and_text_slide(f"{verse_reference} ({translation})", verse, complete_ppt, used_font['title'], used_font['bible reading'])
            verse_references.append(verse_reference)

        except TypeError:
            print('No bible passage found - trying again! (n to exit)')
        
        another_bible_passage = input('Would you like to include another bible passage? (y for yes, any other key to exit): ').lower().strip()
        if another_bible_passage != 'y':
            break
    
    full_message_list = []
    for translation in used_translations:
        full_message_list.append(get_correct_copyright_message(translation))
    
    full_message = "\n\n".join(full_message_list)

    create_title_and_text_slide("", full_message, complete_ppt, 8, 12)
    
    create_bulletin_slide(complete_ppt.slides[0], complete_ppt, saved_file_name, searched_songs, verse_references)

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
    complete_ppt = add_title_with_image_on_right(complete_ppt, 'Mingle time!', 'Mingle', used_font['title'] - 10)

    # Save the file with another warning if you're overwriting a file
    while True:
        if os.path.exists(powerpoint_path):
            proceed = input('Are you sure you want to overwrite the existing file? (y to proceed, n to exit)\n').lower().strip()
            if proceed == 'y':
                kill_powerpoint()
                complete_ppt.save(powerpoint_path)
                break
            elif proceed == 'n':
                return
        else:
            complete_ppt.save(powerpoint_path)
            break

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