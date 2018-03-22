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

__author__ = 'André William dos Santos Silva'
__date__ = '2018-03-08'
__copyright__ = '(C) 2018 by André William dos Santos Silva'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from processing.core.Processing import Processing
from processing.gui.CommanderWindow import CommanderWindow
from squad_tool_provider import SquadToolProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class SquadToolPlugin:

    def __init__(self, iface):
        self.provider = SquadToolProvider()
        self.iface = iface
        Processing.initialize()

    def initGui(self):
        Processing.addProvider(self.provider)

        self.action = QAction(QIcon(":/plugins/squad-plugin/SQUAD_icon_v2_32x32.png"), "SQUAD plugin", self.iface.mainWindow())
        self.action.setObjectName("squadAction")
        self.action.setWhatsThis("Spatial Quality and Anomalies Diagnosis")
        self.action.setStatusTip("...")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&SQUAD", self.action)


    def unload(self):
        Processing.removeProvider(self.provider)

        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&SQUAD", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        alg = Processing.getAlgorithm("squadtoolbox:squadtool")

        # Instantiate the commander window and open the algorithm's interface 
        cw = CommanderWindow(self.iface.mainWindow(), self.iface.mapCanvas())
        if alg is not None:
            cw.runAlgorithm(alg)