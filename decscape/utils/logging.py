import yaml
import logging
import logging.config
from pathlib import Path

def configure_logging():
    conf_path = str(Path(__file__).parent.joinpath('logging.yaml').resolve())
    try:
        # load config from .yaml
        with open(conf_path, 'r') as fp:
            env = yaml.safe_load(fp)
        logging.config.dictConfig(env)  # type: ignore
        logging.info('Configuring logger using dict config')
    except yaml.YAMLError:
        logging.exception("Failed to open logging config file due to yaml parse error")
    except FileNotFoundError:
        logging.exception(
            "Logging config file not found in expected absolute path: {}".format(conf_path))
    else:
        logging.info("Logging configuration successful.")
