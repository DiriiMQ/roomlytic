from generation_strategy import GenerationStrategy

class DefaultGenerationStrategy(GenerationStrategy):
    def generate_config(self, supplier_info):
        """ Generate a configuration based on the supplier information (name and url) """
        config = {
            "name": supplier_info["name"],
            "url": supplier_info["url"],
            "config": {}
        }

        # Add more logics later

        return config