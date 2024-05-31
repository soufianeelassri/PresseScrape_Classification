# Import necessary libraries
from datetime import datetime
import locale
import spacy
from collections import Counter
from heapq import nlargest

def parse_arabic_date(date_string):
    
    # Dictionary mapping Arabic month names to English
    arabic_to_english_months = {
        'يناير': 'January',
        'فبراير': 'February',
        'مارس': 'March',
        'أبريل': 'April',
        'ماي': 'May',
        'يونيو': 'June',
        'يوليوز': 'July',
        'غشت': 'August',
        'شتنبر': 'September',
        'أكتوبر': 'October',
        'نونبر': 'November',
        'دجنبر': 'December'
    }

    # Dictionary mapping Arabic day names to English
    arabic_to_english_days = {
        'السبت': 'Saturday',
        'الأحد': 'Sunday',
        'الإثنين': 'Monday',
        'الثلاثاء': 'Tuesday',
        'الأربعاء': 'Wednesday',
        'الخميس': 'Thursday',
        'الجمعة': 'Friday'
    }

    # Replace Arabic month names with English equivalents
    for arabic, english in arabic_to_english_months.items():
        date_string = date_string.replace(arabic, english)

    # Replace Arabic day names with English equivalents
    for arabic, english in arabic_to_english_days.items():
        date_string = date_string.replace(arabic, english)

    # Remove any hyphens from the date string
    date_string = ''.join([char for char in date_string if char != '-'])
    
    # Define the date format to be used for parsing
    date_format = '%A %d %B %Y %H:%M'

    # Set the locale to ensure consistent parsing
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    # Parse the date string into a datetime object using the specified format
    return datetime.strptime(date_string, date_format)

# Load the English language model
nlp = spacy.blank('ar')

def key_point(text):

    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract tokens, excluding stopwords, punctuation, and newline characters
    tokens = [token.text for token in doc 
          if not token.is_stop and
          not token.is_punct and
          token.text != '\n']
    
    # Calculate word frequencies
    wordFrq = Counter(tokens)
    maxFrq = max(wordFrq.values())
    
    # Normalize word frequencies
    for word in wordFrq.keys():
        wordFrq[word] = wordFrq[word] / maxFrq
        
    if 'sentencizer' not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")
    doc = nlp(text)
    
    # Extract sentences
    sentences = [sent.text for sent in doc.sents]
    
    # Calculate sentence scores based on word frequencies
    sent_score = {}
    for sent in sentences:
        for word in sent.split():
            if word in wordFrq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = wordFrq[word]
                else: sent_score[sent] += wordFrq[word]
    
    # Return top sentences as summary
    summary = nlargest(1, sent_score, key=sent_score.get)
    return " ".join(summary).strip()

def remove_stop_punc(text):
    
    # Tokenize the text using spaCy
    doc = nlp(text)
    
    # Extract words from the tokens that are not stop words or punctuation
    words = [token.text for token in doc if not token.is_stop and not token.is_punct]
    
    for i in range(len(words)):
        # Convert the word to a list of characters
        word = [word for word in words[i]]
        for j in range(len(word)):
            # Check if the character is not alphanumeric
            if not word[j].isalnum():
                # Replace non-alphanumeric characters with a space
                words[i] = words[i].replace(words[i][j], ' ')
    # Join the words back into a single string       
    return ' '.join(words)