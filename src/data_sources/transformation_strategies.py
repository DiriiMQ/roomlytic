def lowercase_transform(value, config):
    return [v.lower() for v in value]

def map_transform(value, config):
    mapping = config["mapping"]
    # print(value)
    # print(config)
    # print(mapping)
    return [
        {target_key: v.get(source_key, None) for target_key, source_key in mapping.items()}
        for v in value
    ]

def default_transform(value, config):
    return config["default"]

def template_transform(value, config):
    return config["template"].format(**value)
