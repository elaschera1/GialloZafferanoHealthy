import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
path_dataset = "Dataset/GialloZafferanoDataset.csv"


def get_metrics(eps, min_samples, dataset, iter_):
    dbscan_model_ = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan_model_.fit(dataset)

    noise_indices = dbscan_model_.labels_ == -1

    if True in noise_indices:
        neighboors = NearestNeighbors(n_neighbors=6).fit(dataset)
        distances, indices = neighboors.kneighbors(dataset)
        noise_distances = distances[noise_indices, 1:]
        noise_mean_distance = round(noise_distances.mean(), 3)
    else:
        noise_mean_distance = None

    number_of_clusters = len(set(dbscan_model_.labels_[dbscan_model_.labels_ >= 0]))

    print("%3d | Tested with eps = %3s and min_samples = %3s | %5s %4s" % (
    iter_, eps, min_samples, str(noise_mean_distance), number_of_clusters))

    return (noise_mean_distance, number_of_clusters)


def ricerca_iperparametri(dataframe):
    eps_to_test = [round(esp, 1) for esp in np.arange(0.1, 2, 0.1)]
    min_samples_to_test = range(5, 50, 5)

    # Dataframe per la metrica sulla distanza media dei noise points dai K punti più vicini
    results_noise = pd.DataFrame(
        data=np.zeros((len(eps_to_test), len(min_samples_to_test))),
        columns=min_samples_to_test,
        index=eps_to_test
    )

    # Dataframe per la metrica sul numero di cluster
    results_cluster = pd.DataFrame(
        data=np.zeros((len(eps_to_test), len(min_samples_to_test))),
        columns=min_samples_to_test,
        index=eps_to_test
    )

    iter_ = 0
    print("ITER| INFO%s |  DIST    CLUS" % (" " * 39))
    print("-" * 65)

    for eps in eps_to_test:
        for min_samples in min_samples_to_test:
            iter_ += 1

            noise_metric, cluster_metric, = get_metrics(eps, min_samples, dataframe, iter_)

            results_noise.loc[eps, min_samples] = noise_metric
            results_cluster.loc[eps, min_samples] = cluster_metric

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    sns.heatmap(results_noise, annot=True, ax=ax1, cbar=False).set_title("METRIC: Mean Noise Points Distance")
    sns.heatmap(results_cluster, annot=True, ax=ax2, cbar=False).set_title("METRIC: Number of clusters")

    ax1.set_xlabel("N")
    ax2.set_xlabel("N")
    ax1.set_ylabel("EPSILON")
    ax2.set_ylabel("EPSILON")

    plt.tight_layout()
    plt.savefig("Img/dbScanParameters.png")
    plt.show()

print("INIZIO K-MEANS")

df = pd.read_csv(path_dataset)
colonne = ['Energia(kcal)','Carboidrati(g)','Zuccheri(g)','Proteine(g)','Grassi(g)','GrassiSaturi(g)','Fibre(g)','Colesterolo(g)','Sodio(g)']

X = df[colonne]

inertia_values = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, n_init='auto')
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)

plt.figure(figsize=(10, 10))
plt.plot(range(1, 11), inertia_values, marker='o')
plt.title("Analisi del gomito")
plt.xlabel("Numero di cluster")
plt.ylabel("Inertia")
plt.xticks(range(1, 11))
plt.savefig("Img/Analisi_del_gomito.png")
plt.show()

silhouette_scores = {}
for k in range(2, 25,1):
    kmeans = KMeans(n_clusters=k, n_init='auto')
    kmeans.fit(X)
    labels_k = kmeans.labels_
    score_k = metrics.silhouette_score(X, labels_k)
    silhouette_scores[k] = score_k
    print("Testo kMeans con k = %d\tSS: %5.4f" % (k, score_k))

plt.figure(figsize = (16,5))
plt.plot(silhouette_scores.values())
plt.xticks(range(0,23,1), silhouette_scores.keys())
plt.title("Silhouette Metric")
plt.xlabel("k")
plt.ylabel("Silhouette")
plt.axvline(1, color = "r")
plt.savefig("Img/Silhouette.png")
plt.show()

print("Addestro kmeans per il suo k migliore ")

kmeans = KMeans(n_clusters=3, random_state=42)

df['Cluster'] = kmeans.fit_predict(X)
colonne = colonne + ['Cluster_KMEANS']

cluster_labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

distances = np.linalg.norm(X - cluster_centers[cluster_labels], axis=1)

anomaly_thresholt = np.percentile(distances, 95)
anomalies = X[distances > anomaly_thresholt]

df_merged = pd.merge(df[:], anomalies, left_index=True, right_index=True, how='inner')
df_merged.to_csv("Dataset/ricetteAnomale.csv")

print("Salvato 'ricetteAnomale.csv' correttamente! ")

print("FINE KMEANS")

print("INIZIO DBSCAN")
colonne = ['Energia(kcal)','Carboidrati(g)','Zuccheri(g)','Proteine(g)','Grassi(g)','GrassiSaturi(g)','Fibre(g)','Colesterolo(g)','Sodio(g)']

scaler = StandardScaler()
data_scaled = scaler.fit_transform(df[colonne])

ricerca_iperparametri(data_scaled)

dbscan = DBSCAN(eps=0.3, min_samples=5)
clusters = dbscan.fit_predict(data_scaled)

df['Cluster_DBscan'] = clusters

num_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
print(f"Numero di cluster ottenuti: {num_clusters}")

df.to_csv('Dataset/ricetteDBscan.csv', index=False)

print("FINE DBSCAN")