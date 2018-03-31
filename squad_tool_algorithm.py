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

__author__ = 'André William dos Santos Silva'
__date__ = '2018-03-08'
__copyright__ = '(C) 2018 by André William dos Santos Silva'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtCore import QUrl
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsField
from qgis.core import QgsFields
from qgis.core import QgsFeature

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterField,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource)
from processing.tools import dataobjects, vector
from processing.gui.AlgorithmDialog import AlgorithmDialog

import os
from . import resources
from .parameters_dict import parameters_desc
from .squad_analysis import SquadAnalysis

class SquadToolAlgorithm(QgsProcessingAlgorithm):
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

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'SquadTool'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.name()

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.groupId()

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """        
        return 'squad_tool'

    def shortHelpString(self):
        DIRNAME = os.path.dirname(__file__)
        path = os.path.join(DIRNAME, 'help.html')
        with open(path) as f:
            return f.read()

    def helpString(self):
        return 'https://github.com/andre-ws/squad-plugin'

    def getParameterDescriptions(self):
        return parameters_desc

    def initAlgorithm(self, config):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The name that the user will see in the toolbox
        # self.name = 'SQUAD Tool'

        # The branch of the toolbox under which the algorithm will appear
        # self.group = 'Analysis'

        # We add the input vector layer. It can have any kind of geometry
        # It is a mandatory (not optional) one, hence the False argument
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.SITES_LAYER,
            'Site File',
            [QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterField(
            self.SITE_ADMIN_UNIT_FIELD,
            'Site Admin Unit Field',
            '',
            self.SITES_LAYER,
            QgsProcessingParameterField.String))
        self.addParameter(QgsProcessingParameterField(
            self.SITE_LONGITUDE_FIELD,
            'Site Longitude Field',
            '',
            self.SITES_LAYER,
            QgsProcessingParameterField.Numeric))
        self.addParameter(QgsProcessingParameterField(
            self.SITE_LATITUDE_FIELD,
            'Site Latitude Field',
            '',
            self.SITES_LAYER,
            QgsProcessingParameterField.Numeric))
        self.addParameter(QgsProcessingParameterField(
            self.SITE_NAME_FIELD,
            'Site Name Field',
            '',
            self.SITES_LAYER,
            QgsProcessingParameterField.String))
        self.addParameter(QgsProcessingParameterField(
            self.SITE_ID_FIELD,
            'Site ID Field',
            '',
            self.SITES_LAYER,
            QgsProcessingParameterField.String))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.ADMIN_UNITS_LAYER,
            'Administrative Units File',
            [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterField(
            self.ADMIN_UNIT_NAME_FIELD,
            'Admin Unit Name Field',
            '', 
            self.ADMIN_UNITS_LAYER, 
            QgsProcessingParameterField.String))

        # We add a vector layer as output
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_LAYER,
            'Site Anomalies Output'),
            True)

    def createOutputFields(self, baseProvider):
        fields = baseProvider.fields()
        fields.append(QgsField(SquadAnalysis.STR_LONG_FIELD, QVariant.String, len=100))
        fields.append(QgsField(SquadAnalysis.STR_LAT_FIELD, QVariant.String, len=100))
        fields.append(QgsField(SquadAnalysis.STR_ANOMALY_1, QVariant.Int))
        fields.append(QgsField(SquadAnalysis.STR_ANOMALY_2, QVariant.Int))
        fields.append(QgsField(SquadAnalysis.STR_ANOMALY_3, QVariant.Int))
        fields.append(QgsField(SquadAnalysis.STR_ANOMALY_4, QVariant.Int))
        fields.append(QgsField(SquadAnalysis.STR_ANOMALY_5, QVariant.Int))
        fields.append(QgsField(SquadAnalysis.STR_ANOMALY_6, QVariant.Int))
        return fields   

    def processAlgorithm(self, parameters, context, feedback):
        """Here is where the processing itself takes place."""
        # The first thing to do is retrieve the values of the parameters
        # entered by the user
        sitesLayer = self.parameterAsSource(parameters, self.SITES_LAYER, context)
        sitesFieldUnit = self.parameterAsString(parameters, self.SITE_ADMIN_UNIT_FIELD, context)
        sitesFieldLong = self.parameterAsString(parameters, self.SITE_LONGITUDE_FIELD, context)
        sitesFieldLat = self.parameterAsString(parameters, self.SITE_LATITUDE_FIELD, context)
        sitesFieldName = self.parameterAsString(parameters, self.SITE_NAME_FIELD, context)
        sitesFieldId = self.parameterAsString(parameters, self.SITE_ID_FIELD, context)
        adminsLayer = self.parameterAsSource(parameters, self.ADMIN_UNITS_LAYER, context)
        adminsFieldName = self.parameterAsString(parameters, self.ADMIN_UNIT_NAME_FIELD, context)

        # try:
        #     sitesLayer = processing.getObjectFromUri(sitesName)
        # except:
        #     raise QgsProcessingException("Invalid Sites Layer")
        # try:
        #     adminsLayer = processing.getObjectFromUri(adminsName)
        # except:
        #     raise QgsProcessingException("Invalid Administrative Units layer")

        fields = self.createOutputFields(sitesLayer)
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_LAYER,
            context,
            fields,
            sitesLayer.wkbType(),
            sitesLayer.sourceCrs())
        #outputName

        # Input layers values are always a string with its location.
        # That string can be converted into a QGIS object (a
        # QgsVectorLayer in this case) using the
        # processing.getObjectFromUri() method.
        # sitesLayer = dataobjects.getObjectFromUri(sitesName)
        # adminsLayer = dataobjects.getObjectFromUri(adminsName)
        
        # Call functions
        analysis = SquadAnalysis(
            sitesLayer,
            sitesFieldUnit,
            sitesFieldLong,
            sitesFieldLat,
            sitesFieldName,
            sitesFieldId,
            adminsLayer,
            adminsFieldName,
            sink,
            fields)
        analysis.execute(context, feedback)
        return {self.OUTPUT_LAYER: dest_id}

    def createInstance(self):
        return SquadToolAlgorithm()        