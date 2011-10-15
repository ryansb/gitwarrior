#!/usr/bin/env python
# -*- coding; utf-8 -*-
# Author: Ryan Brown
# Description: Command Line interface for GitWarrior
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


import os
import readline
from gitwarrior import list_issues
from optparse import OptionParser
from ConfigParser import ConfigParser

LIST_SHORTCUTS = ['list', 'li', 'ls']

def read_config(filename=None):
	if not filename: filename = "%s/.gitwarriorrc" % os.getenv("HOME")
	cfg = ConfigParser()
	cfg.read(filename)
	return cfg

if __name__ == "__main__":
	print "Welcome to GitWarrior"
	#parser = OptionParser(version=__version__, usage="%prog [options] config_url")
	parser = OptionParser(version="0.1", usage="%prog [options] config_url")
	parser.add_option("-e", "--edit", help="Opens the issue in your default editor", dest="edit", default=False, action="store_true") #TODO
	parser.add_option("-t", "--tag", help="Tag for the issue", action="append", dest="tags", metavar="key:value") #TODO
	parser.add_option("-c", "--config", help="Specify a config file to load. Defaults to ~/.gitwarriorrc", dest="config", default=None)

	(options, args) = parser.parse_args()

	config = read_config(options.config)

	if args[0] in LIST_SHORTCUTS:
		#deal with list and all its shortcuts
		print "HI LIST"
		try:
			list_issues(args[1])
		except IndexError:
			list_issues(config.get('Projects', 'default'))

	elif args[0] == 'la':
		#deal with the shortcut of list that autolists all
		#list_issues('all')
		pass


