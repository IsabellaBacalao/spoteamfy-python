import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Étape 1: Charger le modèle
model_path = 'music_genre_classifier_model.h5'
model = load_model(model_path)

# Étape 2: Préparer les données (ceci est un exemple, ajustez selon vos données)
# Supposons que vous avez déjà un DataFrame `df` avec vos données
df = pd.read_csv('dataset.csv')
# Effectuez ici le prétraitement nécessaire (normalisation, etc.)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df.drop('track_genre', axis=1))  # Remplacer 'genre' par la colonne cible appropriée

# Étape 3: Obtenir les prédictions
predictions = model.predict(X_scaled)
predicted_classes = np.argmax(predictions, axis=1)

# Étape 4: Réduire la dimensionnalité pour la visualisation
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

# Étape 5: Visualiser les clusters
df_vis = pd.DataFrame(X_tsne, columns=['TSNE1', 'TSNE2'])
df_vis['Predicted Genre'] = predicted_classes

plt.figure(figsize=(10, 8))
sns.scatterplot(x='TSNE1', y='TSNE2', hue='Predicted Genre', palette=sns.color_palette("hsv", len(np.unique(predicted_classes))), data=df_vis)
plt.title('Clusters de genres musicaux prédits')
plt.xlabel('TSNE Dimension 1')
plt.ylabel('TSNE Dimension 2')
plt.legend(title='Predicted Genre')
plt.show()

