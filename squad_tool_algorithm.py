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

from PyQt4 import QtCore
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import QUrl
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsField
from qgis.core import QgsFields
from qgis.core import QgsFeature

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector

import os
import resources
from parameters_dict import parameters_desc
from squad_analysis import SquadAnalysis

class SquadToolAlgorithm(GeoAlgorithm):
    """This is an example algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the GeoAlgorithm class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    SITES_LAYER = 'SITES_LAYER'
    SITE_ADMIN_UNIT_FIELD = 'SITE_ADMIN_UNIT_FIELD'
    SITE_LONGITUDE_FIELD = 'SITE_LONGITUDE_FIELD'
    SITE_LATITUDE_FIELD = 'SITE_LATITUDE_FIELD'
    SITE_NAME_FIELD = 'SITE_NAME_FIELD'
    SITE_ID_FIELD = 'SITE_ID_FIELD'
    ADMIN_UNITS_LAYER = 'ADMIN_UNITS_LAYER'
    ADMIN_UNIT_NAME_FIELD = 'ADMIN_UNIT_NAME_FIELD'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def shortHelp(self):
        DIRNAME = os.path.dirname(__file__)
        path = os.path.join(DIRNAME, 'help.html')
        if os.path.exists(path):
            return open(path).read()

    def getParameterDescriptions(self):
        return parameters_desc

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The name that the user will see in the toolbox
        self.name = 'SQUAD Tool'

        # The branch of the toolbox under which the algorithm will appear
        self.group = 'Analysis'

        # We add the input vector layer. It can have any kind of geometry
        # It is a mandatory (not optional) one, hence the False argument
        self.addParameter(ParameterVector(self.SITES_LAYER,
            self.tr('Site File'), [ParameterVector.VECTOR_TYPE_ANY], False))
        self.addParameter(ParameterTableField(self.SITE_ADMIN_UNIT_FIELD,
            self.tr('Site Admin Unit Field'), self.SITES_LAYER, ParameterTableField.DATA_TYPE_ANY, False))
        self.addParameter(ParameterTableField(self.SITE_LONGITUDE_FIELD,
            self.tr('Site Longitude Field'), self.SITES_LAYER, ParameterTableField.DATA_TYPE_ANY, False))
        self.addParameter(ParameterTableField(self.SITE_LATITUDE_FIELD,
            self.tr('Site Latitude Field'), self.SITES_LAYER, ParameterTableField.DATA_TYPE_ANY, False))
        self.addParameter(ParameterTableField(self.SITE_NAME_FIELD,
            self.tr('Site Name Field'), self.SITES_LAYER, ParameterTableField.DATA_TYPE_ANY, False))
        self.addParameter(ParameterTableField(self.SITE_ID_FIELD,
            self.tr('Site ID Field'), self.SITES_LAYER, ParameterTableField.DATA_TYPE_ANY, False))
        self.addParameter(ParameterVector(self.ADMIN_UNITS_LAYER,
            self.tr('Administrative Units File'), [ParameterVector.VECTOR_TYPE_ANY], False))
        self.addParameter(ParameterTableField(self.ADMIN_UNIT_NAME_FIELD,
            self.tr('Admin Unit Name Field'), self.ADMIN_UNITS_LAYER, ParameterTableField.DATA_TYPE_ANY, False))

        # We add a vector layer as output
        self.addOutput(OutputVector(self.OUTPUT_LAYER,
            self.tr('Site Anomalies Output')))

    def processAlgorithm(self, progress):
        """Here is where the processing itself takes place."""

        # The first thing to do is retrieve the values of the parameters
        # entered by the user
        sitesName = self.getParameterValue(self.SITES_LAYER)
        sitesFieldUnit = self.getParameterValue(self.SITE_ADMIN_UNIT_FIELD)
        sitesFieldLong = self.getParameterValue(self.SITE_LONGITUDE_FIELD)
        sitesFieldLat = self.getParameterValue(self.SITE_LATITUDE_FIELD)
        sitesFieldName = self.getParameterValue(self.SITE_NAME_FIELD)
        sitesFieldId = self.getParameterValue(self.SITE_ID_FIELD)
        adminsName = self.getParameterValue(self.ADMIN_UNITS_LAYER)
        adminsFieldName = self.getParameterValue(self.ADMIN_UNIT_NAME_FIELD)
        outputName = self.getOutputValue(self.OUTPUT_LAYER)
        
        # Input layers values are always a string with its location.
        # That string can be converted into a QGIS object (a
        # QgsVectorLayer in this case) using the
        # processing.getObjectFromUri() method.
        # sitesLayer = dataobjects.getObjectFromUri(sitesName)
        # adminsLayer = dataobjects.getObjectFromUri(adminsName)
        
        # Call functions
        analysis = SquadAnalysis(
            sitesName,
            sitesFieldUnit,
            sitesFieldLong,
            sitesFieldLat,
            sitesFieldName,
            sitesFieldId,
            adminsName,
            adminsFieldName,
            outputName)
        analysis.execute(progress)