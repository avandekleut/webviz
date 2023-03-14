from networkx import Graph


from webvis.utils.network.clusterizer import Clusterizer
from webvis.utils.network.exporter import Exporter
from webvis.utils.network.node_resizer import NodeResizer


class Pipeline:
    def __init__(self, network: Graph):
        self.network = network

    def run(self, num_clusters=6, name='out'):
        Clusterizer(self.network).cluster(num_clusters)
        NodeResizer(self.network).update_node_sizes()
        Exporter(self.network).export_pyvis(f'{name}.html')
