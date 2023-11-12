import numpy as np
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Read in data
spotify_data = pd.read_csv('./data/us_charts_with_audio_features.csv')

# Cluster songs using K-Means
spotify_data.dropna(inplace=True)
cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                             ('kmeans', KMeans(n_clusters=7, verbose=2, n_init=10))], verbose=True)
columns_to_use = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
X = spotify_data[columns_to_use]
cluster_pipeline.fit(X)

with open('model.joblib', 'wb') as f:
    joblib.dump(cluster_pipeline, f)

