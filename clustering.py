import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
from sklearn.metrics import silhouette_score
import numpy as np

# Charger les données (Assurez-vous de mettre à jour le chemin vers votre fichier de données)
df = pd.read_csv('dataset.csv')

# Préparation des données: Sélectionner les caractéristiques numériques pertinentes pour le clustering
features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
X = df[features]

# Normaliser les caractéristiques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Déterminer le nombre optimal de clusters en utilisant la méthode du coude
inertia = []
silhouette_coefficients = []
# Choisir le nombre de clusters basé sur les graphiques précédents

# Appliquer K-means avec le nombre optimal de clusters choisi selon les graphiques
n_clusters_optimal = 7# (le nombre de clusters que vous avez choisi, par exemple 5)
kmeans_optimal = KMeans(n_clusters=n_clusters_optimal, random_state=42)
kmeans_optimal.fit(X_scaled)

# Nommer les clusters en fonction de leurs caractéristiques moyennes
def name_clusters(cluster_centers, features):
    cluster_names = []
    print(cluster_centers)
    for i, center in enumerate(cluster_centers):
        characteristics = [features[j] for j in center.argsort()[-3:]]  # Prendre les 3 caractéristiques les plus élevées
        name = f"Cluster {i+1} - {' '.join(characteristics)}"
        print(name)
        cluster_names.append(name)
    return cluster_names

cluster_names = name_clusters(kmeans_optimal.cluster_centers_, features)

# Associer chaque point de données à son cluster nommé
labels_named = np.array(cluster_names)[kmeans_optimal.labels_]

# Réduire la dimensionnalité pour la visualisation avec t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

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


# Sauvegarde de l'objet StandardScaler
scaler_filename = "scaler.save"
joblib.dump(scaler, scaler_filename)

# Sauvegarde du modèle KMeans
model_filename = "kmeans_model.save"
joblib.dump(kmeans_optimal, model_filename)

# Si nécessaire, sauvegarder le nom des clusters
names_filename = "cluster_names.save"
joblib.dump(cluster_names, names_filename)

print(f"Modèle sauvegardé sous : {model_filename}")
print(f"Scaler sauvegardé sous : {scaler_filename}")
print(f"Noms des clusters sauvegardés sous : {names_filename}")
