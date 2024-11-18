from .transformation_strategies import (
    TransformationStrategy,
    LowercaseTransformation,
    MapTransformation,
    DefaultTransformation,
    TemplateTransformation
)

class TransformationFactory:
    STRATEGIES = {
        "lowercase": LowercaseTransformation,
        "map": MapTransformation,
        "default": DefaultTransformation,
        "template": TemplateTransformation
    }

    @staticmethod
    def get_transformation(strategy_name: str) -> TransformationStrategy:
        strategy_name = strategy_name.lower()
        if strategy_name in TransformationFactory.STRATEGIES:
            return TransformationFactory.STRATEGIES[strategy_name]
        else:
            raise ValueError(f"Invalid transformation strategy: {strategy_name}")
        