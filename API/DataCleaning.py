import pandas as pd
import re

#read CSV file
df_tweet = pd.read_csv(r"E:\BINAR\Binar-Gold-Challenge\Dataset\data.csv", encoding='latin1')

#filter and convert column 'Tweet' in df_tweet into data frame 
df = pd.DataFrame(df_tweet[['Tweet']])

#Fucntion to Clean tweet data
def Clean(text):
    #lowercase for every word
    text = text.lower()

    #Clean Pattern
    #remove USER
    text = re.sub(r'user', ' ', text)
    #remove 'RT'
    text = re.sub(r'rt', ' ', text)
    #remove 'URL'
    text = re.sub(r'url', ' ', text)
    #remove HTTPS
    text = re.sub(r'https', ' ', text)
    #remove HTTP
    text = re.sub(r'http', ' ', text)
    #remove &amp
    text = re.sub(r'&amp', ' ', text)

    #Clean_Unnecessary_Character
    #remove \n or every word afte '\' with space
    text = re.sub(r'\\n|\\[a-zA-Z0-9]+', ' ', text)
    #remove text emoji
    text = re.sub(r'[^a-zA-Z0-9\s]{2,}|:[a-zA-Z0-9]{0,}', ' ', text)
    #remove all unnecessary character 
    text = re.sub(r'[^0-9a-zA-Z\s]+', ' ', text)
    #remove extra space
    text = re.sub(r'  +', ' ', text)
    #remove space at the start or the end of string
    text = re.sub(r'^ +| +$', '', text)
    
    return text

#tokenization Function
def tokenization(text):
    text = re.split('\W+', text)
    return text

#kamus alay dictionary
kamus_alay = pd.read_csv(r"E:\BINAR\Binar-Gold-Challenge\Dataset\new_kamusalay.csv", encoding = 'ISO-8859-1', header = None)
kamus_alay = kamus_alay.rename(columns={0: 'kata alay', 1: 'arti kata'})
#Create dictionary using words list from kamus_alay
kamus_alay_dict = dict(zip(kamus_alay['kata alay'], kamus_alay['arti kata']))

#lemmatization function to convert every word tha contain 'kata alay' to 'arti kata'
def lemmatization(text):
    newlist = []
    for word in text:
        if word in kamus_alay_dict:
            text = kamus_alay_dict[word]
            newlist.append(text)
        else:
            text = word
            newlist.append(text)
    return newlist

#remove stopwords
#stopword list
f = open(r"E:\BINAR\Binar-Gold-Challenge\Dataset\tala-stopwords-indonesia.txt")
stopword_list = []
for line in f:
    stripped_line = line.strip()
    line_list = stripped_line.split()
    stopword_list.append(line_list[0])
f.close()

#remove stopword function
def remove_stopwords(text):
    text = [word for word in text if word not in stopword_list]
    return text

#function to run all the function
def clean_data(text):
    text = Clean(text)
    text = tokenization(text)
    text = lemmatization(text)
    text = remove_stopwords(text)

    return text

#convert list tweet to string
df['Tweet'] = df['Tweet'].apply(lambda x: ' '.join(map(str, clean_data(x))))

#Drop the duplicate from previous clean data
df.drop_duplicates(subset = 'Tweet', keep = 'first', inplace = True)
