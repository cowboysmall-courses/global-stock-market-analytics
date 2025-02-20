
"""

Global market indices of interest:

    NSEI:  Nifty 50
    DJI:   Dow Jones Index
    IXIC:  Nasdaq
    HSI:   Hang Seng
    N225:  Nikkei 225
    GDAXI: Dax
    VIX:   Volatility Index

"""



# %% 1 - import required libraries
import pandas as pd

import nltk

from string import punctuation, digits

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from wordcloud import WordCloud

from cowboysmall.plots import plt, sns



# %% 1 -
plt.plot_setup()
sns.sns_setup()



# %% 1 - import data and check the head
with open("./data/tweets/Tweets 12-6-24.txt") as file:
    tweets = [line.rstrip() for line in file]



# %% 1 - 
data = pd.DataFrame([line for line in tweets if len(line) > 0], columns= ["Tweets"])
data.head()
#                                               Tweets
# 0  #bankNifty 50100 ce looks good at 70+-2 for a ...
# 1  "#market #banknifty #OptionsTrading #optionbuy...
# 2  PENNY STOCK MADHUCON PROJECTS LTD cmp-11 FOLLO...
# 3  #Nifty50 has been in a healthy uptrend since t...
# 4  #Gravita #livetrading #stockstowatch #stocksin...



# %% 1 - 
stop_words    = set(stopwords.words('english')) | set(["nifty", "banknifty", "niftybank", "stockmarketindia", "stockmarket"])
remove_punc   = str.maketrans('', '', punctuation)
remove_digits = str.maketrans('', '', digits)

def preprocess_tweet(tweet):
    tokens = word_tokenize(tweet.lower().translate(remove_punc).translate(remove_digits))
    return " ".join([word for word in tokens if word not in stop_words])



# %% 1 - 
data["Cleaned_Tweets"] = data["Tweets"].apply(preprocess_tweet)
data.head()
#                                               Tweets  \
# 0  #bankNifty 50100 ce looks good at 70+-2 for a ...   
# 1  "#market #banknifty #OptionsTrading #optionbuy...   
# 2  PENNY STOCK MADHUCON PROJECTS LTD cmp-11 FOLLO...   
# 3  #Nifty50 has been in a healthy uptrend since t...   
# 4  #Gravita #livetrading #stockstowatch #stocksin...   

#                                       Cleaned_Tweets  
# 0                               ce looks good target  
# 1  market optionstrading optionbuying trading buy...  
# 2  penny stock madhucon projects ltd cmp followht...  
# 3  healthy uptrend since beginning year didnt bre...  
# 4  gravita livetrading stockstowatch stocksinfocu...  



# %% 1 - 
tweet_words = data["Cleaned_Tweets"].str.cat(sep = " ")



# %% 1 - 
freq_dist    = nltk.FreqDist(tweet_words.split())
freq_dist_df = pd.DataFrame(freq_dist.most_common(30), columns=["Words", "Frequency"])
freq_dist_df.head(30)
#               Words  Frequency
# 0            sensex         43
# 1            stocks         38
# 2    optionstrading         36
# 3               bse         34
# 4    breakoutstocks         31
# 5           trading         30
# 6            market         29
# 7             india         26
# 8               ipm         25
# 9              good         24
# 10              nse         24
# 11           growth         24
# 12         nseindia         23
# 13              may         23
# 14  pharmaceuticals         23
# 15     indianpharma         23
# 16      stockstobuy         22
# 17      sharemarket         21
# 18     stockmarkets         20
# 19              amp         19
# 20           points         19
# 21    stocksinfocus         19
# 22             time         19
# 23             bank         18
# 24            today         18
# 25    stockstowatch         18
# 26            index         17
# 27     optionbuying         16
# 28              buy         16
# 29         finnifty         16



# %% 1 - 
plt.barh_plot(freq_dist_df["Words"], freq_dist_df["Frequency"], "Frequency", "Words", "Words by Frequency")



# %% 1 - 
wordcloud = WordCloud(background_color = "white", collocations = False).generate(tweet_words)



# %% 1 - 
plt.image_plot(wordcloud)



# %% 1 - 
sia = SentimentIntensityAnalyzer()

data["Sentiment_Scores"] = data["Cleaned_Tweets"].apply(lambda x: sia.polarity_scores(x))



# %% 1 - 
data["Positive_Score"] = data["Sentiment_Scores"].apply(lambda x:  x["pos"])
data["Negative_Score"] = data["Sentiment_Scores"].apply(lambda x: -x["neg"])
data["Neutral_Score"]  = data["Sentiment_Scores"].apply(lambda x:  x["neu"])
data["Compound_Score"] = data["Sentiment_Scores"].apply(lambda x:  x["compound"])



# %% 1 - 
scores = data[["Positive_Score", "Negative_Score", "Neutral_Score", "Compound_Score"]]
scores.head()
#    Positive_Score  Negative_Score  Neutral_Score  Compound_Score
# 0           0.492          -0.000          0.508          0.4404
# 1           0.077          -0.149          0.774         -0.3400
# 2           0.155          -0.000          0.845          0.2960
# 3           0.100          -0.198          0.702         -0.3935
# 4           0.262          -0.000          0.738          0.5994



# %% 1 - 
scores.describe()
#        Positive_Score  Negative_Score  Neutral_Score  Compound_Score
# count      245.000000      245.000000     245.000000      245.000000
# mean         0.121494       -0.029559       0.848963        0.172913
# std          0.154320        0.073763       0.165248        0.343955
# min          0.000000       -0.405000       0.213000       -0.807400
# 25%          0.000000        0.000000       0.734000        0.000000
# 50%          0.055000        0.000000       0.868000        0.000000
# 75%          0.208000        0.000000       1.000000        0.440400
# max          0.787000       -0.000000       1.000000        0.928700



# %% 1 - 
sns.box_plot_values(scores, "Type", "Score", "Scores")
