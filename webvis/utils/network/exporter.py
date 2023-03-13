from networkx import Graph
from pyvis.network import Network

from webvis.utils.create_missing_folders import create_missing_folders


class Exporter:
    def __init__(self, network: Graph):
        self.network = network

    def export_pyvis(self, filename: str):
        create_missing_folders(filename)

        net = Network(
            select_menu=True,
            cdn_resources='remote'
        )
        net.from_nx(self.network)
        net.save_graph(filename)
