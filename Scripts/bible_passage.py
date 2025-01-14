from random import choice
from meaningless import WebExtractor # Meaningless extractor obtains necessary bible verses
from meaningless.utilities.exceptions import InvalidSearchError

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

        # Generate 10 random Bible books
        verse_reference = choice(bible_books)
    
        extractor = WebExtractor(translation=output_translation, output_as_list=True)
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
        
        return parts, verse_reference

    while True:
        verse_reference = input("Enter a Bible verse reference such as '2 Peter 1:5-11' (n for template)\n")
        
        if verse_reference.lower().strip() == "n":
            return 'T', 'T'

        try:
            extractor = WebExtractor(translation=output_translation, output_as_list=True)
            verse_text = extractor.search(verse_reference)
            break
        except InvalidSearchError:
            go_again = input("No text found. Would you like to try again? (Y for yes, any other key to exit)\n")
            if go_again.lower().strip() == "y":
                continue
            else:
                return 'T', 'T'
            
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
    
    return parts, verse_reference

def bible_passage_auto(verse_reference, output_translation="NIV", verse_max=2, newlines_max=4):
    '''
    Obtains a bible passage using the meaningless extractor.
    The passages are split into parts, which have their size restricted by a number of verses or newlines

    verse_max - The max number of verses that compose a part
    newlines_max - The max number of lines that compose a part - 1
    '''

    if verse_reference.lower().strip() == "n":
        return 'T', 'T'

    try:
        extractor = WebExtractor(translation=output_translation, output_as_list=True)
        verse_text = extractor.search(verse_reference)
    except InvalidSearchError:
        return 'T', 'T'

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
