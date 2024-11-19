from generation_strategy import GenerationStrategy
from default_generation_strategy import DefaultGenerationStrategy

class ConfigGenerator:
    def __init__(self, generation_strategy: GenerationStrategy = DefaultGenerationStrategy):
        self.generation_strategy = generation_strategy()

    def generate_config(self, supplier_info: dict) -> dict:
        return self.generation_strategy.generate_config(supplier_info)