import os
import sys

from dynaconf import Dynaconf

ALLOWED_ENVS = ['DEV', "BETA", 'PROD']
ENVIRONMENT = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ALLOWED_ENVS else 'DEV'

config_files = ['config.yaml']
if ENVIRONMENT == 'BETA':
    config_files.append('config-BETA.yaml')
if ENVIRONMENT == 'PROD':
    config_files.append('config-PROD.yaml')


settings = Dynaconf(
    root_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    settings_files=config_files,
    load_dotenv=True,
    dotenv_path="../.env"
)
