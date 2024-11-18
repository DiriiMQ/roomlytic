class TransformationStrategy:
    def transform(self, value, config):
        raise NotImplementedError("Transform method not implemented")

class LowercaseTransformation(TransformationStrategy):
    def transform(self, value, config):
        if value is None:
            return []
        return [v.lower() for v in value]

class MapTransformation(TransformationStrategy):
    def transform(self, value, config):
        if value is None:
            return []
        
        mapping = config["mapping"]
        return [
            {target_key: v.get(source_key, None) for target_key, source_key in mapping.items()}
            for v in value
        ]

class DefaultTransformation(TransformationStrategy):
    def transform(self, value, config):
        return config["default"]

class TemplateTransformation(TransformationStrategy):
    def transform(self, value, config):
        if value is None:
            return ""
        return config["template"].format(**value)