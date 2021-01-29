#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that shows generic changelog for Artella project
"""

from __future__ import print_function, division, absolute_import

from artellapipe.core import tool


class ChangelogToolset(tool.ArtellaToolset, object):
    def __init__(self, *args, **kwargs):
        super(ChangelogToolset, self).__init__(*args, **kwargs)

    def contents(self):

        from artellapipe.tools.changelog.core import view

        changelog_widget = view.ChangelogView(
            project=self._project, config=self._config, settings=self._settings, parent=self)
        return [changelog_widget]
