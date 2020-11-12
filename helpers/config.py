# ---------------------------------------------------------------------------------------------------------------
# HELPER CONFIG
# Name: config.py
# Desc: Encapsula funciones para configuracion por entorno
# ---------------------------------------------------------------------------------------------------------------

import os
import sys
from functools import reduce

from pyhocon import ConfigFactory

# from .environment import running_in_docker

# from helpers.file_settings import BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__config_args = [arg.split("=")[1] for arg in sys.argv if arg.startswith("--config-path=")]

ALLOWED_ENVS = ['DEV', "BETA", 'PROD']
ENVIRONMENT = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ALLOWED_ENVS else 'DEV'
CONFIG_DIR = __config_args[0] if len(__config_args) > 0 else None

# if the application is running inside docker
# we mount host's ~/app into container's /env to read environment-override.conf


# TODO: this should tell whether we're running in docker or not
# ENV_DIR = "/env" if running_in_docker() else BASE_DIR
ENV_DIR = BASE_DIR


def load_from_argv():
    args = sys.argv
    stripped_args = [arg[2:] for arg in args if arg.startswith('-C')]
    return ConfigFactory.parse_string('\n'.join(stripped_args))


def load_config(env=ENVIRONMENT):
    file_names = filter_existed_files(['{}/environment-override.conf'.format(ENV_DIR)])

    if CONFIG_DIR is not None:
        # If config arg is passed we prefer it
        file_names += filter_existed_files(['{}/environment-{}.conf'.format(CONFIG_DIR, env),
                                            '{}/common.conf'.format(CONFIG_DIR)])

    if "{}/common.conf".format(CONFIG_DIR) not in file_names:
        # We'll search in BASE_DIR as a fallback if there aren't configs in the given directory
        file_names += filter_existed_files(['{}/config/environment-{}.conf'.format(BASE_DIR, env),
                                            '{}/config/common.conf'.format(BASE_DIR)])

    print("######################## CONFIG #########################")
    print("Found config files: {}".format(file_names))
    print("#########################################################")

    assert len(file_names) > 0, "No config files loaded"

    new_conf = reduce(lambda cnf, filename: cnf.with_fallback(filename), file_names, load_from_argv())

    return new_conf


def filter_existed_files(file_names):
    return [i for i in file_names if os.path.lexists(i)]


conf = load_config()

print('Loaded config with Environment: {}'.format(ENVIRONMENT))
