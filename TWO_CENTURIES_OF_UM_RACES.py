#!/usr/bin/env python
# coding: utf-8

# In[105]:


#Dataset: https://www.kaggle.com/datasets/aiaiaidavid/the-big-dataset-of-ultra-marathon-running/discussion/420633


# In[106]:


#Import Libararies


# In[107]:


import pandas as pd


# In[108]:


import seaborn as sns


# In[109]:


df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")


# In[6]:


#see the data that's been imported 


# In[110]:


print(df)


# In[111]:


df.head(10)


# In[119]:


df.shape


# In[120]:


df.dtypes


# In[121]:


#clean up data


# In[122]:


#only want USA Races, 50K or 50mi, 2020


# In[123]:


#step 1 show 50Mi or 50k                         
#50km


# In[124]:


df[df['Event distance/length'] == '50km']


# In[126]:


#50mi 
df[df['Event distance/length'] == '50mi']


# In[128]:


#combine 50k/50mi with isin  
df[df['Event distance/length'].isin(['50km','50mi'])]


# In[130]:


#showing year of 2020 
df[(df['Event distance/length'].isin(['50km','50mi'])) & (df ['Year of event'] == 2020)]


# In[131]:


#how to get the USA 
df[df['Event name'] == 'Everglades 50 km Ultra Run (USA)']['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)


# In[132]:


#sPLIT USA FROM table                   
df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA']


# In[20]:


#COMBINE ALL FILTERS TOGETHER


# In[133]:


df[(df['Event distance/length'].isin(['50km','50mi'])) & (df ['Year of event'] == 2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]


# In[134]:


df2 = df[(df['Event distance/length'].isin(['50km','50mi'])) & (df ['Year of event'] == 2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]


# In[135]:


df2.head(10)


# In[136]:


df2.shape


# In[137]:


#Remove (USA) from event name 
df2['Event name'].str.split('(').str.get(0)


# In[138]:


df['Event name']


# In[139]:


df['Event name'].str.split('(')


# In[140]:


df['Event name'].str.split('(').str.get(1)


# In[141]:


df['Event name'].str.split('(').str.get(1).str.split(')')


# In[142]:


df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)


# In[143]:


df2['Event name'] = df2['Event name'].str.split('(').str.get(0)


# In[144]:


df2.head()


# In[145]:


#clean up athlete age 
df2['athlete_age'] = 2020 - df2['Athlete year of birth']


# In[146]:


#remove h from athlete performance 
df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)


# In[147]:


df2.head(5)


# In[148]:


#drop columns :Athlete club, athlete country, athlete year of birth, athlete age category


# In[149]:


df2 = df2.drop(['Athlete club', 'Athlete country', 'Athlete year of birth', 'Athlete age category'],  axis =1)


# In[150]:


df2.head()


# In[151]:


#clean up null values 
df2.isna().sum()


# In[152]:


df2.shape


# In[153]:


#check for duplicate values 
df2[df2.duplicated() == True]


# In[154]:


#reset index 

df2.reset_index(drop)


# In[155]:


#fix types 
df2.dtypes


# In[156]:


df2['Athlete average speed'] = df2['Athlete average speed'].astype(float)


# In[157]:


df2.dtypes


# In[158]:


df2.head()


# #rename columns name 
# Year of event                  int64
# Event dates                   object
# Event name                    object
# Event distance/length         object
# Event number of finishers      int64
# Athlete performance           object
# Athlete gender                object
# Athlete average speed        float64
# Athlete ID                     int64

# In[162]:


df2 = df2.rename(columns = {'Year of event': 'year', 
                        'Event dates' : 'race_day',
                        'Event name' : 'race_name',
                        'Event distance/length' : 'race_length',
                        'Event number of finishers' : 'race_number_of_finishers',
                        'Athlete performance' : 'athlete_performance',
                        'Athlete gender' : 'athletegender',
                        'Athlete average speed' : 'athlete_average_speed',
                        'Athlete ID' : 'athlete_id',
                        'athlete_age' : 'athleteage'
                        })


# In[164]:


df2.head()


# In[168]:


#reorder columns 
df3 = df2[['race_day', 'race_name', 'race_length', 'race_number_of_finishers', 'athlete_id', 'athletegender','year','athlete_performance','athlete_average_speed', 'athleteage']]


# In[169]:


df3.head()


# In[170]:


df3[df3['race_name'] == 'Everglades 50 km Ultra Run ']


# In[171]:


#222509 
df3[df3['athlete_id'] == 222509]


# In[172]:


sns.histplot(df3['race_length'])


# In[173]:


sns.histplot(df3, x = 'race_length', hue = 'athletegender')


# In[174]:


sns.displot(df3[df3['race_length'] == '50mi'] ['athlete_average_speed'])


# In[175]:


sns.violinplot(data=df3, x='race_length', y='athlete_average_speed', hue='athletegender', split=True, inner='quartile')


# In[177]:


import seaborn as sns
sns.lmplot(data=df2, x='athleteage', y='athlete_average_speed', hue='athletegender')


# In[80]:


#questions I want to find out from the data 
#race_day
#race_name
#race_length 
#race_number_of_finishers 
#athelete_id 
#athlete_geneder 
#athlete_age 
#athlete_performance 
#athlete_averange_speed


# In[ ]:


#diffrence in speed for the 50k, 50mi male and female


# In[178]:


df3.groupby(['race_length', 'athletegender'])['athlete_average_speed'].mean()


# In[182]:


#what age groups are the best in the 50m Race (20 + races min)
df3.query('race_length == "50mi"').groupby('athleteage')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False).query('count > 19')


# In[183]:


#what age groups are the worst in the 50m Race (20 + races min) (Show 20) 
df3.query('race_length == "50mi"').groupby('athleteage')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = True).query('count > 9')


# In[ ]:


#Seasons for the data --> slower in summer than winter? 
#sprin 3-5
#summer 6-8
#fall 9-11
#winter 12-2 

#split between two decimals


# In[184]:


df3['race_month'] = df3['race_day'].str.split('.').str.get(1).astype(int)


# In[186]:


df3.head(25)


# In[188]:


df3['race_season'] = df3['race_month'].apply(
    lambda x: 'Winter' if x > 11 or x <= 2 else
              'Fall' if x > 8 else
              'Summer' if x > 5 else
              'Spring' if x > 2 else 'Unknown'  # The 'Unknown' is just a safeguard; it should never be reached with valid month values.
)


# In[189]:


df3.head(25)


# In[191]:


df3.groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[192]:


df3.query('race_length == "50mi"').groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[ ]:




