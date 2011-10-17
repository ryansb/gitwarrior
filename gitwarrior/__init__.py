#!/usr/bin/env python
# -*- coding; utf-8 -*-
# Author: Ryan Brown
# Description: Module that does all the work for the gw frontend command as
# well as all the pushing to TaskWarrior
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
# OUT OF OR IN conn WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

__version__ = "0.1"
import os
import tempfile
from subprocess import call
from operator import attrgetter
from github2.client import Github
from ConfigParser import ConfigParser

ISSUE_FILE_CONTENT = """[Issue]
Title = {title}
Body  = {body}
"""

HEADERS = {
    'ID': {'get': attrgetter('number'), 'length':4},
    'State': {'get': attrgetter('state'), 'length':7},
    'Title': {'get': attrgetter('title'), 'length':32},
    'Body': {'get': attrgetter('body'), 'length':50},
    'User': {'get': attrgetter('user'), 'length':15},
    'Votes': {'get': attrgetter('votes'), 'length':5},
}

def format_issue(issue, headers=('ID', 'State', 'Title', 'Body')):
	"""Description: Returns a string of formatted output

	Can pass in either a list of Issue objects or a single Issue

	headers is a tuple of the headers for the formatted output
	They are printed in order, options are:
		ID, State, Title, Body, User, Votes
	"""
	ret = ""
	formatter_string = ''

	if not isinstance(issue, list):
		issue = [issue]

	for h in headers:
		formatter_string += "%%-%ds" % HEADERS[h]['length']
	ret += formatter_string % headers
	ret += '\n'
	ret += "-" * len(formatter_string % headers)
	ret += '\n'

	for i in issue:
		ret_list = []
		for h in headers:
			t = unicode(HEADERS[h]['get'](i)) + ''
			if len(t) > HEADERS[h]['length']:
				t = t[:HEADERS[h]['length']-3] + '...'
			ret_list.append(t)
		ret += (formatter_string % tuple(ret_list)) + '\n'
	return ret

class Hub(object):
	def __init__(self, config):
		self.uname = config.get('Credentials', 'username')
		self.token = config.get('Credentials', 'token')
		self._connect()
		self.def_proj = "%s/%s" % (self.uname, config.get('Defaults', 'project'))
		self.config = config

	@property
	def gh(self):
		if self._gh is None:
			self._connect
		return self._gh

	def _connect(self):
		self._gh = Github(self.uname, self.token)

	def list_issues(self, opt, user=None):
		"""Description:
			:param opt: Option passed in, can be 'all' or the name of a project
			:type str:

			:param user: The user who owns the project, defaults to the username
								on the connection
			:type str:

			:rtype: ilist: List of Issues for that project
			:return: list
		"""
		if not user:
			user = self.uname
		ilist = []
		if opt == 'all':
			#list all issues
			for p in self.gh.repos.list(self.uname):
				if p.has_issues:
					l = self.list_issues(p.name)
					if l:
						ilist.extend(l)
		else:
			#list issues on a specific project
			ilist.extend(self.gh.issues.list("%s/%s" % (user, opt)))
		if len(ilist) > 0:
			return ilist
		return None

	def get_issue(self, id, opt=None):
		if not opt: opt = self.def_proj
		if len(opt.split('/')) < 1:
			opt = "%s/%s" % (self.uname, opt)

		return self.gh.issues.show(opt, id)

	def edit(self, id, opt=None):
		issue = self.get_issue(id, opt)
		(fh, name) = tempfile.mkstemp(prefix='gw-edit-', suffix='.txt', text=True)
		f = open(name, 'w')
		f.write(ISSUE_FILE_CONTENT.format(title=issue.title, body=issue.body))
		f.close()
		call([self.get_editor(), name])
		f = open(name, 'r')
		alterations = ConfigParser()
		alterations.readfp(f)
		f.close()
		self.gh.issues.edit(id, opt, alterations.get('Issue', 'Title'), alterations.get('Issue', 'Body'))
		return "Issue %s now has:\nTitle: %s\nBody: %s" % (id,
				alterations.get('Issue', 'Title'), alterations.get('Issue',
					'Body'))

	def new(self, title, body, opt=None):
		if not opt: opt = self.def_proj
		elif len(opt.split('/')) < 1:
			opt = "%s/%s" % (self.uname, opt)
		i = self.gh.issues.open(opt, title, body)
		return (i.number, opt)

	def get_editor(self):
		return (self.config.get('Defaults', 'editor') or os.environ.get('EDITOR')
				or 'vi')

	def status(self, id, opt=None, action=None):
		if not opt: opt = self.def_proj
		elif len(opt.split('/')) < 1:
			opt = "%s/%s" % (self.uname, opt)

		if not action:
			return self.gh.issues.show(opt, id)
		if action.lower() in ['open', 'o', 'op']:
			self.gh.issues.reopen(opt, id)
		elif action.lower() in ['close', 'c', 'cl']:
			self.gh.issues.close(opt, id)

		return self.gh.issues.show(opt, id)

	def add_comment(self, id, body, opt=None):
		if not opt: opt = self.def_proj
		elif len(opt.split('/')) < 1:
			opt = "%s/%s" % (self.uname, opt)

		self.gh.issues.comment(opt, id, body)
		return "Added comment successfully"

	def show_comments(self, id, opt=None):
		if not opt: opt = self.def_proj
		elif len(opt.split('/')) < 1:
			opt = "%s/%s" % (self.uname, opt)

		return self.gh.issues.comments(opt, id)
