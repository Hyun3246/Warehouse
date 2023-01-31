import pandas as pd
import numpy as np

df_reviews = pd.read_csv("reviews.csv")
df_movie_titles = pd.read_csv("movies.csv", index_col=False)

df = pd.merge(df_reviews, df_movie_titles, on='movieId')

df_ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
df_ratings['number_of_ratings'] = df.groupby('title')['rating'].count()
print(df_ratings.head())

movie_matrix = df.pivot_table(index='userId', columns='title', values='rating')

# 영화 추천
Avatar_user_rating = movie_matrix['Avatar (2009)']
Avatar_user_rating =Avatar_user_rating.dropna()
Avatar_user_rating.head()

similar_to_Avatar = movie_matrix.corrwith(Avatar_user_rating)
corr_Avatar = pd.DataFrame(similar_to_Avatar, columns=['correlation'])
corr_Avatar.dropna(inplace=True)
corr_Avatar = corr_Avatar.join(df_ratings['number_of_ratings'])
print(corr_Avatar.head())