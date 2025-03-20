import csv
import re
from .base_checker import BaseChecker

class SubsystemViolationChecker(BaseChecker):
    def __init__(self, expected_dependencies_path):
        self.expected_dependencies = []
        self.subsystems = {}
        self.components = {}
        self.process_expected_dependencies(expected_dependencies_path)

    def process_expected_dependencies(self, expected_dependencies_path):
        with open(expected_dependencies_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                source_property, source_value, target_property, target_value = row
                self.expected_dependencies.append({
                    "source_property": source_property,
                    "source_value": source_value,
                    "target_property": target_property,
                    "target_value": target_value
                })

    def set_subsystems(self, subsystems):
        self.subsystems = subsystems     

    def set_components(self, components):
        self.components = components

    def is_dependency_a_violation(self, source, target):
        source_properties = self.components.get(source, {})
        target_properties = self.components.get(target, {})

        if source_properties.get("Subsystem") == target_properties.get("Subsystem"):
            return False

        for rule in self.expected_dependencies:
            source_property_value = source_properties.get(rule["source_property"], "")
            source_property_value = "." if source_property_value == "" else source_property_value
            target_property_value = target_properties.get(rule["target_property"], "")
            if re.search(rule["source_value"].lower(), source_property_value.lower()) and re.search(rule["target_value"].lower(), target_property_value.lower()):
                return False

        return True
    
    def is_dependency_a_deviation(self, source, target):
        source_properties = self.components.get(source, {})
        target_properties = self.components.get(target, {})

        target_subsystem_has_external_interfaces = self.subsystems.get(target_properties.get("Subsystem"), {}).get("has_external_interfaces", False)
        target_subsystem_has_internal_interfaces = self.subsystems.get(target_properties.get("Subsystem"), {}).get("has_internal_interfaces", False)
        
        if source_properties.get("Subsystem") == target_properties.get("Subsystem"):
            return False
        
        if target_properties.get("Interface") == "Interface Type 1":
            if source_properties.get("Category") != target_properties.get("Category") and target_subsystem_has_external_interfaces:
                return True
        elif target_properties.get("Interface") == "":
            if target_subsystem_has_internal_interfaces or target_subsystem_has_external_interfaces:
                return True
            
        return False

    def is_component_deviating(self, component):
        component_properties = self.components.get(component, {})
        
        return component_properties.get("Interface") != "" and not re.search("ITF", component)