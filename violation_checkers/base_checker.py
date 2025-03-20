from abc import ABC, abstractmethod

class BaseChecker(ABC):
    def __init__(self):
        self.expected_dependencies = {}

    @abstractmethod
    def process_expected_dependencies(self, expected_dependencies):
        pass
    
    @abstractmethod
    def is_dependency_a_violation(self, source, target):
        pass

    @abstractmethod
    def is_dependency_a_deviation(self, source, target):
        pass
