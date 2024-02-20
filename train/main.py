import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
dataset = pd.read_csv("dataset.csv")

# Select relevant features for clustering
features = dataset[
    [
        "popularity",
        "duration_ms",
        "explicit",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "time_signature",
    ]
]

# Perform KMeans clustering
kmeans = KMeans(n_clusters=5)  # You can adjust the number of clusters as needed
clusters = kmeans.fit_predict(features)

# Add cluster labels to the dataset
dataset["cluster"] = clusters

# Visualize clusters
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Scatter plot 1: duration_ms vs popularity
sns.scatterplot(
    data=dataset,
    x="duration_ms",
    y="popularity",
    hue="cluster",
    palette="viridis",
    ax=axes[0, 0],
)
axes[0, 0].set_title("Duration vs Popularity")
axes[0, 0].set_xlabel("Duration (ms)")
axes[0, 0].set_ylabel("Popularity")

# Scatter plot 2: danceability vs energy
sns.scatterplot(
    data=dataset,
    x="danceability",
    y="energy",
    hue="cluster",
    palette="viridis",
    ax=axes[0, 1],
)
axes[0, 1].set_title("Danceability vs Energy")
axes[0, 1].set_xlabel("Danceability")
axes[0, 1].set_ylabel("Energy")

# Scatter plot 3: loudness vs valence
sns.scatterplot(
    data=dataset,
    x="loudness",
    y="valence",
    hue="cluster",
    palette="viridis",
    ax=axes[1, 0],
)
axes[1, 0].set_title("Loudness vs Valence")
axes[1, 0].set_xlabel("Loudness")
axes[1, 0].set_ylabel("Valence")

# Scatter plot 4: speechiness vs acousticness
sns.scatterplot(
    data=dataset,
    x="speechiness",
    y="acousticness",
    hue="cluster",
    palette="viridis",
    ax=axes[1, 1],
)
axes[1, 1].set_title("Speechiness vs Acousticness")
axes[1, 1].set_xlabel("Speechiness")
axes[1, 1].set_ylabel("Acousticness")

plt.tight_layout()
plt.show()
