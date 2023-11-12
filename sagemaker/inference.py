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
obj = s3.get_object(Bucket= "aghadge-song-data", Key= "us_charts_with_audio_features.csv") 

spotify_data = pd.read_csv(obj['Body'])
columns_to_use = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
X = spotify_data[columns_to_use]

# Recommendation System
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))

def find_song(name, artist):
    song_data = defaultdict()
    results = sp.search(q= 'track: {} artist: {}'.format(name, artist), type='track', limit=1)
    if results['tracks']['items'] == []:
        return None
    
    results = results['tracks']['items'][0]

    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]
    
    song_data['name'] = [name]
    song_data['artists'] = [artist]
    
    for key, value in audio_features.items():
        song_data[key] = value
    
    return pd.DataFrame(song_data)

def get_song_data(song, spotify_data):
    # Check if song is in the spotify dataset, otherwise use find_song method
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name']) 
                                & (spotify_data['artists'] == song['artist'])].iloc[0]
        return song_data
    except IndexError:
        return find_song(song['name'], song['artist'])

def get_mean_vector(song_list, spotify_data):
    song_vectors = []
    
    # Add all songs to song_vectors
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[columns_to_use].values
        song_vectors.append(song_vector)
    
    # Convert to numpy array then use np.mean
    converted_arrays = [arr.astype(np.float64).flatten() for arr in song_vectors]
    song_matrix = np.array(converted_arrays)
    return np.mean(song_matrix, axis=0)

def flatten_dict_list(dict_list):
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def recommend_songs(song_list, spotify_data, cluster_pipeline, n_songs=10):
    # Compute average vector of input songs
    song_center = get_mean_vector(song_list, spotify_data)
    scaler = cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[columns_to_use])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))

    # Find closest songs in dataset to the average vector using cosine distance
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    # Recommend corresponding songs from the dataset
    rec_songs = spotify_data.iloc[index]
    song_dict = flatten_dict_list(song_list)
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]

    # Format output
    metadata_cols = ['name', 'artists', 'url']
    result = rec_songs[metadata_cols].to_dict(orient='records')
    urls = []
    images = []
    for song in result:
        urls.append(song['url'])
        
    tracks = sp.tracks(urls)
    
    for t in tracks['tracks']:
        images.append(t['album']['images'][0]['url'])
        
    for i, song in enumerate(result):
        song['image_url'] = images[i]
    return result

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