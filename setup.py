#!/usr/bin/env python
# -*- coding; utf-8 -*-
# Author: Ryan Brown
# Description: easy_install setup file for GitWarrior
#
# Copyright (c) 2011 Ryan Brown ryansb@csh.rit.edu
#
# This software is licensed under the AGPL, see below URL for more information
# about the AGPL.
#
# https://www.gnu.org/licenses/agpl-3.0.html
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from setuptools import setup, find_packages

from gitwarrior import __version__

setup(name = "gitwarrior",
		version = __version__,
		description = "GitWarrior TaskWarrior-Github interface",
		long_description="An application that syncs between Github issues and TaskWarrior tasks",
		author = "Ryan Brown",
		author_email = "ryansb@csh.rit.edu",
		url = "https://",
		packages = find_packages(),
		include_package_data = True,
		package_data = {
			'': ['*.yaml', 'conf/*.yaml']
		},
		scripts = [
			'bin/gw',
		],
		license = 'NONE',
		platforms = 'Posix; MacOS X (maybe?);',
		classifiers = [ 'Development Status :: 3 - Alpha',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Operating System :: OS Independent',
			'Topic :: Internet',
		],
		dependency_links = ['https://github.com/ask/python-github2' ],
		install_requires = [ ],
	)
