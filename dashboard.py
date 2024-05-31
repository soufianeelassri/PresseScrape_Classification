# Import necessary libraries
import streamlit as st
import json
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title='Hespress', page_icon=':bar_chart', layout='wide')

# Set title
st.title(':bar_chart: Hespress EDA')

# Apply custom styling
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Open JSON file and load data into a dictionary
with open('hespress_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Split keywords into individual keywords and count their occurrences
keywords_split = df['key_words'].str.split(',').explode()
keyword_counts = keywords_split.groupby(keywords_split).count().reset_index(name='count')

# Exclude the first row (index)
keyword_counts = keyword_counts.iloc[1:]

# Select top 10 keywords based on frequency
top_10_keywords = keyword_counts.sort_values(by='count', ascending=False).iloc[:10]

# Extract keyword names
keyword_names = [keyword for keyword in top_10_keywords['key_words']]

# Create bar plot for top 10 keywords
fig_keywords = px.bar(
    x=top_10_keywords['count'][::-1],  # Reverse order to display highest count on top
    y=keyword_names[::-1],
    orientation='h',
    title='Top 10 Keywords',
    labels={'x': 'Frequency', 'y': 'Keyword'},
    template='seaborn'
)

# Adjust layout margins
fig_keywords.update_layout(margin=dict(t=50, b=50, l=150, r=50))

# Count the number of articles for each source
source_counts = df.groupby('source')['title'].count().reset_index(name='count')

# Select top 10 sources based on article count
top_10_source_counts = source_counts.sort_values(by='count', ascending=False).iloc[:10]

# Extract source names
source_names = [source for source in top_10_source_counts['source']]

# Create bar plot for top 10 sources
fig_sources = px.bar(
    x=top_10_source_counts['count'][::-1], 
    y=source_names[::-1], 
    orientation='h',
    title='Top 10 Publishers',
    labels={'x': 'Number of Articles', 'y': 'Publisher Name'},
    template='seaborn'
)

fig_sources.update_layout(margin=dict(t=50, b=50, l=150, r=50))

    
# Create two columns layout
col1, col2 = st.columns(2)

# Display the bar plot for top 10 keywords in the first column
with col1:
    st.plotly_chart(fig_keywords, use_container_width=True)

# Display the bar plot for top 10 sources in the second column
with col2:
    st.plotly_chart(fig_sources, use_container_width=True)
    
# Count the number of articles for each category
category_counts = df.groupby('category')['title'].count().reset_index(name='count')

# Create pie chart for category distribution
fig_pie = px.pie(
    values=category_counts['count'],
    names=category_counts['category'],
    title='Category Distribution',
    template='seaborn'
)

# Create a single column layout for the pie chart
col3 = st.columns(1)[0]

# Display the pie chart
with col3:
    st.plotly_chart(fig_pie, use_container_width=True)

# Count the number of articles for each month
monthly_counts = df.groupby(['year', 'month', 'month_name']).size()
monthly_counts = monthly_counts.reset_index()

# Create line plot for monthly timeline
fig_month = px.line(
    x=monthly_counts['month_name'],
    y=monthly_counts[0],
    title='Monthly Timeline',
    labels={'x': 'Month', 'y': 'Number of Articles'},
    markers=True,
    template='seaborn'
)

# Define Arabic names of days of the week
days_in_arabic = ['الإثنين' , 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']

# Convert 'day_name' column to categorical with Arabic names of days
df['day_name'] = pd.Categorical(df['day_name'], categories=days_in_arabic, ordered=True)

# Count the number of articles for each day
daily_counts = df.groupby(df['day_name']).size()

# Create line plot for daily timeline
fig_day = px.line(
    x=daily_counts.index,
    y=daily_counts.values,
    title='Daily Timeline',
    labels={'x': 'Day', 'y': 'Number of Articles'},
    markers=True,
    template='seaborn'
)
   
# Create two columns layout
col4, col5 = st.columns(2)

# Display the line plot for monthly timeline
with col4:
    st.plotly_chart(fig_month, use_container_width=True)

# Display the line plot for daily timeline
with col5:
    st.plotly_chart(fig_day, use_container_width=True)
  
# Define labels for different periods of the day
labels = ['الصباح', 'الظهيرة', 'المساء', 'الليل']

# Group articles by hour and categorize them into periods of the day
hourly_counts = df.groupby(pd.cut(df['hour'],
                                  bins=[0, 6, 12, 18, 24],
                                  labels=labels
                                 )).size()  

# Create bar plot for hourly timeline
fig_hour = px.bar(
    x=hourly_counts.index,
    y=hourly_counts.values,
    title='Hourly Timeline',
    labels={'x': 'Period', 'y': 'Number of Articles'},
    template='seaborn'
)
  
# Create a single column layout for the hourly timeline
col6 = st.columns(1)[0]

# Display the bar plot for hourly timeline
with col6:
    st.plotly_chart(fig_hour, use_container_width=True)
