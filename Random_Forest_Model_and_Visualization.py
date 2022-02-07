#### Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py
import plotly.express as px

#Read the collected/cleaned NBA and college data
draftdf=pd.read_csv('nba_draft_data_cleaned_new.csv')
college_df=pd.read_csv('College_Statistics_Cleaned.csv')

#Merge the datasets
final_df=college_df.merge(draftdf,'left')

#Filter out players who did not play at least a season's worth of NBA games
final_df=final_df[final_df['G']>=82]

#Plot distribtuion of WS
import chart_studio.plotly as py
import plotly.express as px
fig = px.histogram(final_df, x="WS",labels={'WS':'Win Shares','y':'count'})
fig.show()

#Drop NBA columns
drop_cols=['Pk','Tm','Yrs','G','MP',
          'PTS','TRB','AST',
          'FG%','3P%','FT%','MP.1','PTS.1',
          'TRB.1','AST.1','BPM','WS/48','VORP',
          'Link','Unnamed: 0',
          'Unnamed: 0.1','College_Season']
final_df=final_df.drop(drop_cols,axis=1)


#Drop columns excluded after feature selection: No importance
drop_cols = ['College', 'College_Games_Played','College_Field_Goals_Attempted_Per_Game',
            'College_FG%','College_2PT_Field_Goals_Made_Per_Game','College_2PT_Field_Goals_Attempted_Per_Game',
            'College_2PT_FG%','College_Free_Throws_Attempted_Per_Game',
            'College_FT%','Fouls_pergame','Team_strength_of_schedule']

final_df=final_df.drop(drop_cols,axis=1)

final_df = final_df.dropna(axis=0)

##Setting Player as the dataframe's index
final_df.set_index('Player')

#Split data into train and test by years
x_train = final_df[final_df['Draft_Year'].isin([2000,2001,2002,2003,2004,2005,2006,2007,2008,2009])]
x_test = final_df[final_df['Draft_Year'].isin([2015,2016,2017,2018,2019])]
x_train=x_train.set_index('Player')
x_test=x_test.set_index('Player')

#Create a x/y split for independent and dependent variables
y_train=x_train['WS']
y_test = x_test['WS']
x_train = x_train.drop(['Draft_Year','WS'],axis=1)
x_test =x_test.drop(['Draft_Year','WS'],axis=1)

### Defining a Random Forest model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import MinMaxScaler

#Initializing the Linear Regression model
rf = RandomForestRegressor()

#Fitting the training data
rf.fit(x_train,y_train)

#Predict on test data
y_pred = rf.predict(x_test)

# Reset_indexes
x_test=x_test.reset_index()
x_train=x_train.reset_index()

#Create a Results dataframe for analysis
Results=pd.DataFrame()
Results['Player']=x_test['Player']
Results['WS_Pred']=y_pred
Results.set_index('Player')

#Bring back full dataset
Results=Results.merge(final_df,how='left')
Results=Results.merge(draftdf,'left')


###Creating a visualization for the regression model
fig= go.Figure([
    go.Scatter(x=Results['Player'], y = Results['WS'], name='Win Shares',mode='markers'),
    go.Scatter(x=Results['Player'], y=Results['WS_Pred'], name='Predicted Win Shares')
])
fig.show()

#Slicing Results
Result_slice=Results[['Pk','Player','WS','WS_Pred','Draft_Year']].sort_values('WS_Pred',ascending=False)

#Performing steps to filter the data by years for further analysis
Result_slice['Deviation']=Result_slice['WS']-Result_slice['WS_Pred']
Result_slice.WS_Pred=Result_slice.WS_Pred.round(decimals=2)

#Filtering continued
Result_2015=Result_slice[Result_slice.Draft_Year == 2015.0]
Result_2016=Result_slice[Result_slice.Draft_Year == 2016.0]
Result_2017=Result_slice[Result_slice.Draft_Year == 2017.0]
Result_2018=Result_slice[Result_slice.Draft_Year == 2018.0]
Result_2019=Result_slice[Result_slice.Draft_Year == 2019.0]

Result_2015['Original_Draft_Pick']=Result_2015['Pk']
Result_2016['Original_Draft_Pick']=Result_2016['Pk']
Result_2017['Original_Draft_Pick']=Result_2017['Pk']
Result_2018['Original_Draft_Pick']=Result_2018['Pk']
Result_2019['Original_Draft_Pick']=Result_2019['Pk']

Result_2015['Rank_of_WS_Prediction'] = Result_2015['WS_Pred'].rank(method='dense', ascending=False).astype(int)
Result_2016['Rank_of_WS_Prediction'] = Result_2016['WS_Pred'].rank(method='dense', ascending=False).astype(int)
Result_2017['Rank_of_WS_Prediction'] = Result_2017['WS_Pred'].rank(method='dense', ascending=False).astype(int)
Result_2018['Rank_of_WS_Prediction'] = Result_2018['WS_Pred'].rank(method='dense', ascending=False).astype(int)
Result_2019['Rank_of_WS_Prediction'] = Result_2019['WS_Pred'].rank(method='dense', ascending=False).astype(int)

Result_2015['Rank_of_Current_WS'] = Result_2015['WS'].rank(method='dense', ascending=False).astype(int)
Result_2016['Rank_of_Current_WS'] = Result_2016['WS'].rank(method='dense', ascending=False).astype(int)
Result_2017['Rank_of_Current_WS'] = Result_2017['WS'].rank(method='dense', ascending=False).astype(int)
Result_2018['Rank_of_Current_WS'] = Result_2018['WS'].rank(method='dense', ascending=False).astype(int)
Result_2019['Rank_of_Current_WS'] = Result_2019['WS'].rank(method='dense', ascending=False).astype(int)

Result_2015['Current_WS']=Result_2015['WS']
Result_2016['Current_WS']=Result_2016['WS']
Result_2017['Current_WS']=Result_2017['WS']
Result_2018['Current_WS']=Result_2018['WS']
Result_2019['Current_WS']=Result_2019['WS']

###Visualizations code for top 15 WS_Pred: Change Year of df name for year wanted to view.
Result_2015['Rank'] = Result_2015['WS_Pred'].rank(method='dense', ascending=False).astype(int)
colorscale = [[0, '#800000'],[.5, '#ffffff'],[1, '#ffffff']]
fig = ff.create_table(Result_2015[['Rank','Player','Original_Draft_Pick','WS_Pred','Rank_of_Current_WS']].sort_values('WS_Pred',ascending=False).head(15),colorscale)
for i in range(len(fig.layout.annotations)):
    fig.layout.annotations[i].font.size = 13
fig.show()

###Visualizations code for top 15 WS: Change Year of df name for year wanted to view.
Result_2015['Rank'] = Result_2015['WS'].rank(method='dense', ascending=False).astype(int)
colorscale = [[0, '#800000'],[.5, '#fffffe'],[1, '#ffffff']]
fig = ff.create_table(Result_2015[['Rank','Player','Original_Draft_Pick','Current_WS','Rank_of_WS_Prediction']].sort_values('Current_WS',ascending=False).head(15),colorscale)
for i in range(len(fig.layout.annotations)):
    fig.layout.annotations[i].font.size = 13
fig.show()
