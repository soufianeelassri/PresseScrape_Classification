# Import necessary libraries
import pandas as pd
from functions import parse_arabic_date, key_point, remove_stop_punc
import json

# Load the JSON data into a Python dictionary 
with open('hespress.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a pandas DataFrame from the loaded JSON data
data = pd.DataFrame(data)

# Rename the columns of the DataFrame
data.columns = ['title', 'category', 'content', 'key_words', 'source', 'date']

# Join the lists of key words into comma-separated strings
data['key_words'] = data['key_words'].apply(lambda x: ', '.join(x))

# Remove duplicate rows in place
data.drop_duplicates(inplace=True)

# Remove rows from DataFrame data where the 'category' column does not match one of the specified categories
data.drop(data[~data['category'].isin(['اقتصاد', 'رياضة', 'سياسة', 'فن وثقافة'])].index, inplace=True)

# Apply the parse_arabic_date function to convert Arabic date strings to English datetime objects
data['date'] = data['date'].apply(lambda date: parse_arabic_date(date))

# Extract year, month (numerical and name), day (numerical and name), hour, and minute from the datetime objects
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['month_name'] = data['date'].dt.month_name()
data['day'] = data['date'].dt.day
data['day_name'] = data['date'].dt.day_name()
data['hour'] = data['date'].dt.hour
data['minute'] = data['date'].dt.minute

# Drop the original 'date' column from the DataFrame
data.drop(columns=['date'], inplace=True)

# Dictionary mapping English month names to Arabic
english_to_arabic_months = {
    'January': 'يناير',
    'February': 'فبراير',
    'March': 'مارس',
    'April': 'أبريل',
    'May': 'ماي',
    'June': 'يونيو',
    'July': 'يوليوز',
    'August': 'غشت',
    'September': 'شتنبر',
    'October': 'أكتوبر',
    'November': 'نونبر',
    'December': 'دجنبر'
}

# Dictionary mapping English day names to Arabic
english_to_arabic_days = {
    'Monday': 'الإثنين',
    'Tuesday': 'الثلاثاء',
    'Wednesday': 'الأربعاء',
    'Thursday': 'الخميس',
    'Friday': 'الجمعة',
    'Saturday': 'السبت',
    'Sunday': 'الأحد'
}

# Replace English day names with Arabic equivalents
data['month_name'] = data['month_name'].apply(lambda month: month.replace(month, english_to_arabic_months.get(month)))

# Replace English day names with Arabic equivalents
data['day_name'] = data['day_name'].apply(lambda day: day.replace(day, english_to_arabic_days.get(day)))

# Apply the spacy_summarizer function to each content column entry to generate a summary
data['key_point'] = data['content'].apply(lambda text: key_point(text))   

# Drop the 'content' column from the DataFrame
data.drop(columns=['content'], inplace=True)

# Apply the remove_stop_punc function to each entry in the 'recap' column
data['key_point'] = data['key_point'].apply(lambda text: remove_stop_punc(text))

# Apply the remove_stop_punc function to each entry in the 'title' column
data['title'] = data['title'].apply(lambda text: remove_stop_punc(text))
    
# Remove extra white spaces
data['key_point'] = data['key_point'].apply(lambda text : " ".join(text.split()))
data['title'] = data['title'].apply(lambda text : " ".join(text.split()))

data_dict = {}

for column in data.columns:
    # Convert the column data to a list and store it in the dictionary
    data_dict[column] = data[column].tolist()
     
with open('hespress_analysis.json', 'w', encoding='utf-8') as f:
    # Serialize the dictionary to JSON format
    json.dump(data_dict, f, ensure_ascii=False)