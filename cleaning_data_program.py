import pandas as pd
import re

#read CSV file
df_tweet = pd.read_csv(r"E:\BINAR\Gold - Challenge\DATASET\data.csv", encoding='latin1')

#filter and convert column 'Tweet' in df_tweet into data frame 
df = pd.DataFrame(df_tweet[['Tweet']])

#Fucntion to Clean tweet data
def Clean(Tweet):
    #lowercase for every word
    Tweet = Tweet.lower()

    #Clean Pattern
    #remove USER
    Tweet = re.sub(r'user|user:', ' ', Tweet)
    #remove 'RT'
    Tweet = re.sub(r'^rt[\s]+| rt', ' ', Tweet)
    #remove 'URL'
    Tweet = re.sub(r'^url[\s]+| url', ' ', Tweet)
    #remove HTTPS
    Tweet = re.sub(r'https\S+|https', ' ', Tweet)
    #remove HTTP
    Tweet = re.sub(r'http\S+|http', ' ', Tweet)
    #remove &amp
    Tweet = re.sub(r'&amp', ' ', Tweet)

    #Clean_Unnecessary_Character
    #remove \n or every word afte '\' with space
    Tweet = re.sub(r'\\n|\\[a-zA-Z0-9]+', ' ', Tweet)
    #remove text emoji
    Tweet = re.sub(r'[^a-zA-Z0-9\s]{2,}|:[a-zA-Z0-9]{0,}', ' ', Tweet)
    #remove all unnecessary character 
    Tweet = re.sub(r'[^0-9a-zA-Z\s]+', ' ', Tweet)
    #remove extra space
    Tweet = re.sub(r'  +', ' ', Tweet)
    #remove space at the start or the end of string
    Tweet = re.sub(r'^ +| +$', '', Tweet)
    
    return Tweet

#Apply the funtion
df['clean_Tweet'] = df['Tweet'].apply(Clean)

#Drop the duplicate from previous clean data
df.drop_duplicates(subset = 'clean_Tweet', keep = 'first', inplace = True)

#Filter coulumn 'clean_Tweet'
Output = df[['clean_Tweet']]

#Export final clean data to CSV file
Output.to_csv('new_data.csv')