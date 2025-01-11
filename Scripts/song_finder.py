import os, lyricsgenius, re, webbrowser
from random import randint
from bs4 import BeautifulSoup  # This is only required as part of LyricsGeniusWithHotfix

# Path to the root directory containing "Songs" and "Complete Slides" directories
root_directory = f"{os.path.dirname(__file__)}/../"

# Path to the "Songs" directory
songs_directory = os.path.join(root_directory, "songs")

class LyricsGeniusWithHotfix(lyricsgenius.genius.Genius):
    """
    TLDR: This applies an updated lyrics() function onto the Genius class that removes metadata and other cruft.

    Too Long But I Want To Read Anyway:

    There was a change committed into the LyricsGenius repo which addresses the issue where metadata such as contributor counts and other
    unrelated contents were incorrectly being treated as part of the song.
    (see https://github.com/johnwmillr/LyricsGenius/commit/a702f5f0161bfcb28dd52dbfa96ab3192c36ed93)

    As of writing, this change has been staged into the master branch but there haven't been any releases made by the library maintainers
    so that the newest version of the Genius class is available, which means this updated functionality is locked away until the next
    release happens (which looks fairly unlikely, based on the GitHub history since 2022).

    Since the change only affects a single function in the Genius class, it's possible to apply this fix manually using a
    class which extends from the Genius class in such a way that everything is the same EXCEPT the lyrics() function, which overrides
    the old function with the updated one.

    Once the next release of the lyricsgenius library happens (eventually?), this class is no longer required.
    """
    def lyrics(self, song_id=None, song_url=None, remove_section_headers=False):
        msg = "You must supply either `song_id` or `song_url`."
        assert any([song_id, song_url]), msg
        if song_url:
            path = song_url.replace("https://genius.com/", "")
        else:
            path = self.song(song_id)['song']['path'][1:]

        # Scrape the song lyrics from the HTML
        html = BeautifulSoup(
            self._make_request(path, web=True).replace('<br/>', '\n'),
            "html.parser"
        )

        # Determine the class of the div
        divs = html.find_all("div", class_=re.compile("^lyrics$|Lyrics__Container"))
        if divs is None or len(divs) <= 0:
            if self.verbose:
                print("Couldn't find the lyrics section. "
                      "Please report this if the song has lyrics.\n"
                      "Song URL: https://genius.com/{}".format(path))
            return None

        lyrics = "\n".join([div.get_text() for div in divs])

        # Remove [Verse], [Bridge], etc.
        if self.remove_section_headers or remove_section_headers:
            lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
            lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
        return lyrics.strip("\n")

# Modify the function to allow pressing enter ("e") to exit
def fetch_lyrics(song_name):

    while True:

        # Increase timeout if it isn't working
        # genius = LyricsGeniusWithHotfix(genius_token, timeout=100)
        
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

        # Open a browser tab to search for the song lyrics
        if confirm_song_name.lower().strip() == "y":
            search_query = f"{song_name.replace('.pptx', '')} lyrics {artist}"
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

            header = "\n".join([song_name, f"CCLI license number: {randint(10000000, 99999999)}\n"])
            
            # Save the text file
            new_song_directory = os.path.join(songs_directory, song_name)
            os.makedirs(new_song_directory, exist_ok=True)

            text_file_path = f"{new_song_directory}/{song_name.replace('.pptx', '')}_Lyrics.txt"
            # # Write into the file
            # if keep_going == "":
            #     with open(text_file_path, "w") as file:
            #         # Make blank file if the user said so
            #         file.write('Sample Song\nCCLI license number: Sample\n[Verse 1]\nSample Lyrics')
            # else:

            with open(text_file_path, "w") as file:
                file.write(header)
            
            strip_lines(text_file_path)
            
            print("Headers saved to the file. Please manually paste lyrics and headers into the file")

            webbrowser.open_new_tab("file://" + text_file_path)
            
            return os.path.basename(text_file_path).replace('_Lyrics.txt', '')
        else:
            return "Lyrics not available for this song."

def strip_lines(file_path):
    '''
    Removes all newlines without characters on the same line
    '''
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Strip leading and trailing whitespace from each line
    stripped_lines = [line.strip() for line in lines]
    for i in stripped_lines:
        if i == '':
            stripped_lines.remove(i)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(stripped_lines))