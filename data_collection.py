import os
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
print(spotify_charts.head(5))
spotify_charts.info()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))

# find audio features for first 3 songs
for i in range(3):
    name = spotify_charts.iloc[i]['title']
    year = spotify_charts.iloc[i]['date'][:4]
    artists = spotify_charts.iloc[i]['artist']

    # returns dictionary, with many keys having other dictionaries as values
    results = sp.search(q= 'track: {} artist: {}'.format(name, artists), limit=1)
    uri = results['tracks']['items'][0]['uri']

    # returns list of dictionaries, get the first one
    audio_features = sp.audio_features(uri)[0]

    # add audio features as columns to song's row
    for key, value in audio_features.items():
        spotify_charts.iloc[i][key] = value

spotify_charts.to_csv("./src/sagemaker/data/charts_with_audio_features.csv")