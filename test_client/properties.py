#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Procyon <https://github.com/Gr1N/procyon>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import json
from urlparse import urlparse

from procyon import settings as procyon_settings

__all__ = (
    'set_remote_repo_url',
)

def set_remote_repo_url(url):
    allowed_schemes = (
        'http',
        'https',
    )
    parse_result = urlparse(url)
    if not parse_result.scheme in allowed_schemes:
        return (False, 'Only http/https allowed')
    if not parse_result.path.endswith('.git'):
        return (False, 'Only git repositories allowed')
    
    settings_path = os.path.join(procyon_settings['PROCYON_PATH'], 'settings.json')
    f = open(settings_path, 'r')
    try:
        settings_from_file = json.load(f)
        f.close()
    except ValueError as e:
        raise e
    settings_from_file['REMOTE_REPO'] = url
    f = open(settings_path, 'w')
    json.dump(settings_from_file, f)
    f.close()

    return (True, '')