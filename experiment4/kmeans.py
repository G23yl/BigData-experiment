import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score


class Kmeans:
    def __init__(self, data, k=3, epsilon=1e-8) -> None:
        self.k = k
        self.data = data
        self.epsilon = epsilon

    def initialize_centroids(self):
        centroids = self.data[np.random.choice(data.shape[0], self.k, replace=False)]
        return sorted(centroids, key=lambda c: c[0], reverse=True)

    def get_clusters(self, centroids):
        distances = np.linalg.norm(self.data[:, np.newaxis] - centroids, axis=2, ord=2)
        cluster_labels = np.argmin(distances, axis=1)
        return cluster_labels

    def update_centroids(self, cluster_labels):
        new_centroids = np.array(
            [self.data[cluster_labels == i].mean(axis=0) for i in range(self.k)]
        )
        return new_centroids

    def kmeans(self):
        centroids = self.initialize_centroids()
        while True:
            cluster_labels = self.get_clusters(centroids)
            new_centroids = self.update_centroids(cluster_labels)
            if np.sum(np.linalg.norm(new_centroids - centroids, axis=1, ord=2)) < self.epsilon:
                break
            centroids = new_centroids
        SSE = 0
        for i in range(self.k):
            d = np.array(self.data[cluster_labels == i])
            SSE += np.sum(np.linalg.norm(d - centroids[i], ord=2, axis=1))
        return cluster_labels, SSE


def draw_cluster(data, labels, acc, SSE, k=3):
    colors = np.array(
        [
            "#FF0000",
            "#0000FF",
            "#00FF00",
            "#FFFF00",
            "#00FFFF",
            "#FF00FF",
            "#800000",
            "#008000",
            "#000080",
            "#808000",
            "#800080",
            "#008080",
            "#444444",
            "#FFD700",
            "#008080",
        ]
    )
    data = np.array(data)
    labels = np.array(labels)
    text = "acc: " + str(acc) + "   SSE: " + str(SSE)
    plt.title(text)
    plt.scatter(data[:, 0], data[:, 1], marker="o", c="black", s=7)
    for i in range(k):
        plt.scatter(
            data[np.nonzero(labels == i), 0],
            data[np.nonzero(labels == i), 1],
            c=colors[i],
            s=7,
            marker="o",
        )
    plt.show()


def data_processing(file_name: str):
    df = pd.read_csv(file_name)
    df = df.loc[
        :,
        [
            "Popularity",
            "Score-10",
            "Score-9",
            "Score-8",
            "Score-7",
            "Score-6",
            "Score-5",
            "Score-4",
            "Score-3",
            "Score-2",
        ],
    ]
    df.dropna(inplace=True)
    data = []
    for row in df.itertuples():
        if (
            row[1] != "Unknown"
            and row[2] != "Unknown"
            and row[3] != "Unknown"
            and row[4] != "Unknown"
            and row[5] != "Unknown"
            and row[6] != "Unknown"
            and row[7] != "Unknown"
            and row[8] != "Unknown"
            and row[9] != "Unknown"
            and row[10] != "Unknown"
        ):
            row1 = [int(t) for t in row]  # 把元组里面的数据类型变为int
            data.append(row1[1:])
    data = sorted(data, key=lambda d: d[0], reverse=True)
    length = len(data)
    selected_data = []
    # 1, 2, 3代表高中低
    for i in range(60):
        d1 = data[i]
        d1.append(1)
        selected_data.append(d1)
    for i in range(60):
        d2 = data[i + length // 2]
        d2.append(2)
        selected_data.append(d2)
    for i in range(60):
        d3 = data[i - 60]
        d3.append(3)
        selected_data.append(d3)
    columns = ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "label"]
    scaler = MinMaxScaler()
    selected_data = scaler.fit_transform(selected_data)
    for i in range(60):
        selected_data[i][10] = 0
        selected_data[i + 60][10] = 1
        selected_data[i + 120][10] = 2
    selected_data = pd.DataFrame(selected_data, columns=columns)
    return selected_data

def acc_score(original_labels, pred_labels):
    max1 = np.argmax(np.bincount(pred_labels[: 60]))
    max2 = np.argmax(np.bincount(pred_labels[60 : 120]))
    max3 = np.argmax(np.bincount(pred_labels[120: 180]))
    for i in range(60):
        original_labels[i] = max1
        original_labels[i + 60] = max2
        original_labels[i + 120] = max3
    return accuracy_score(original_labels, pred_labels)


if __name__ == "__main__":
    data = data_processing("./anime.csv")
    features = ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10"]
    two_dim_features = ["d2", "d10"]
    original_labels = data["label"]
    kmeans = Kmeans(np.array(data[features]))
    labels, SSE = kmeans.kmeans()
    acc = acc_score(original_labels, labels)
    # print(f"acc: {acc}\n")
    # print(f"SSE: {SSE}\n")
    
    # 画图只用2维
    kmeans = Kmeans(np.array(data[two_dim_features]))
    labels, _ = kmeans.kmeans()
    draw_cluster(data[two_dim_features], labels, acc, SSE)