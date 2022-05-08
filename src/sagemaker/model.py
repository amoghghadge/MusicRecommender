import numpy as np
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Read in data
spotify_data = pd.read_csv('./data/data.csv')

# Cluster songs using K-Means
cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=20, verbose=2))],verbose=True)
X = spotify_data.select_dtypes(np.number)
number_cols = list(X.columns)
cluster_pipeline.fit(X)

with open('model.joblib', 'wb') as f:
    joblib.dump(cluster_pipeline, f)

