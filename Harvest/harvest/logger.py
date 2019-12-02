import logging
import logging.config
import os
import yaml


def setup_logging(default_path, default_level, env_key):
    """ Setup logging configuration """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level, filename='logs.log',
                            format="%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        print('Failed to load configuration file. Using default configs')