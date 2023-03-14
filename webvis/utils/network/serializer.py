import pickle
from networkx import Graph

from webvis.utils.create_missing_folders import create_missing_folders


class Serializer:
    def __init__(self, network: Graph):
        self.network = network

    def save(self, filename: str):
        create_missing_folders(filename)
        pickle.dump(self.network, open(filename, 'wb'))

    def load(self, filename: str):
        self.network = pickle.load(open(filename, 'rb'))
