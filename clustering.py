import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
from sklearn.metrics import silhouette_score
import numpy as np
import joblib

# Charger les données
df = pd.read_csv('dataset.csv')

# Préparation des données: Sélectionner les caractéristiques numériques pertinentes pour le clustering
features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
X = df[features]

# Normaliser les caractéristiques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Appliquer PCA pour la réduction de dimensionnalité
pca = PCA(n_components=0.9)  # Conserver 90% de la variance
X_pca = pca.fit_transform(X_scaled)

# Appliquer K-means sur les données réduites par PCA
n_clusters_optimal = 7
kmeans_optimal = KMeans(n_clusters=n_clusters_optimal, random_state=42)
kmeans_optimal.fit(X_pca)

# Nommer les clusters en fonction de leurs caractéristiques moyennes
def name_clusters(cluster_centers, features):
    cluster_names = []
    for i, center in enumerate(cluster_centers):
        characteristics = [features[j] for j in center.argsort()[-3:]]
        name = f"Cluster {i+1} - {' '.join(characteristics)}"
        cluster_names.append(name)
    return cluster_names

cluster_names = name_clusters(kmeans_optimal.cluster_centers_, features)

# Associer chaque point de données à son cluster nommé
labels_named = np.array(cluster_names)[kmeans_optimal.labels_]

# Réduire la dimensionnalité pour la visualisation avec t-SNE sur les données PCA
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_pca)  # Appliquer t-SNE sur les données PCA
np.save('X_tsne.npy', X_tsne)
# Visualiser les clusters avec des noms
df_vis = pd.DataFrame(X_tsne, columns=['TSNE1', 'TSNE2'])
df_vis['Cluster'] = labels_named

plt.figure(figsize=(10, 8))
sns.scatterplot(x='TSNE1', y='TSNE2', hue='Cluster', palette=sns.color_palette("hsv", n_clusters_optimal), data=df_vis)
plt.title('Visualisation des clusters de caractéristiques Spotify avec des noms')
plt.xlabel('TSNE Dimension 1')
plt.ylabel('TSNE Dimension 2')
plt.legend(title='Cluster')
plt.show()

# Sauvegarde des objets
joblib.dump(scaler, "scaler.save")
joblib.dump(pca, "pca_model.save")
joblib.dump(kmeans_optimal, "kmeans_model.save")
joblib.dump(cluster_names, "cluster_names.save")

print(f"Modèle sauvegardé sous : kmeans_model.save")
print(f"Scaler sauvegardé sous : scaler.save")
print(f"PCA modèle sauvegardé sous : pca_model.save")
print(f"Noms des clusters sauvegardés sous : cluster_names.save")

