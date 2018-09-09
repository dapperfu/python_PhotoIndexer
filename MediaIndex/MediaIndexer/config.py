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
config["darknet"] = dict()
config["weights"] = dict()

# Read ENV variables for overrides, otherwise use defaults from above.
config["darknet"]["root"] = os.environ.get(
    key="DARKNET_ROOT", default=default_darknet_root
)
config["darknet"]["clone_url"] = os.environ.get(
    key="DARKNET_CLONE_URL", default=default_darknet_clone_url
)
default_darknet_weight_dir = os.path.join(config["darknet"]["root"], "weights")
config["darknet"]["weight_dir"] = os.environ.get(
    key="DARKNET_WEIGHT_DIR", default=default_darknet_weight_dir
)
config["weights"]["url_root"] = os.environ.get(
    key="DARKNET_WEIGHT_URL", default=default_darknet_weight_url
)

