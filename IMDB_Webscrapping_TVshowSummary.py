# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 18:42:16 2021

@author: jessa
"""

# setting up environment
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# setting up macro variables
end = 8 # number of seasons of the show
show = 'tt0238784' # from IMBD the show ID

# creating empty dataframe
df = pd.DataFrame()

# setting up empty lists
sumofsum = []
sumofepisodenum = []

# make a for loop for URLS
for num in range(1, end):
    URL = 'https://www.imdb.com/title/' + show + '/episodes?season=' + str(num)
    # getting request for the URLs
    req = requests.get(URL)
    # parsing this
    soup = bs(req.text, 'html.parser')
    
    # getting all the pieces out
    plot_sum = soup.find_all('div', class_='item_description')
    # title_sum = soup.find_all('div', class_='item_description') # need to update class_
    episodenum_sum = soup.find_all('div', class_='zero-z-index') # need to update class_
    
    # for loop to place these in a list
    for i in range(0, len(plot_sum)):
        text_sum1 = plot_sum[i].text
        sumofsum.append(text_sum1)
    # for loop to place these in a list
    for i in range(0, len(episodenum_sum)):
        text_sum3 = episodenum_sum[i].text
        sumofepisodenum.append(text_sum3)
        
# creating dataframe
df['Episode_Numbers'] = sumofepisodenum

# splitting episode info out
df = pd.DataFrame(df.Episode_Numbers.str.split(',',1).tolist(), columns = ['Season','Episode'])

# adding in summaries
df['Episode_Numbers'] = sumofepisodenum
df['Summaries'] = sumofsum

# removing first episode (unaired pilot)
df = df.iloc[1:]

# stripping text off season & episode number
df['Season'] = df['Season'].str.replace('S', '')
df['Season'] = df['Season'].str.replace('\n', '')
df['Episode'] = df['Episode'].str.replace('Ep', '')
df['Episode'] = df['Episode'].str.replace('\n', '')

# writing out my pretty dataset
df.to_excel('C:\\Users\\jessa\\OneDrive\\Documents\\Projects\\GilmoreGirls\\data.xlsx', index = False)
