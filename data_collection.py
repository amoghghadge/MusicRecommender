import os
import time
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# remove duplicates in charts data (done only once)
# spotify_charts = pd.read_csv('./src/sagemaker/data/charts.csv')
# print(spotify_charts.head(10))
# spotify_charts.info()
# spotify_charts = spotify_charts.drop_duplicates(subset="title")
# spotify_charts.to_csv('./src/sagemaker/data/charts_no_duplicates.csv', encoding='utf-8', index=False)

spotify_charts = pd.read_csv("./src/sagemaker/data/charts_no_duplicates.csv")

only_us = spotify_charts[spotify_charts['region'].isin(["United States", "Global", "United Kingdom", "Canada", "New Zealand", "Australia", "Ireland"])]
only_us = only_us[spotify_charts["chart"] == "top200"]
only_us = only_us.reset_index(drop=True)

print(only_us.head(10))
only_us.info()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))
df = pd.DataFrame(columns=['name', 'date', 'artists', 'url', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                           'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'])

print("\nrunning on " + str(len(only_us.index)) + " songs!")
print("good luck!\n")

# find audio features for all songs on spotify charts
for i in range(0, len(only_us.index), 100):
    print(str(i) + " song\n")
    time.sleep(0.1)
    name = only_us.iloc[i:i+100]['title']
    date = only_us.iloc[i:i+100]['date']
    artists = only_us.iloc[i:i+100]['artist']
    url = only_us.iloc[i:i+100]['url']

    # returns list off dictionaries for 100 songs
    audio_features = sp.audio_features(url)

    # make new row enteries for audio features of each song
    for j in range(i, min(i+100, len(only_us.index))):
        try:
            track_features = audio_features[j-i]
            relevant_features = [track_features[col] for col in df.columns if col not in ['name', 'date', 'artists', 'url']]
            row = [name[j], date[j], artists[j], url[j], *relevant_features]
            df.loc[len(df.index)] = row
        except:
            print("Error for song")

df.to_csv("./src/sagemaker/data/us_charts_with_audio_features.csv", encoding='utf-8', index=False)