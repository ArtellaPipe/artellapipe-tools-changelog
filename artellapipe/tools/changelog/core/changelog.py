#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that shows generic changelog for Artella project
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import artellapipe

# Defines ID of the tool
TOOL_ID = 'artellapipe-tools-changelog'

# We skip the reloading of this module when launching the tool
no_reload = True


class ChangelogTool(artellapipe.Tool, object):
    def __init__(self, *args, **kwargs):
        super(ChangelogTool, self).__init__(*args, **kwargs)


class ChangelogToolset(artellapipe.Toolset, object):
    ID = TOOL_ID

    def __init__(self, *args, **kwargs):
        super(ChangelogToolset, self).__init__(*args, **kwargs)

    def contents(self):

        from artellapipe.tools.changelog.widgets import changelog

        changelog_widget = changelog.ArtellaChangelog(
            project=self._project, config=self._config, settings=self._settings, parent=self)
        return [changelog_widget]
