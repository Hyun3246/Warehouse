import tweepy, json, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

twitter_access_token = <my_twitter_access_token>
twitter_access_token_secret = <my_twitter_access_token_secret>
twitter_consumer_key = <my_consumer_key>
twitter_consumer_secret = <my_twitter_consumer_secret>

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# 뉴스 소스 선정
news_sources = ('@BBC', '@ctvnews', '@CNN', '@FoxNews', '@dawn_com')

# 메인 루프
print("...STARTING... collecting tweets from sources")

array_sentiments = []

for user in news_sources:
    count_tweet= 100    # 트윗을 100개씩 수집
    print("Start tweets from %s %user")
    for x in range(5):  # 5개 페이지 분량의 트윗을 추출
        public_tweets = api.user_timeline(user, page=x)
        for tweet in public_tweets:
            # 트윗의 감성 점수와 긍정/부정/중립 확률 계산
            compound = analyzer.polarity_scores(tweet["text"])['compound']
            pos = analyzer.polarity_scores(tweet["text"])["pos"]
            neu = analyzer.polarity_scores(tweet['text'])['neu']
            neg = analyzer.polarity_scores(tweet["text"])["neg"]

            array_sentiments.append(
                {"Media": user,
                "Tweet Text": tweet["text"],
                'Compound': compound,
                "Positive": pos,
                'Negative': neg,
                "Neutral": neu,
                'Date': tweet["created_at"],
                "Tweets Ago": count_tweet})
            
            count_tweet -=1

print("Done with extracting tweets")

# 데이터 프레임으로 변환
sentiments_df=pd.DataFrame.from_dict(array_sentiments)
sentiments_df['Media'] = sentiments_df['Media'].map(lambda x: x.lstrip('@'))
sentiments_df=sentiments_df[["Media","Date","Tweet Text","Compound","Positive","Negative","Neutral","Tweets Ago"]]
sentiments_df.to_csv("mySentimentAnalysis.csv")

sentiments_df.head(10)

source=sentiments_df["Media"].unique()


# 감성을 시각화 하는 플롯
for media in source:
    mydf = sentiments_df[sentiments_df["Media"] == media]
    plt.scatter(mydf["Tweets Ago"], mydf["Compound"], marker="o", linewidth=0, alpha=0.8, label=media, facecolors=mydf.Media.map(
        {"BBC": "pink",
        "ctvnews": "purple",
        "CNN": 'red',
        "FoxNews": 'blue',
        "dawn_com": "green"
        }))

plt.legend(bbox_to_anchor = (1, 1), title = "Media Sources")
plt.title("Sentiment Analysis of Media Tweets (%s)" %(time.strftime("%x")), fontsize=14)
plt.xlabel("Tweets Ago")
plt.ylabel("Tweet Polarity")
plt.xlim(101, 0)
plt.ylim(-1, 1)
plt.grid(True)
plt.savefig("Output/Sentiment Analysis of Media Tweets.png", bbox_inches = "tight")
plt.show()

# 감성 점수를 데이터프레임에 저장
means_media_trends = sentiments_df.groupby("Media").mean()['Compound'].to_frame()

# 인덱스 초기화
means_media_trends.reset_index(inplace=True)

print(means_media_trends)
