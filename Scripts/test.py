
from slide_builders import create_from_template, create_offering_slide,create_starting_slides, create_title_and_text_slide, create_title_slide, add_title_with_image_on_right, append_song_to_powerpoint, append_song_to_powerpoint_translated
from helpers import scripts_folder
from bible_passage import bible_passage, get_correct_copyright_message
import PIL
import os

# Global variable to store relative path information
input_file_folder = f'{scripts_folder}/../input_files'

def test():
    # Create starting slides
    test_ppts = create_from_template(test_mode=True)
    
    try:
        os.mkdir(f'{scripts_folder}/../TEST')
    except:
        pass

    count = 0

    font_sizes_large = {'title': 40, 'song': 27, 'bible reading': 23, 'tithing': 16}
    font_sizes_medium = {'title': 50, 'song': 33, 'bible reading': 32, 'tithing': 23}
    font_sizes_small = {'title': 70, 'song': 53, 'bible reading': 43, 'tithing': 32}

    for my_ppt in test_ppts:
        count += 1
        # new_ppt = create_from_template(test_mode=True)
        # If we return a list, then we are in test mode. Please create it in a new directory with ALL templates
        powerpoint_path = f'{scripts_folder}/../TEST/TEST_{count}.pptx'.replace('/Scripts/', '/Complete slides/')
        
        ppt_obj = my_ppt.presentation
        ppt_font_size = my_ppt.font_size
        
        if ppt_font_size == 'small':
            used_font = font_sizes_small
        elif ppt_font_size == 'medium':
            used_font = font_sizes_medium
        elif ppt_font_size == 'large':
            used_font = font_sizes_large
        
        ppt_obj = create_starting_slides(ppt_obj, used_font['title'], used_font['title'] - 10)

        searched_songs = os.listdir(f'{scripts_folder}/../Songs')
        try:
            searched_songs.remove(".DS_Store")
        except ValueError:
            pass
        # searched_songs = ["Reckless Love"]

        songs = 0
        for song in searched_songs:
            if songs <= 2:
                ppt_obj = append_song_to_powerpoint(song, ppt_obj, used_font['title'], used_font['song'])
                ppt_obj = append_song_to_powerpoint_translated(song, ppt_obj, used_font['title'], used_font['song'], 2)
            songs += 1
        
        # Test communion slide
        try:
            ppt_obj = add_title_with_image_on_right(ppt_obj, "Holy Communion", 'Communion', used_font['title'] - 10)
        except PIL.UnidentifiedImageError:
            print("Warning: could not find communion image, continuing without image")
            # ppt_obj = create_title_slide('Holy Communion', '', ppt_obj, used_font['title'])
        
        verses, reference, translation = bible_passage(test_mode=True)

        for i in verses:
            # Create a verse slide for each verse 'group'
            ppt_obj = create_title_and_text_slide(f"{reference.strip().lower().title()} ({translation})", i, ppt_obj, used_font['title'], used_font['bible reading'])
        
        ppt_obj = create_title_and_text_slide("", get_correct_copyright_message(translation), ppt_obj, 8, 8)

        # Announcements slide
        ppt_obj = create_title_slide('Announcements', '', ppt_obj, used_font['title'])
        
        # Tithing slide
        ppt_obj = create_offering_slide(ppt_obj, used_font['title'] - 10, used_font['tithing'])

        # Prayer points slide (identical to announcements)
        ppt_obj = create_title_slide('Prayer points', '', ppt_obj, used_font['title'])

        # Mingle time slide
        ppt_obj = add_title_with_image_on_right(ppt_obj, 'Mingle time!', 'Mingle', used_font['title'] - 10)

        ppt_obj.save(powerpoint_path)
        print(f'Test {count} created - {ppt_font_size}')
    return 
