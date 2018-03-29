# -*- coding: utf-8 -*-

"""
/***************************************************************************
 SquadTool
                                 A QGIS plugin
 Spatial Quality and Anomalies Diagnosis
                              -------------------
        begin                : 2018-03-08
        copyright            : (C) 2018 by André William dos Santos Silva
        email                : wss.andre@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import

from builtins import object
__author__ = 'André William dos Santos Silva'
__date__ = '2018-03-08'
__copyright__ = '(C) 2018 by André William dos Santos Silva'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from processing import Processing
from processing.gui.AlgorithmDialog import AlgorithmDialog
from qgis.core import QgsApplication
from qgis.core import QgsProcessingException
from .squad_tool_provider import SquadToolProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class SquadToolPlugin(object):

    def __init__(self, iface):
        self.provider = SquadToolProvider()
        self.iface = iface
        # Processing.initialize()
        
        self.actions = []
        self.menu = '&SQUAD'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SquadTool')
        self.toolbar.setObjectName(u'SquadTool')

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action        

    def initGui(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

        icon_path = ":/plugins/squad-plugin/SQUAD_icon_v2_32x32.png"
        self.add_action(
            icon_path,
            text='SQUAD',
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # self.action.setObjectName("squadAction")
        # self.action.setWhatsThis("Spatial Quality and Anomalies Diagnosis")
        # self.action.setStatusTip("...")
        # self.action.triggered.connect(self.run)

        # # add toolbar button and menu item
        # self.iface.addToolBarIcon(self.action)
        # self.iface.addPluginToMenu("&SQUAD", self.action)


    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                '&SQUAD',
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        # remove the plugin menu item and icon
        # self.iface.removePluginMenu("&SQUAD", self.action)
        # self.iface.removeToolBarIcon(self.action)

    def run(self):
        # alg = Processing.getAlgorithm("squadtoolbox:squadtool")
        alg = QgsApplication.processingRegistry().algorithmById('squad:SquadTool')
        # Instantiate the commander window and open the algorithm's interface 
        # cw = CommanderWindow(self.iface.mainWindow(), self.iface.mapCanvas())
        if alg is not None:
            dlg = AlgorithmDialog(alg)
            # cw.runAlgorithm(alg)
            dlg.show()
        else:
            raise QgsProcessingException('Algorithm Provider not found')