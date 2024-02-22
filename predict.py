import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import seaborn as sns
import matplotlib.pyplot as plt

# ... (le reste du script pour le prétraitement et la formation des clusters)
features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
# Imaginons que vous ayez de nouvelles données utilisateur que vous souhaitez traiter
# Pour l'exemple, supposons que nous avons un DataFrame 'new_user_data' au même format que 'df'
new_user_data = pd.read_csv('new_user_data.csv')
new_user_features = new_user_data[features]

# Prétraitement des nouvelles données avec le StandardScaler sauvegardé
scaler = joblib.load('scaler.save')
new_user_features_scaled = scaler.transform(new_user_features)

# Utilisation du modèle KMeans sauvegardé pour attribuer un cluster aux nouvelles données
kmeans_optimal = joblib.load('kmeans_model.save')
new_user_labels = kmeans_optimal.predict(new_user_features_scaled)

# Associer chaque nouvelle donnée utilisateur à son cluster nommé
cluster_names = joblib.load('cluster_names.save')
new_user_cluster_names = np.array(cluster_names)[new_user_labels]

# Ajouter les noms des clusters au DataFrame des nouvelles données utilisateur
new_user_data['Cluster'] = new_user_cluster_names

# Afficher le DataFrame avec le cluster assigné
print(new_user_data[['Cluster'] + features])

