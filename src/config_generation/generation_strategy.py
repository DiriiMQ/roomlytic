import abc

class GenerationStrategy(abc.ABC):
    @abc.abstractmethod
    def generate_config(self, supplier_info: dict) -> dict:
        """ Generate a configuration based on the supplier information (name and url) """
        pass