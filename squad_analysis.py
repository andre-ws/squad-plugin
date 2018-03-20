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

from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QVariant
from PyQt4 import QtCore
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsField
from qgis.core import QgsFields
from qgis.core import QgsFeature

from qgis.core import *

import processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector
from processing.tools.vector import VectorWriter

class SquadAnalysis:
    TXT_LONG_FIELD = 'Point_X_TXT'
    TXT_LAT_FIELD = 'Point_Y_TXT'
    ANOMALY_1 = "Anomaly_1"
    ANOMALY_2 = "Anomaly_2"
    ANOMALY_3 = "Anomaly_3"
    ANOMALY_4 = "Anomaly_4"
    ANOMALY_5 = "Anomaly_5"
    ANOMALY_6 = "Anomaly_6"

    def __init__(
            self,
            _sitesName,
            _sitesFieldUnit,
            _sitesFieldLong,
            _sitesFieldLat,
            _sitesFieldName,
            _sitesFieldId,
            _adminsName,
            _adminsFieldName,
            _outputName):
        self.sitesName = _sitesName
        self.sitesFieldUnit = _sitesFieldUnit
        self.sitesFieldLong = _sitesFieldLong
        self.sitesFieldLat = _sitesFieldLat
        self.sitesFieldName = _sitesFieldName
        self.sitesFieldId = _sitesFieldId
        self.adminsName = _adminsName
        self.adminsFieldName = _adminsFieldName
        self.outputName = _outputName
        self.sitesLayer = processing.getObjectFromUri(self.sitesName)
        self.adminsLayer = processing.getObjectFromUri(self.adminsName)


    def createOutputFields(self, baseProvider):
        fields = QgsFields(baseProvider.fields())
        fields.append(QgsField(self.TXT_LONG_FIELD, QVariant.String, len=100))
        fields.append(QgsField(self.TXT_LAT_FIELD, QVariant.String, len=100))
        fields.append(QgsField(self.ANOMALY_1, QVariant.Int))
        fields.append(QgsField(self.ANOMALY_2, QVariant.Int))
        fields.append(QgsField(self.ANOMALY_3, QVariant.Int))
        fields.append(QgsField(self.ANOMALY_4, QVariant.Int))
        fields.append(QgsField(self.ANOMALY_5, QVariant.Int))
        fields.append(QgsField(self.ANOMALY_6, QVariant.Int))    
        return fields   

    def checkAccuracy(self, number):
        ok = False
        s = str(number)
        if s.count('.') > 0:
            (size, precision) = s.split('.')
            if len(precision) >= 3:
                ok = True
        return ok

    def findDistrict(self, name):
        exp = QgsExpression("{} = \'{}\'".format(self.adminsFieldName, name))
        request = QgsFeatureRequest(exp)
        return next((f for f in self.adminsLayer.getFeatures(request)), None)

    def execute(self, progress):
        # First we create the output layer. The output value entered by
        # the user is a string containing a filename, so we can use it
        # directly
        sitesProvider = self.sitesLayer.dataProvider()
        outputFields = self.createOutputFields(sitesProvider)

        anomaly1 = set()
        anomaly2 = set()
        anomaly3 = set()
        anomaly4 = set()
        anomaly5 = set()
        anomaly6 = set()

        # Cache
        longLatSet = set()
        nameSet = set()
        features = vector.features(self.sitesLayer)
        for f in features:
            id = f[self.sitesFieldId]
            x = f[self.sitesFieldLong]
            y = f[self.sitesFieldLat]
            if x and y:
                if not (self.checkAccuracy(x) and self.checkAccuracy(y)):
                    anomaly2.add(id)
                else:
                    longLat = str(round(x, 5)) + ',' + str(round(y, 5))
                    if longLat in longLatSet:
                        anomaly3.add(longLat)
                    else:
                        longLatSet.add(longLat)
            else:
                anomaly1.add(id)
            name = f[self.sitesFieldName]
            if name in nameSet:
                anomaly4.add(name)
            else:
                nameSet.add(name)

            districtName = f[self.sitesFieldUnit]
            district = self.findDistrict(districtName)
            if district:
                if not f.geometry().within(district.geometry()):
                    results = district.geometry().closestSegmentWithContext(f.geometry().asPoint())
                    (sqrDist, minDistPoint, afterVertex) = results
                    distance = QgsDistanceArea()
                    crs = QgsCoordinateReferenceSystem()
                    crs.createFromSrsId(4326)
                    distance.setSourceCrs(crs)
                    distance.setEllipsoidalMode(True)
                    distance.setEllipsoid('WGS84')
                    m = distance.measureLine(f.geometry().asPoint(), minDistPoint) 
                    if m <= 2000:
                        anomaly5.add(id)
                    else:
                        anomaly6.add(id)

        # Output layer
        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        writer = processing.VectorWriter(
            self.outputName,
            systemEncoding,
            outputFields,
            sitesProvider.geometryType(),
            sitesProvider.crs())

        features = vector.features(self.sitesLayer)
        for f in features:
            id = f[self.sitesFieldId]
            x = f[self.sitesFieldLong]
            y = f[self.sitesFieldLat]
            if x and y:
                longLat = str(round(x, 5)) + ',' + str(round(y, 5))
            name = f[self.sitesFieldName]
            newFeature = QgsFeature(outputFields)
            newFeature.setGeometry(f.geometry())
            columns = f.fields()
            for c in columns:
                value = f[c.name()]
                newFeature[c.name()] = value

            txtLong = f[self.sitesFieldLong]
            txtLat = f[self.sitesFieldLat]
            newFeature[self.TXT_LONG_FIELD] = txtLong
            newFeature[self.TXT_LAT_FIELD] = txtLat

            if id in anomaly1:
                newFeature[self.ANOMALY_1] = 1
            elif id in anomaly2:
                newFeature[self.ANOMALY_2] = 1
            elif longLat in anomaly3:
                newFeature[self.ANOMALY_3] = 1
            elif name in anomaly4:
                newFeature[self.ANOMALY_4] = 1
            elif id in anomaly5:
                newFeature[self.ANOMALY_5] = 1
            elif id in anomaly6:
                newFeature[self.ANOMALY_6] = 1

            # Now we take the features from input layer and add them to the
            # output. Method features() returns an iterator, considering the
            # selection that might exist in layer and the configuration that
            # indicates should algorithm use only selected features or all
            # of them
            writer.addFeature(newFeature)
            # progress.setText(str(ok))
        del writer

        # There is nothing more to do here. We do not have to open the
        # layer that we have created. The framework will take care of
        # that, or will handle it if this algorithm is executed within
        # a complex model