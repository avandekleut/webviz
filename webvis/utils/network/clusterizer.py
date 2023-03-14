from networkx.algorithms.community.centrality import girvan_newman
from networkx import Graph


class Clusterizer:
    def __init__(self, network: Graph):
        self.network = network

    # TODO: Export once per cluster iteration to save compute
    def cluster(self, num_clusters: int):
        clusters = self.get_clusters(num_clusters)
        self.update_node_groups_by_clusters(clusters)

    def get_clusters(self, num_clusters: int) -> "list[list[str]]":
        cluster_generator = girvan_newman(self.network)

        iters = num_clusters - 1
        for iter in range(iters):
            try:
                clusters = next(cluster_generator)
                clusters = map(list, clusters)
            except StopIteration:
                pass

        return clusters

    def update_node_groups_by_clusters(self, clusters: "list[list[str]]"):
        for i, community in enumerate(clusters):
            for node in community:
                self.network.nodes[node]['group'] = i
