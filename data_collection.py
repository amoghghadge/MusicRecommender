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
df = pd.DataFrame(columns=['name', 'year', 'artists', 'track_uri', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                           'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'])

print("running on " + str(len(spotify_charts.index)) + " songs!")
print("\ngood luck!\n")

# find audio features for all songs on spotify charts
for i in range(50):
    print(str(i) + " song\n")
    name = spotify_charts.iloc[i]['title']
    year = spotify_charts.iloc[i]['date'][:4]
    artists = spotify_charts.iloc[i]['artist']

    # returns dictionary, with many keys having other dictionaries as values
    try:
        results = sp.search(q= 'track: {} artist: {}'.format(name, artists), limit=1)
    except:
        print("Song taken down\n")
        continue
    uri = results['tracks']['items'][0]['uri']

    # returns list of dictionaries, get the first one
    audio_features = sp.audio_features(uri)[0]

    # see audio features of track
    # print("\nAUDIO FEATURES OF: " + name)
    # print()
    # for key, value in audio_features.items():
    #     print(str(key) + " " + str(value))

    # add audio features as columns to song's row
    relevant_features = [audio_features[col] for col in df.columns if col not in ['name', 'year', 'artists', 'track_uri']]
    row = [name, year, artists, uri, *relevant_features]
    df.loc[len(df.index)] = row

df.to_csv("./src/sagemaker/data/charts_with_audio_features.csv", encoding='utf-8', index=False)