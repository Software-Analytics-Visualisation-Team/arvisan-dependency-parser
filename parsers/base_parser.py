from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self):
        # Common storage for all parsers
        self.nodes = {}  
        self.edges = {}

        print(f"{self.__module__} initialized.")

    @abstractmethod
    def process_mapping(self, mapping_path):
        pass
    
    @abstractmethod
    def process_dependencies(self, depenendencies_path, expected_dependencies_path = None):
        pass
    
    def get_data(self):
        """Returns parsed nodes and edges."""
        return self.nodes, self.edges
