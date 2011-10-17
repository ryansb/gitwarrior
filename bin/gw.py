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
from gitwarrior import Hub
from gitwarrior import __version__
from optparse import OptionParser
from gitwarrior import format_issue
from ConfigParser import ConfigParser

SHORTCUTS = {
	'list':     ['list', 'li', 'ls'],
	'edit':     ['edit', 'ed', 'e'],
	'status':   ['status', 'st', 'stat']
}

DOCS = {
	'list':     "List open issues, args: [ all | project name ]",
	'edit':     "Edit the title or body of an issue. Opens the issue in default editor, or vi if it can't find a default editor",
	'status':   "Check the status [ Open | Closed ] and alter it by giving a new status [ (open,op,o) | (closed, cl, c) ]"
}

def read_config(filename=None):
	if not filename: filename = "%s/.gitwarriorrc" % os.getenv("HOME")
	cfg = ConfigParser()
	cfg.read(filename)
	return cfg

if __name__ == "__main__":
	parser = OptionParser(version=__version__, usage="%prog [options] config_url")
	parser.add_option("-e", "--edit", help="Opens the issue in your default editor", dest="edit", default=False, action="store_true") #TODO
	parser.add_option("-t", "--tag", help="Tag for the issue", action="append", dest="tags", metavar="key:value") #TODO
	parser.add_option("-c", "--config", help="Specify a config file to load. Defaults to ~/.gitwarriorrc", dest="config", default=None)
	parser.add_option("-H", "--headers", help="Specify headers to use as a comma-separated list. [ ID | Title | State | Body | User | Votes ]", dest="headers", default="ID,State,Title,Body")
	parser.add_option("-p", "--project", help="Specify name of project, either as 'projectname' or 'user/projectname'", dest="project", default=None)


	(options, args) = parser.parse_args()

	config = read_config(options.config)

	hub = Hub(config)

	if args[0] in SHORTCUTS['list']:
		#deal with list and all its shortcuts
		try:
			print format_issue(hub.list_issues(args[1]), tuple(options.headers.split(',')))
		except IndexError:
			print format_issue(hub.list_issues(config.get('Defaults', 'project')), tuple(options.headers.split(',')))

	elif args[0] == 'la':
		#deal with the shortcut of list that autolists all
		print format_issue(hub.list_issues('all'), tuple(options.headers.split(',')))

	elif args[0] in SHORTCUTS['edit']:
		print hub.edit(args[1], options.project)
	
	elif args[0] in SHORTCUTS['status']:
		try:
			print format_issue(hub.status(args[1], options.project, args[2]), tuple(options.headers.split(',')))
		except IndexError:
			print format_issue(hub.status(args[1], options.project), tuple(options.headers.split(',')))
	elif args[0] in ['help', 'h']:
		for c, d in DOCS.items():
			print "  %s:\n\t\t%s" % (c, d)

