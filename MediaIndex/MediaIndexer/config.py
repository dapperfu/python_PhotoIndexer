"""pydarknet configuration options.

Configuration options for all pydarknet.
"""

import configparser
import os

"""Default values."""
default_darknet_root = os.path.expanduser(os.path.join("~", ".darknet"))
default_darknet_clone_url = "https://github.com/jed-frey/darknet.git"
# default_darknet_weight_url = "https://pjreddie.com/media/files/" #
default_darknet_weight_url = "https://functionalsafety.tech/darknet_weights/"

# Create new config parser.
config = configparser.ConfigParser()

# Setup config sections.
config["MediaIndexer"] = dict()