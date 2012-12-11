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

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import textwrap

from procyon import core

import test_client.message as msg
import test_client.properties


command_accordance = {
    'installed': 'freeze',
    'available': 'cache',
    'outdated': 'outdated',
}

parser = argparse.ArgumentParser(prog='procyon',
    description='Package manager for OSTIS project.',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''Supported commands:
  set <url> - Sets url of repo containing packages.
  update - Updates package list.
  install <packages> - Installs new package.
  remove <packages> - Removes installed package.
  upgrade <packages> - Installs new version of all installed packages.
  search <package> - Searches packages with key word.
  list <list command> - Shows list of specified packages

Supported list commands:
  installed - Shows list of currently installed packages.
  available - Shows list of available to install packages.
  outdated - Shows list of outdated packages.
'''))

parser.add_argument('command', help='command name')
parser.add_argument('parameter', nargs='*', help='command parameter (file url or command name)')

args = parser.parse_args()

try:
    if args.command == 'set':
        if args.parameter:
            result = test_client.properties.set_remote_repo_url(args.parameter[0])
            print(msg.get_repo_setting_status(result))
        else:
            parser.print_help()

    elif args.command == 'update':
        result = core.update()
        print(msg.get_update_status(result))

    elif args.command == 'install':
        if args.parameter:
            result = core.install(args.parameter)
            for package in result:
                print(msg.get_installation_status(package))
        else:
            parser.print_help()

    elif args.command == 'remove':
        if args.parameter:
            result = core.uninstall(args.parameter)
            for package in result:
                print(msg.get_uninstallation_status(package))
        else:
            parser.print_help()

    elif args.command == 'upgrade':
        core.upgrade()

    elif args.command == 'search':
        if args.parameter:
            result = core.search(args.parameter[0])
            if result:
                info = msg.get_package_list_info('available', result)
                for i in info:
                    print(i)
        else:
            parser.print_help()

    elif args.command == 'list':
        if not args.parameter:
            parser.print_help()
        client_command = args.parameter[0]
        core_command = command_accordance.get(client_command)
        if not core_command:
            parser.print_help()
        command = getattr(core, core_command, None)
        result = command()
        if result:
            info = msg.get_available_package_list_info(result)
            for i in info:
                print(i)
    else:
        parser.print_help()

except TypeError:
    parser.print_help()
