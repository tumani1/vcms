from os.path import join
import yaml
from settings import CONFIG_PATH

with open(join(CONFIG_PATH,'auth.yaml')) as acf:
    token_settings = yaml.safe_load(acf)
