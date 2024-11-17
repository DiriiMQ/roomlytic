def lowercase_transform(value, config):
    return value.lower()

def map_transform(value, config):
    mapping = config["mapping"]
    print(value)
    print(config)
    return [
        {target_key: value.get(source_key, None) for target_key, source_key in mapping.items()}
    ]

def default_transform(value, config):
    return config["default"]

def template_transform(value, config):
    return config["template"].format(**value)
