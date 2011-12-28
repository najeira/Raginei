﻿# -*- coding: utf-8 -*-

import os
import sys

lib_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lib')
if lib_path not in sys.path:
  sys.path.insert(0, lib_path)

from raginei.testutil import get_base

GaeTestCase = get_base(r'C:\software\dev\google_appengine')
