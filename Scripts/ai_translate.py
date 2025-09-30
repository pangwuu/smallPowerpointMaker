import google.generativeai as genai
import os
from dotenv import load_dotenv
from functools import cache

@cache
def translate_with_gemini(text: str, translated_language: str,  start_language: str='English') -> str:
    load_dotenv()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f'''
You are a song translator. For the song below, please translate the song line by line into {translated_language}.

Make sure the number of syllables on each {translated_language} line match up with the number of syllables in each {start_language} line. 

Your priorities are:
1. To ensure that the translated version is a faithful representation of the original version of the song
2. Since this song is going to be sung in church matching the syllables in each {translated_language} line to the number of syllables in each {start_language} line is also important. However, it is not as important as priority 1.

Make sure your output format alternates lines of {start_language} and {translated_language} simplified. Provide the result as a string representation of a python 2D array, and provide the translation after the english line/s. For example

['Verse 1', 'ENGLISH LINE 1\nENGLISH LINE 2\n'] should be changed to
['Verse 1', 'ENGLISH LINE 1\nTRANSLATED LINE 1\nENGLISH LINE 2\nTRANSLATED LINE 2']

{text}

DO NOT PROVIDE ANY OTHER OUTPUTS OTHER THAN THE PYTHON 2D ARRAY AS A STRING. 
'''

    # Now you can interact with the model
    response = model.generate_content(prompt)

    # If theres a little markdown syntax we can remove it 
    response_string = response.text
    response_string = response_string[response.text.index('['):-3]

    return response_string

print(translate_with_gemini('''
                            [['Verse 1', 'With this heart open wide\nFrom the depths, from the heights\n'], ['Verse 1', 'I will bring a sacrifice\n\n'], ['Verse 1', 'With these hands lifted high\nHear my song, hear my cry\n'], ['Verse 1', 'I will bring a sacrifice\nI will bring a sacrifice\n'], ['Chorus', "I lay me down, I'm not my own\nI belong to You alone\n"], ['Chorus', 'Lay me down, lay me down\n\n'], ['Chorus', 'Oh, hand on my heart\nThis much is true\n'], ['Chorus', "There's no life apart from You\nLay me down, lay me down\n"], ['Verse 2', 'Letting go of my pride\nGiving up all my rights\n'], ['Verse 2', 'Take this life and let it shine, shine, shine\nTake this life and let it shine\n'], ['Chorus', "I lay me down, I'm not my own\nI belong to You alone\n"], ['Chorus', 'Lay me down, lay me down\n\n'], ['Chorus', 'Oh, hand on my heart\nThis much is true\n'], ['Chorus', "There's no life apart from You\n\n"], ['Chorus', 'Lay me down, lay me down\nOh, lay me down, lay me down\n'], ['Bridge', 'It will be my joy to say\n"Your will, Your way"\n'], ['Bridge', 'It will be my joy to say\n"Your will, Your way"\n'], ['Bridge', 'It will be my joy to say\n"Your will, Your way, always"\n'], ['Bridge', '\n\n'], ['Bridge', 'It will be my joy to say\n"Your will, Your way"\n'], ['Bridge', 'It will be my joy to say\n"Your will, Your way"\n'], ['Bridge', 'It will be my joy to say\n"Your will, Your way, always"\n'], ['Chorus', "I lay me down, I'm not my own\nI belong to You alone\n"], ['Chorus', 'Lay me down, lay me down\n\n'], ['Chorus', 'Oh, hand on my heart\nThis much is true\n'], ['Chorus', "There's no life apart from You\nLay me down, lay me down\n"], ['Chorus', "\nI lay me down, I'm not my own\n"], ['Chorus', 'I belong to You alone\nLay me down, lay me down\n'], ['Chorus', '\nOh, hand on my heart\n'], ['Chorus', "This much is true\nThere's no life apart from You\n"], ['Chorus', 'Lay me down, lay me down, oh\nLay me down, lay me down, oh\n']]''', 'Chinese (Simplified)'))

# @cache
# def translate_line_with_gemini(song_line: str, translated_language: str,  start_language: str='English') -> str:
#     load_dotenv()

#     genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#     model = genai.GenerativeModel('gemini-2.5-flash')

#     prompt = f'''
# For the line below, translate the song line by line into {translated_language}. Make sure the translated meaning is faithful, and the number of syllables of the {translated_language} line is the same (or similar) up with the number of syllables in each {start_language} line.

# Your output format should just be the translated line, with nothing else.

# {song_line}
# '''

#     # Now you can interact with the model
#     response = model.generate_content(prompt)
#     return response.text
