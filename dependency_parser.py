import sys
import json
import importlib
from utils import export
from utils.graph_utils import node_header, edge_header

def main(graph_name):
    # Load configuration
    with open("config.json", "r") as file:
        config = json.load(file)

    # Dynamically load the parser
    parser_module = importlib.import_module(f"parsers.{config['parser_type']}")
    parser = parser_module.Parser()  # Create an instance

    # Execute parsing
    print("Processing mapping...")
    parser.process_mapping(config["mapping_path"])
    print("Mapping processed.")

    print("Processing dependencies...")
    parser.process_dependencies(config["dependencies_path"], config["expected_dependencies_path"])
    print("Dependencies processed.")

    nodes, edges = parser.get_data()

    print("Writing nodes to CSV...")
    export.write_to_csv(f"{config['output_dir']}/{graph_name}/{graph_name}-nodes.csv", node_header, nodes)
    print(f"Nodes written to {config['output_dir']}/{graph_name}/{graph_name}-nodes.csv")

    print("Writing edges to CSV...")
    export.write_to_csv(f"{config['output_dir']}/{graph_name}/{graph_name}-edges.csv", edge_header, edges)
    print(f"Edges written to {config['output_dir']}/{graph_name}/{graph_name}-edges.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dependency_parser.py <graph_name>")
        sys.exit(1)
    graph_name = sys.argv[1]
    main(graph_name)