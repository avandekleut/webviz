from networkx.algorithms.community.centrality import girvan_newman
from networkx import Graph


from webvis.utils.network.clusterizer import Clusterizer
from webvis.utils.network.exporter import Exporter
from webvis.utils.network.node_resizer import NodeResizer


class Pipeline:
    def __init__(self, network: Graph):
        self.network = network
    
    def run(self):
        Clusterizer(self.network).cluster(7)
        NodeResizer(self.network).update_node_sizes()
        Exporter(self.network).export_pyvis('out.html')
