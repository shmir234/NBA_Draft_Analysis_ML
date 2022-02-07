# Importing necessary packages

import pandas as pd
import numpy as np

college_df=pd.read_csv('College_Statistics.csv')

#Checking for null values
college_df.isnull().sum()

#Performing data transformation/preparation steps
college_df['College_Season']=college_df['College_Season'].fillna(value='Career')

# Filling null values
college_df['College_3PT_FG%']=college_df['College_3PT_FG%'].fillna(value='0')
college_df['Turnovers_pergame']=college_df['Turnovers_pergame'].fillna(value='0')
college_df['Fouls_pergame']=college_df['Fouls_pergame'].fillna(value='0')
college_df['College_2PT_Field_Goals_Made_Per_Game']=college_df['College_2PT_Field_Goals_Made_Per_Game'].fillna(value='0')
college_df['College_2PT_Field_Goals_Attempted_Per_Game']=college_df['College_2PT_Field_Goals_Attempted_Per_Game'].fillna(value='0')
college_df['College_3PT_Field_Goals_Made_Per_Game']=college_df['College_3PT_Field_Goals_Made_Per_Game'].fillna(value='0')
college_df['College_3PT_Field_Goals_Attempted_Per_Game']=college_df['College_3PT_Field_Goals_Attempted_Per_Game'].fillna(value='0')
college_df['Team_strength_of_schedule']=college_df['Team_strength_of_schedule'].fillna(value=college_df['Team_strength_of_schedule'].mean())

college_df.isnull().sum()

##Finding historical value of Offensive rebounds and Defensive Rebounds to fill in
#For 95 players with missing values
college_df['Offensive_Rebound_Percentage'] = college_df['Offensive_Rebounds_pergame'] / college_df['Total_Rebounds_pergame'] * 100
college_df['Defensive_Rebound_Percentage'] = college_df['Defensive_Rebounds_pergame'] / college_df['Total_Rebounds_pergame'] * 100

##28.5% is ORB
##71.5% is DRB
college_df['Offensive_Rebounds_pergame']=college_df['Offensive_Rebounds_pergame'].fillna(value=college_df['Total_Rebounds_pergame']*.285)
college_df['Defensive_Rebounds_pergame']=college_df['Defensive_Rebounds_pergame'].fillna(value=college_df['Total_Rebounds_pergame']*.715)

college_df.to_csv('College_Statistics_Cleaned.csv')
