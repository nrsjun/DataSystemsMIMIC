import yaml
from yaml.loader import SafeLoader



with open('credentials2.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)