from dotenv import load_dotenv
import os, lyricsgenius, webbrowser, warnings
from random import randint
import helpers

# Path to the root directory containing "Songs" and "Complete Slides" directories
root_directory = f"{os.path.dirname(__file__)}/../"

load_dotenv()
# Put your own genius token here
genius_token = os.environ.get("GENIUS_TOKEN")

if genius_token == "":
    raise Exception

# Path to the "Songs" directory
songs_directory = os.path.join(root_directory, "songs")

# Modify the function to allow pressing enter ("e") to exit
def fetch_lyrics(song_name):

    while True:

        # Increase timeout if it isn't working
        try:
            genius = lyricsgenius.Genius(genius_token, timeout=100)
        except TypeError:
            raise Exception("Invalid Genius token. Please check your token and try again.")
        
        artist = input(f'Enter the artist for {song_name}: ').lower().strip().title()
        song_name = song_name.lower().strip().title()

        if artist != "":
            confirm_song_name = input(f"To confirm, you're looking for {song_name.replace('.pptx', '')} by {artist}: (Y to continue, Enter or 'e' to exit) ")
        else:
            confirm_song_name = input(f"To confirm, you're looking for {song_name.replace('.pptx', '')}: (Y to continue, Enter or 'e' to exit) ")
        
        # Check for exit condition
        if confirm_song_name.lower().strip() == "e":
            return ""

        # Searches the api for the song
        if confirm_song_name.lower().strip() == "y":
            song = genius.search_song(song_name.replace(".pptx", ""), artist, get_full_info=False)
            if song:
                new_formatted_lyrics = "\n".join([song.title, f"CCLI license number: {randint(10000000, 99999999)}\n", song.lyrics])
                print(new_formatted_lyrics[:500])
                
                keep_going = input("\nDoes the above sample look like what you're looking for? (Y to continue, a for again, 'e' to exit)\n")

                # Check for exit condition
                if keep_going.lower().strip() == "e":
                    return ""
                
                if keep_going.lower().strip() == "a":
                    continue
                
                # Save the text file
                new_song_directory = os.path.join(songs_directory, song_name)
                os.makedirs(new_song_directory, exist_ok=True)

                text_file_path = f"{new_song_directory}/{song_name.replace('.pptx', '')}_Lyrics.txt"
                # Write into the file
                if keep_going == "":
                    with open(text_file_path, "w", encoding='utf-8') as file:
                        # Make blank file if the user said so
                        file.write('Sample Song\nCCLI license number: Sample\n[Verse 1]\nSample Lyrics')
                else:
                    with open(text_file_path, "w", encoding='utf-8') as file:
                        file.write(new_formatted_lyrics)
                
                strip_lines(text_file_path)
                
                print("Lyrics saved to the file.")

                webbrowser.open_new_tab("file://" + text_file_path)
                
                return os.path.basename(text_file_path).replace('_Lyrics.txt', '')

            else:
                return "Lyrics not available for this song."
        else:
            return "Lyrics not available for this song."

def fetch_lyrics_auto(song_name, artist):

    # Increase timeout if it isn't working
    genius = lyricsgenius.Genius(genius_token, timeout=100)

    song_name = song_name.lower().strip().title()

    # Searches the api for the song
    if not helpers.is_running_in_ci():
        song = genius.search_song(song_name.replace(".pptx", ""), artist, get_full_info=False)
    else:
        warnings.warn(f"Warning: Cannot fetch lyrics for '{song_name}' in a CI context - You can either provide them manually when the PowerPoint file is available or re-run on a local environment to use the LyricsGenius API")
        song = {'title': song_name, 'lyrics': ''}

    if song:
        new_formatted_lyrics = "\n".join([song.title, f"CCLI license number: {randint(10000000, 99999999)}\n", song.lyrics])
        print(new_formatted_lyrics[:500])

        # Save the text file
        new_song_directory = os.path.join(songs_directory, song_name)
        os.makedirs(new_song_directory, exist_ok=True)

        text_file_path = f"{new_song_directory}/{song_name.replace('.pptx', '')}_Lyrics.txt"
        # Write into the file
        with open(text_file_path, "w", encoding="utf-8") as file:
            file.write(new_formatted_lyrics)

        strip_lines(text_file_path)

        print(f"Lyrics saved to the file. It can be viewed through an internet browser at: file://{text_file_path}")
        webbrowser.open_new_tab(f"file://{text_file_path}")
        return os.path.basename(text_file_path).replace('_Lyrics.txt', '')

def fetch_lyrics_auto_confirm(song_name, artist):

    # Increase timeout if it isn't working
    genius = lyricsgenius.Genius(genius_token, timeout=100)

    song_name = song_name.lower().strip().title()

    # Searches the api for the song
    if not helpers.is_running_in_ci():
        song = genius.search_song(song_name.replace(".pptx", ""), artist, get_full_info=False)
    else:
        warnings.warn(f"Warning: Cannot fetch lyrics for '{song_name}' in a CI context - You can either provide them manually when the PowerPoint file is available or re-run on a local environment to use the LyricsGenius API")
        song = {'title': song_name, 'lyrics': ''}

    if song:
        new_formatted_lyrics = "\n".join([song.title, f"CCLI license number: {randint(10000000, 99999999)}\n", song.lyrics])
        print(new_formatted_lyrics[:500])
        confirmation = input("Do the above lyrics look like what you're expecting? (Control + C to cancel) ")

        # Save the text file
        new_song_directory = os.path.join(songs_directory, song_name)
        os.makedirs(new_song_directory, exist_ok=True)

        text_file_path = f"{new_song_directory}/{song_name.replace('.pptx', '')}_Lyrics.txt"

        if os.path.exists(text_file_path):
            # warn user
            overwrite_perms = input("A song with the same name already exists, overwrite it? (Control + C to cancel) ")

        # Write into the file
        with open(text_file_path, "w", encoding="utf-8") as file:
            file.write(new_formatted_lyrics)

        strip_lines(text_file_path)

        print(f"Lyrics saved to the file. It can be viewed through an internet browser at: file://{text_file_path}")
        webbrowser.open_new_tab(f"file://{text_file_path}")
        return os.path.basename(text_file_path).replace('_Lyrics.txt', '')

def strip_lines(file_path):
    '''
    Removes all newlines without characters on the same line
    '''
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Strip leading and trailing whitespace from each line
    stripped_lines = [line.strip() for line in lines]
    for i in stripped_lines:
        if i == '':
            stripped_lines.remove(i)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(stripped_lines))

if __name__ == "__main__":
    song = input("Input song name: ")
    artist = input("Input artist name: ")
    fetch_lyrics_auto_confirm(song, artist)