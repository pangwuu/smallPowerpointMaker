import google.generativeai as genai
import os
from dotenv import load_dotenv
from functools import cache

@cache
def translate_with_gemini(text: str, translated_language: str,  start_language: str='English') -> str:
    # make sure GEMINI_API_KEY is defined in your .env file
    load_dotenv()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Change model if needed
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f'''
You are a song translator. For the song below, please translate the song line by line into {translated_language}.

Make sure the number of syllables on each {translated_language} line match up with the number of syllables in each {start_language} line. 

Since this song is going to be sung in church matching the syllables in each {translated_language} line to the number of syllables in each {start_language} line is also very important.

Make sure your output format alternates lines of {start_language} and {translated_language} simplified. For example

{start_language} LINE
{translated_language} LINE
{start_language} LINE
{translated_language} LINE

{text}

DO NOT PROVIDE ANY OTHER OUTPUTS OTHER THAN THE SONG LINES IN THE FORMAT ABOVE 
'''

    # Now you can interact with the model
    response = model.generate_content(prompt)

    return response.text

if __name__ == '__main__':
    print(translate_with_gemini("""What gift of grace is Jesus, my Redeemer
    There is no more for Heaven now to give
    He is my joy, my righteousness, and freedom
    My steadfast love, my deep and boundless peace""", "Chinese (Simplified)"))


