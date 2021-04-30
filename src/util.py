import yaml


def get_config():
    with open("config/config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.CLoader)
    return config
