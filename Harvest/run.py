#!/usr/bin/env python
import argparse
import configparser
import os
from harvest import main

parser = argparse.ArgumentParser()
config = configparser.ConfigParser()
parser.add_argument("url", nargs='?', help="The url you want your harvest to occur", type=str)
args = parser.parse_args()
if args.url is None:
    path = os.path.dirname(__file__)
    config.read(os.path.join(path, 'setup.ini'))
    # using the default arguments from setup.ini
    main.main(config['arguments']['url'])
else:
    main.main(args.url)



