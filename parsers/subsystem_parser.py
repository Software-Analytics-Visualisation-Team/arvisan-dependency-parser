import csv

from .base_parser import BaseParser
from utils.graph_utils import create_domain_node, create_application_node, create_sublayer_node, create_module_node, create_edge, update_node_color
from violation_checkers.subsystem_violation_checker import SubsystemViolationChecker

class Parser(BaseParser):
    subsystems = {}
    components = {}

    def process_mapping(self, mapping_path):

        self.nodes['domain_node'] = create_domain_node("All Subsystem Groups")

        # Helper function to update subsystem information
        def update_subsystem(subsystem, interface):
            current_subsystem = self.subsystems.get(subsystem, {'has_external_interfaces': False, 'has_internal_interfaces': False})	
            if interface == 'External':
                current_subsystem['has_external_interfaces'] = True
            elif interface == 'Internal':
                current_subsystem['has_internal_interfaces'] = True
            self.subsystems[subsystem] = current_subsystem

        # Read and process the mapping CSV file
        with open(mapping_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    component = row["Component"]
                    subsystem = row["Subsystem"]
                    subsystem_group = row["Subsystem Group"]
                    category = row["Category"]
                    deployment = row["Deployment"]
                    interface = row["Interface"]
                except KeyError as e:
                    print(f"Missing key in CSV row: {e}")
                    continue

                if subsystem_group and subsystem:
                    update_subsystem(subsystem, interface)  # Update subsystem information

                    # Store component information
                    self.components[component] = {
                        "Component Name": component,
                        "Subsystem Group": subsystem_group,
                        "Subsystem": subsystem,
                        "Category": category,
                        "Deployment": deployment,
                        "Interface": interface
                    }

                    # Generate node IDs
                    subgrp_node_id = "subgrp:" + subsystem_group
                    subsys_node_id = "subsys:" + subsystem
                    comp_node_id = "comp:" + component

                    # Create and add application node if it doesn't exist
                    if subgrp_node_id not in self.nodes.keys():
                        subgrp_node = create_application_node(subgrp_node_id, subsystem_group, "Subsystem Group")
                        self.nodes[subgrp_node_id] = subgrp_node

                        # Add edge from domain to application
                        domain_contains_edge = create_edge(
                            "domain_node",
                            subgrp_node_id,
                            "CONTAINS",
                        )
                        self.edges[domain_contains_edge[0]] = domain_contains_edge

                    # Create and add sublayer node if it doesn't exist
                    if subsys_node_id not in self.nodes.keys():
                        subsys_node = create_sublayer_node(subsys_node_id, subsystem, "Subsystem")
                        self.nodes[subsys_node_id] = subsys_node

                    # Create and add module node if it doesn't exist
                    if comp_node_id not in self.nodes.keys():
                        node_properties = {
                            "InterfaceProfileCategory": interface,
                            "Deployment": deployment,
                        }
                        comp_node = create_module_node(comp_node_id, component, "Module", node_properties = node_properties)
                        self.nodes[comp_node_id] = comp_node

                    # Add edge from application to sublayer
                    subgrp_contains_edge = create_edge(
                        subgrp_node_id, subsys_node_id, "CONTAINS"
                    )
                    if subgrp_contains_edge[0] not in self.edges:
                        self.edges[subgrp_contains_edge[0]] = subgrp_contains_edge

                    # Add edge from sublayer to module
                    subsys_contains_edge = create_edge(
                        subsys_node_id, comp_node_id, "CONTAINS"
                    )
                    if subsys_contains_edge[0] not in self.edges:
                        self.edges[subsys_contains_edge[0]] = subsys_contains_edge
    
        print(f"Number of subsystems added to the graph: {len(self.subsystems)}")
        print(f"Number of components added to the graph: {len(self.components)}")

    def process_dependencies(self, depenendencies_path, expected_dependencies_path = None):
        with open(depenendencies_path, "r") as file:
            dependency_count = 0
    
            if expected_dependencies_path:
                print("Checking for dependency violation or deviation...")
            
            for line in file:
                line = line.strip()
                if "=>" in line:
                    source, target = line.split("=>")
                    source_node_id = "comp:" + source
                    target_node_id = "comp:" + target

                    if source_node_id in self.nodes.keys() and target_node_id in self.nodes.keys():
                        if expected_dependencies_path:
                            # Check for dependency violation or deviation
                            violation_checker = SubsystemViolationChecker(expected_dependencies_path)
                            violation_checker.set_subsystems(self.subsystems)
                            violation_checker.set_components(self.components)
                            
                            if violation_checker.is_dependency_a_violation(source, target):
                                current_edge = create_edge(source_node_id, target_node_id, "VIOLATES")
                            elif violation_checker.is_dependency_a_deviation(source, target):
                                current_edge = create_edge(source_node_id, target_node_id, "DEVIATES")
                            else:
                                if violation_checker.is_component_deviating(target):
                                    self.nodes = update_node_color(self.nodes, target_node_id, "#ff9933")  # Update node color for deviation

                                current_edge = create_edge(source_node_id, target_node_id, "CALLS")
                    else:
                        current_edge = create_edge(source_node_id, target_node_id, "CALLS")
                    if current_edge[0] not in self.edges:
                        self.edges[current_edge[0]] = current_edge

                    dependency_count += 1
            
            print(f"Total dependencies read: {dependency_count}")
            print(f"Number of dependencies added to the graph: {len(self.edges)}")

            if expected_dependencies_path:
                print(f"Number of violations: {len([edge for edge in self.edges.values() if edge[1] == 'VIOLATES'])}")
                print(f"Number of deviations: {len([edge for edge in self.edges.values() if edge[1] == 'DEVIATES'])}")