from random import choice
import re
from meaningless import WebExtractor # Meaningless extractor obtains necessary bible verses
import meaningless
from meaningless.utilities.exceptions import InvalidSearchError
import google.generativeai as genai
import os
from dotenv import load_dotenv

def bible_passage(output_translation="NIV", verse_max=2, newlines_max=4, test_mode=False):
    '''
    Obtains a bible passage using the meaningless extractor. 
    The passages are split into parts, which have their size restricted by a number of verses or newlines

    verse_max - The max number of verses that compose a part
    newlines_max - The max number of lines that compose a part - 1
    '''
    if test_mode:
    
        bible_books = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
        "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
        "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
        "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
        "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
        "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John",
        "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
        "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
        "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
        "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
        "Jude", "Revelation"]

        bible_editions = ["NIV", "ESV", "KJV", "NKJV", "NLT"]

        # Generate 10 random Bible books
        verse_reference = choice(bible_books)
        version = choice(bible_editions)
    
        extractor = WebExtractor(translation=version, output_as_list=True)
        verse_text = extractor.search(verse_reference)
        verse_remaining = len(verse_text)
        verse_count = 0
        part_count = 0
        part = ""
        parts = []

        for i, verse in enumerate(verse_text):
            part = f"{part}{verse}"

            # This ensures each slide has a consistent number of verses
            verse_count = (verse_count + 1) % verse_max
            # This is kept track of to ensure a partial collection at the end is accounted for
            verse_remaining -= 1
            # Each part consists of either a set number of verses OR an approximate set of lines.
            # There might be situations where a really long verse takes up an entire slide's worth of space,
            # or the alternative where lots of verses are placed onto one slide
            if verse_count <= 0 or verse_remaining <= 0 or part.count("\n") >= newlines_max:
                verse_count = 0  # Need to reset the verse count in case it's the other conditions that matched
                part_count += 1
                parts.append(part)
                part = ""
        
        return parts, verse_reference, version

    while True:
        verse_reference = input("Enter a Bible verse reference such as '2 Peter 1:5-11' (n for template, enter the required version in brackets if needed e.g. (ESV) )\n")
        
        if verse_reference.lower().strip() == "n":
            return 'T', 'T', output_translation
        pattern = r"\((.+)\)"
        output_translation = re.search(pattern, verse_reference).group(1) if re.search(pattern, verse_reference) else output_translation

        verse_reference = verse_reference.replace(f"({output_translation})", "").strip()


        
        try:
            extractor = WebExtractor(translation=output_translation, output_as_list=True)
            verse_text = extractor.search(verse_reference)
            break
        except meaningless.utilities.exceptions.UnsupportedTranslationError:
            print("Invalid translation entered, defaulting to specified default version")
            extractor = WebExtractor(output_as_list=True)
            verse_text = extractor.search(verse_reference)
            break
        except InvalidSearchError:
            go_again = input("No text found. Would you like to try again? (Y for yes, any other key to exit)\n")
            if go_again.lower().strip() == "y":
                continue
            else:
                return 'No text found', 'No text found', output_translation
        
            
            
    verse_remaining = len(verse_text)
    verse_count = 0
    part_count = 0
    part = ""
    parts = []

    for i, verse in enumerate(verse_text):
        part = f"{part}{verse}"

        # This ensures each slide has a consistent number of verses
        verse_count = (verse_count + 1) % verse_max
        # This is kept track of to ensure a partial collection at the end is accounted for
        verse_remaining -= 1
        # Each part consists of either a set number of verses OR an approximate set of lines.
        # There might be situations where a really long verse takes up an entire slide's worth of space,
        # or the alternative where lots of verses are placed onto one slide
        if verse_count <= 0 or verse_remaining <= 0 or part.count("\n") >= newlines_max:
            verse_count = 0  # Need to reset the verse count in case it's the other conditions that matched
            part_count += 1
            parts.append(part)
            part = ""
    
    return parts, verse_reference, output_translation


def bible_passage_auto(verse_reference: str, output_translation="NIV", verse_max=2, newlines_max=4):
    '''
    Obtains a bible passage using the meaningless extractor.
    The passages are split into parts, which have their size restricted by a number of verses or newlines

    verse_max - The max number of verses that compose a part
    newlines_max - The max number of lines that compose a part - 1
    '''

    if verse_reference.lower().strip() == "n":
        return 'T'

    try:
        extractor = WebExtractor(translation=output_translation, output_as_list=True)
        verse_text = extractor.search(verse_reference)
    except InvalidSearchError:
        # make a call to GenAI to try fix the input 
        # make sure GEMINI_API_KEY is defined in your .env file
        load_dotenv()

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        # Change model if needed
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f'You are a biblical scholar. For the provided passage, please attempt to get the bible passage this reference: {verse_reference} ({output_translation})'
        print(f'Prompting GenAI with {prompt}')

        # Now you can interact with the model
        response = model.generate_content(prompt)
        print(f'GenAI bible passage response: {response}')

        verse_text = response.text

    verse_remaining = len(verse_text)
    verse_count = 0
    part_count = 0
    part = ""
    parts = []

    for i, verse in enumerate(verse_text):
        part = f"{part}{verse}"

        # This ensures each slide has a consistent number of verses
        verse_count = (verse_count + 1) % verse_max
        # This is kept track of to ensure a partial collection at the end is accounted for
        verse_remaining -= 1
        # Each part consists of either a set number of verses OR an approximate set of lines.
        # There might be situations where a really long verse takes up an entire slide's worth of space,
        # or the alternative where lots of verses are placed onto one slide
        if verse_count <= 0 or verse_remaining <= 0 or part.count("\n") >= newlines_max:
            verse_count = 0  # Need to reset the verse count in case it's the other conditions that matched
            part_count += 1
            parts.append(part)
            part = ""

    return parts

def get_correct_copyright_message(bible_version: str) -> str:
    match bible_version:
        case "NIV":
            return """Scripture quotations taken from The Holy Bible, New International Version® NIV®
            Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.
            Used with permission. All rights reserved worldwide."""
        case "ESV":
            return """Scripture quotations are from The ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved.
            """
        case "NLT":
            return """Scripture quotations are taken from the Holy Bible, New Living Translation, Copyright © 1996, 2004, 2015 by Tyndale House Foundation. Used by permission of Tyndale House Publishers, Inc., Carol Stream, Illinois 60188. All rights reserved."""
        case "CEV":
            return """Scripture quotations marked (CEV) are from the Contemporary English Version Copyright © 1991, 1992, 1995 by American Bible Society. Used by Permission."""
        case "NASB":
            return """Scripture quotations taken from the (NASB®) New American Standard Bible®, Copyright © 1960, 1971, 1977, 1995, 2020 by The Lockman Foundation. Used by permission. All rights reserved. lockman.org"""
        case "NKJV":
            return """Scripture taken from the New King James Version®. Copyright © 1982 by Thomas Nelson. Used by permission. All rights reserved."""
        case _ :
            return "Public domain"
    
    return "Public domain"