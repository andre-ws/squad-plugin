# -*- coding: utf-8 -*-

"""
/***************************************************************************
 SquadPlugin
                                 A QGIS plugin
 Spatial Quality and Anomalies Diagnosis (SQUAD)
                              -------------------
        begin                : 2018-03-06
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
__date__ = '2018-03-06'
__copyright__ = '(C) 2018 by André William dos Santos Silva'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from processing.core.Processing import Processing

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QGis, QgsFeature, QgsGeometry, QgsPoint
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector
from qgis.gui import QgsMessageBar


cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class SquadPluginPlugin:

    def __init__(self, iface):
        self.iface = iface
        Processing.initialize()

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/testplug/icon.png"), "SQUAD plugin", self.iface.mainWindow())
        self.action.setObjectName("squadAction")
        self.action.setWhatsThis("Spatial Quality and Anomalies Diagnosis")
        self.action.setStatusTip("...")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&SQUAD", self.action)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&SQUAD", self.action)
        self.iface.removeToolBarIcon(self.action)
    
    def run(self):
        # create and show a configuration dialog or something similar
        self.iface.messageBar().pushMessage("Success", "Hello world!", level=QgsMessageBar.INFO)