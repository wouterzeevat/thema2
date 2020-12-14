import logging
from pypovray import config

# Default configuration file located in the project root
DEFAULT_CONFIG = 'default.ini'
# Create a SETTINGS object containing all the settings as attributes.
# Use as SETTINGS.Quality, SETTINGS.MovieFPS, etc.
SETTINGS = config.Config(DEFAULT_CONFIG)

# Setup logging, reading log-level from the configuration file
logging.basicConfig(level=logging._nameToLevel[SETTINGS.LogLevel])
logger = logging.getLogger(__name__)

logger.info(' Using config file "%s"', DEFAULT_CONFIG)


def load_config(config_file):
    logger.info(' Loading config file "%s"', config_file)
    return config.Config(config_file)