import pandas as pd
import re

#read CSV file
df_tweet = pd.read_csv(r"E:\BINAR\Gold - Challenge\DATASET\data.csv", encoding='latin1')

#filter and convert column 'Tweet' in df_tweet into data frame 
df = pd.DataFrame(df_tweet[['Tweet']])

#Fucntion to Clean tweet data
def Clean(Tweet):
    #remove USER
    Tweet = re.sub(r'USER:|USER', '', Tweet)
    #Remove numbers 0-9 or any numbers with '.' as an end string
    Tweet = re.sub(r'[0-9]+[.]{1,}|[0-9]+', '', Tweet)
    #remove 'RT'
    Tweet = re.sub(r'^RT[\s]+| RT', '', Tweet)
    #remove 'URL'
    Tweet = re.sub(r'^URL[\s]+| URL', '', Tweet)
    #remove hashtags '#' sign
    Tweet = re.sub(r'#', '', Tweet)
    #remove any character or space in the start of string
    Tweet = re.sub(r'^[^a-zA-Z0-9]{0,}', '', Tweet)
    #remove \n or every word afte '\' with space
    Tweet = re.sub(r'\\n|\\[a-zA-Z0-9]+', ' ', Tweet)
    #remove text emoji
    Tweet = re.sub(r'[^a-zA-Z0-9\s]{2,}|:[a-zA-Z0-9]{0,}', '', Tweet)
    #remove (') & (")  at string
    Tweet = re.sub(r'\'{1,}|\"{1,}', '', Tweet)
    #remove &amp
    Tweet = re.sub(r'&amp', '', Tweet)
    
    return Tweet

#Apply the funtion
df['clean_Tweet'] = df['Tweet'].apply(lambda x: Clean(x))

#Drop the duplicate from previous clean data
df.drop_duplicates(subset = 'clean_Tweet', keep = 'first', inplace = True)

#Filter coulumn 'clean_Tweet'
Output = df[['clean_Tweet']]

#Export final clean data to CSV file
Output.to_csv('new_data_3.csv')