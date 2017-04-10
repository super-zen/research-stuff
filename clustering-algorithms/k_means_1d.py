def k_means_1d(S, k):
    X = sorted(S)
    last_centroids = None
    centroids = [ X[0] + (X[-1] - X[0]) / k * i for i in range(k) ]

    while centroids != last_centroids:
        clusters = [ [] for centroid in centroids ]

        for x in X:
            dists = []

            for centroid in centroids:
                if centroid == None:
                    dists.append(float('inf'))
                    continue

                dists.append(abs(x - centroid))

            clusters[dists.index(min(dists))].append(x)

        last_centroids = centroids
        centroids = [ sum(cluster) / len(cluster) if len(cluster) > 0 else None for cluster in clusters ]
        
    return centroids, clusters

def get_largest_clusters(centroids, clusters):
    magnitudes = [ len(cluster) for cluster in clusters ]
    max_mag = max(magnitudes)

    large_clusters = []
    significant_centroids = []

    for i, cluster in enumerate(clusters):
        if len(cluster) == max_mag:
            large_clusters.append(cluster)
            significant_centroids.append(centroids[i])

    return significant_centroids, large_clusters

def get_most_focused_clusters(centroids, clusters):
    dists = [ cluster[-1] - cluster[0] for cluster in clusters ]
    min_dist = min(dists)

    focused_clusters = []
    significant_centroids = []

    for i, dist in enumerate(dists):
        if dist == min_dist:
            focused_clusters.append(clusters[i])
            significant_centroids.append(centroids[i])
            
    return significant_centroids, focused_clusters

