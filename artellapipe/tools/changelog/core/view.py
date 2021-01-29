#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains artellapipe-tools-changelog view implementation
"""

from __future__ import print_function, division, absolute_import

import os
import json
import logging
from collections import OrderedDict
from distutils.version import LooseVersion

import yaml
import yamlordereddictloader

from Qt.QtCore import Qt
from Qt.QtWidgets import QSizePolicy, QWidget, QScrollArea

from tpDcc.libs.qt.widgets import layouts, accordion, buttons, label

from artellapipe.core import tool

from artellapipe.tools.changelog.core import consts

logger = logging.getLogger(consts.TOOL_ID)


class ChangelogView(tool.ArtellaToolWidget, object):
    def __init__(self, project, config, settings, parent):
        super(ChangelogView, self).__init__(project=project, config=config, settings=settings, parent=parent)

        self._load_changelog()

    def ui(self):
        super(ChangelogView, self).ui()

        scroll_layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))
        scroll_layout.setAlignment(Qt.AlignTop)
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setFocusPolicy(Qt.NoFocus)
        ok_btn = buttons.BaseButton('OK', parent=self)
        ok_btn.setMinimumHeight(30)
        ok_btn.setStyleSheet("""
                border-bottom-left-radius: 5;
                border-bottom-right-radius: 5;
                background-color: rgb(50, 50, 50);
                """)
        ok_btn.clicked.connect(self.close_tool_attacher)
        self.main_layout.addWidget(scroll)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(ok_btn)
        scroll.setWidget(central_widget)
        central_widget.setLayout(scroll_layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.main_layout = scroll_layout

        # ===========================================================================================

        self.version_accordion = accordion.AccordionWidget(parent=self)
        self.version_accordion.rollout_style = accordion.AccordionStyle.MAYA
        self.main_layout.addWidget(self.version_accordion)

    def _load_changelog(self):
        """
        Internal function that lads current changelog file for the project
        """

        changelog_json_file = self._project.get_changelog_path()
        if not os.path.isfile(changelog_json_file):
            logger.warning('Changelog File "{}" does not exists!'.format(changelog_json_file))
            return

        logger.warning('Loading Changelog from: "{}"'.format(changelog_json_file))

        with open(changelog_json_file, 'r') as f:
            if changelog_json_file.endswith('.json'):
                changelog_data = json.load(f, object_pairs_hook=OrderedDict)
            else:
                changelog_data = yaml.load(f, Loader=yamlordereddictloader.Loader)
        if not changelog_data:
            return

        changelog_versions = [key for key in changelog_data.keys()]
        ordered_versions = self._order_changelog_versions(changelog_versions)

        for version in reversed(ordered_versions):
            self._create_version(str(version), changelog_data[str(version)])

        last_version_item = self.version_accordion.item_at(0)
        last_version_item.set_collapsed(False)

    def _order_changelog_versions(self, versions):
        """
        Returns an ordered list of versions
        :param versions:
        :return:
        """

        return sorted(versions, key=LooseVersion)

    def _create_version(self, version, elements):
        """
        Internal function that creates new version widget
        :param version: str
        :param elements: str
        """

        version_widget = QWidget()
        version_layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))
        version_layout.setAlignment(Qt.AlignTop)
        version_widget.setLayout(version_layout)
        self.version_accordion.add_item(version, version_widget, collapsed=True)

        version_label = label.BaseLabel(parent=self)
        version_layout.addWidget(version_label)
        version_text = ''
        for item in elements:
            version_text += '- {}\n'.format(item)
        version_label.setText(version_text)
