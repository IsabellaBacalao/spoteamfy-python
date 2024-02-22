import numpy as np
# import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import joblib
import json

# Fonction ajustée pour inclure les données utilisateur dans la visualisation des données d'origine
def predict_cluster(user_data):
    # Chargement des modèles pré-entraînés et des coordonnées TSNE pour le dataset d'origine
    scaler = joblib.load('scaler.save')
    pca = joblib.load('pca_model.save')
    kmeans_optimal = joblib.load('kmeans_model.save')
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    X_tsne_orig = np.load('X_tsne.npy')  # Coordonnées TSNE pré-calculées du dataset d'origine
    orig_clusters = kmeans_optimal.labels_

    # Conversion des données utilisateur en DataFrame et prétraitement
    user_df = pd.DataFrame(user_data)
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    user_features = user_df[features]
    user_features_imputed = imputer.fit_transform(user_features)
    user_features_scaled = scaler.transform(user_features_imputed)
    user_features_pca = pca.transform(user_features_scaled)

    # Prédiction du cluster pour les données utilisateur
    user_clusters = kmeans_optimal.predict(user_features_pca)

    # Affichage des données d'origine et utilisateur sur le même graphique
    # plt.figure(figsize=(12, 8))
    #
    # # Plot des points TSNE pour les données d'origine
    # plt.scatter(X_tsne_orig[:, 0], X_tsne_orig[:, 1], c=orig_clusters, cmap='viridis', alpha=0.5, label='Original Data')
    #
    # # Plot des points PCA pour les données utilisateur (comme approximation)
    # # Note: ceci est une simplification. En réalité, vous pourriez vouloir recalculer TSNE pour une intégration parfaite.
    # plt.scatter(user_features_pca[:, 0], user_features_pca[:, 1], c='red', edgecolor='white', linewidth=1, s=100, label='User Data')
    #
    # plt.title('Visualisation TSNE avec données utilisateur')
    # plt.xlabel('PCA Dimension 1')
    # plt.ylabel('PCA Dimension 2')
    # plt.legend()
    # plt.show()


    user_features_pca_coords = user_features_pca  # Si vous utilisez PCA comme approximation
    # Préparation des données du graphique pour la réponse
    graph_data = {
        "user_cluster": int(user_clusters[0]),
        "user_pca_coords": user_features_pca_coords.tolist(),  # Coordonnées PCA des utilisateurs
        "user_cluster": user_clusters.tolist(),
    }

    return graph_data

# Exemple d'utilisation
with open('features.json', 'r') as file:
    user_data = json.load(file)

response = predict_cluster(user_data)
print(response)

