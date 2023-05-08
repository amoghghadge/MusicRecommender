import os
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify_data = pd.read_csv('./src/sagemaker/data/tracks_features.csv')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))

#for i in range(3):
#name = spotify_data.iloc[i]['name']
#year = spotify_data.iloc[i]['year']

name = "if looks could kill"
year = 2023
    
results = sp.search(q= 'track: {} year: {}'.format(name, year), limit=1)
print(results)
results = results['tracks']['items'][0]
    
track_id = results['id']
audio_features = sp.audio_features(track_id)[0]
print()
print("AUDIO FEATURES OF: " + name)

print()

for key, value in audio_features.items():
    print(str(key) + " " + str(value))