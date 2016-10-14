
# coding: utf-8

# # Cancer Health Data Analytics
# Done in concurrent with, Kaggle Analytics

# In[52]:

import pandas as pd
path = r'C:\Users\ADEKUNLE\Desktop\Web Scrape'
health_data = pd.read_csv(path + r'\fullData.csv', encoding = 'ISO-8859-1', header = 0,                           index_col = 0)

#Check if there exist any null value
health_data.isnull().values.any()


# The dataframe appears to be okay(that will be after you have filled the various aspect that you need to), what to do next will be to select features that will be useful to intuit some great stuffs, probably popEst2015, MedIncome, deathRate, IncidenceRate, avgDeathsPerYear, County(you may need to split to get the State) and Name
# 
# Questions to Answer
# * Reviewing StudyCount effect on incidence rate

# In[66]:

new_HealthDF = health_data.ix[:, ['studyCount','PovertyEst', 'medIncome', 'popEst2015', 'incidenceRate', 'recentTrend']]

print(new_HealthDF.head())
print('-------------------')
new_HealthDF.info()


# The Data contains some funny values in the 'recentTrend' column, so replacing them using the replace() function in pandas that work well on pandas series, and the kind of filling is 'pad'.

# In[117]:

#Replace unclean values in the 'recentTrend' Column
print(new_HealthDF['recentTrend'].unique())

#new_HealthDF['recentTrend'].replace(['*', '¶', '¶¶'], method = 'pad', inplace= True)


# In[118]:

get_ipython().magic('matplotlib inline')

import matplotlib.pyplot as plt
import seaborn as sb

g = sb.pairplot(new_HealthDF)
g.set(xticklabels = []) #This help remove the x label value, and replace with only the column Title

#Add title to your plot 
g.fig.suptitle('PAIRPLOT VARIATIONS BETWEEN THE DATASET')
g.fig.subplots_adjust(top = 0.95) #This will help leave enough space for the title to stay on


# In[ ]:




# Good!, the Data does not have any null value, so we are good
# Also, its good to observe that what we are looking at is the data against 'Recent Trend' and 'rec Trend'

# In[31]:

health_data['recTrend'].unique()


# In[ ]:

#Check where the values of '*', and other symbol is in 'recentTrend' and replace them rightly
#Do same for 'recTrend'


# In[61]:

health_data['County'].unique()


# In[ ]:



