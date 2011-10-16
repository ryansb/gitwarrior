#!/usr/bin/env python
# -*- coding; utf-8 -*-
# Author: Ryan Brown
# Description: 
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
from github2.client import Github

class Hub(object):
	def __init__(self, uname, token, default_project):
		self.uname = uname
		self.token = token
		self._connect()
		self.def_proj = "%s/%s" % (uname, default_project)

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
