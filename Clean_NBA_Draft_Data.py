###Import packages
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import plotly.express as px

# Read collected draft data csv
draftdf=pd.read_csv('nba_draft_data.csv')

##Checking for null values
draftdf.isnull().sum()

#Taking the dataframe without any rows where 'Player' is NA
#Taking df where 'College' is not NA
#Removing the nulls from this column as I am interested in players who played for a College
#Remove empty 'G' as I want to analyze players who played in NBA as a baseline for performance
draftdf = draftdf[draftdf['Player'].notna()]
draftdf = draftdf[draftdf['College'].notna()]
draftdf = draftdf[draftdf['G'].notna()]

#Creating a histogram for number of NBA Games
fig = px.histogram(draftdf, x="G",labels={'G':'NBA_Games_Played','y':'count'})
fig.show()

# Export cleaned data to a csv file
draftdf.to_csv("nba_draft_data_cleaned.csv", index=False)
