#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that shows generic changelog for Artella project
"""

from __future__ import print_function, division, absolute_import

import os
import sys

from artellapipe.core import tool

from artellapipe.tools.changelog.core import consts, toolset


class ChangelogTool(tool.ArtellaTool, object):

    ID = consts.TOOL_ID
    TOOLSET_CLASS = toolset.ChangelogToolset

    def __init__(self, *args, **kwargs):
        super(ChangelogTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.ArtellaTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Changelog',
            'id': cls.ID,
            'logo': 'changelog_logo',
            'icon': 'document',
            'tooltip': 'Tool that shows changelog of the different versions',
            'tags': ['changelog'],
            'sentry_id': 'https://780f09885fe84358a3d54f5f475a82fc@sentry.io/1764084',
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Changelog', 'load_on_startup': False, 'color': '', 'background_color': ''}
        }
        base_tool_config.update(tool_config)

        return base_tool_config


if __name__ == '__main__':
    import tpDcc.loader
    import solstice.loader
    from artellapipe.managers import tools

    tool_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    if tool_path not in sys.path:
        sys.path.append(tool_path)

    tpDcc.loader.init(dev=True)
    solstice.loader.init(dev=True)
    tools.run_tool(ChangelogTool.ID, project_name='solstice')
