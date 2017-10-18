#!/usr/bin/env python

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://lucas.bourneuf.net'
RELATIVE_URLS = False
FEED_ATOM = 'feeds/atom.xml'
DELETE_OUTPUT_DIRECTORY = False
PIWIK = True  # not used as url holder, but uniquely as enable/disable piwik
