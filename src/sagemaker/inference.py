import argparse
import sys

import os
from urllib import request
module_path = os.path.abspath('/opt/ml/code')
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import pandas as pd
import boto3
import spotipy
import joblib
import json
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
from collections import defaultdict
from scipy.spatial.distance import cdist

s3 = boto3.client('s3') 
obj = s3.get_object(Bucket= "aghadge-song-data", Key= "data.csv") 

spotify_data = pd.read_csv(obj['Body'])
X = spotify_data.select_dtypes(np.number)
number_cols = list(X.columns)

# Recommendation System
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))

def find_song(name, year):
  
    """
    This function returns a dataframe with data for a song given the name and release year.
    The function uses Spotipy to fetch audio features and metadata for the specified song.
    """
    
    song_data = defaultdict()
    results = sp.search(q= 'track: {} year: {}'.format(name,year), limit=1)
    if results['tracks']['items'] == []:
        return None
    
    results = results['tracks']['items'][0]

    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]
    
    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]
    
    for key, value in audio_features.items():
        song_data[key] = value
    
    return pd.DataFrame(song_data)

number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

def get_song_data(song, spotify_data):
    
    """
    Gets the song data for a specific song. The song argument takes the form of a dictionary with 
    key-value pairs for the name and release year of the song.
    """
    
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name']) & (spotify_data['year'] == int(song['year']))].iloc[0]
        return song_data
    
    except IndexError:
        return find_song(song['name'], song['year'])

def get_mean_vector(song_list, spotify_data):
  
    """
    Gets the mean vector for a list of songs.
    """
    
    song_vectors = []
    
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)  
    
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)

def flatten_dict_list(dict_list):
   
    """
    Utility function for flattening a list of dictionaries.
    """
    
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def recommend_songs(song_list, spotify_data, cluster_pipeline, n_songs=10):
  
    """
    Recommends songs based on a list of previous songs that a user has listened to.
    """
    
    metadata_cols = ['name', 'year', 'artists']
    song_dict = flatten_dict_list(song_list)
    
    song_center = get_mean_vector(song_list, spotify_data)
    scaler = cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return rec_songs[metadata_cols].to_dict(orient='records')

# Methods for SageMaker
def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def input_fn(request_body, request_body_content_type):
    if request_body_content_type == 'application/json':
        request_body=json.loads(request_body)
        inpVar = {'Songs': request_body['Songs'], 'Number': request_body['Number']}
        return inpVar
    else: 
        raise ValueError("This model only supports application/json input")

def predict_fn(input_data, model):
    song_list = input_data.get('Songs')
    n_songs = input_data.get('Number')
    cluster_labels = model.predict(X)
    spotify_data['cluster_label'] = cluster_labels
    resp = recommend_songs(song_list, spotify_data, model, n_songs)
    return resp

def output_fn(prediction, content_type):
    respJSON = {'Songs': prediction}
    return respJSON

"""

with open('model.joblib', 'rb') as f:
    testmodel = joblib.load(f)

sample = {'Songs' : [{'name': 'Got It On Me', 'year': 2020},
                {'name': 'Mannequin (feat. Lil Tjay)', 'year': 2020},
                {'name': 'Dior', 'year': 2019},
                {'name': 'Welcome To The Party', 'year': 2019}], 'Number' : 10}

print(transform_fn(testmodel, sample, 'application/json', 'application/json'))

"""