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

from builtins import str
from builtins import object
__author__ = 'André William dos Santos Silva'
__date__ = '2018-03-08'
__copyright__ = '(C) 2018 by André William dos Santos Silva'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt import QtCore
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsField
from qgis.core import QgsFields
from qgis.core import QgsFeature
from qgis.core import QgsProcessingException

from qgis.core import *

import processing
from processing.tools import dataobjects, vector

class SquadAnalysis(object):
    STR_ANOMALY_1 = "Anomaly_1"
    STR_ANOMALY_2 = "Anomaly_2"
    STR_ANOMALY_3 = "Anomaly_3"
    STR_ANOMALY_4 = "Anomaly_4"
    STR_ANOMALY_5 = "Anomaly_5"
    STR_ANOMALY_6 = "Anomaly_6"

    def __init__(
            self,
            sitesLayer_,
            sitesFieldUnit_,
            sitesFieldLong_,
            sitesFieldLat_,
            sitesFieldName_,
            sitesFieldId_,
            adminsLayer_,
            adminsFieldName_,
            sink_,
            fields_):
        self.sitesLayer = sitesLayer_
        self.sitesFieldUnit = sitesFieldUnit_
        self.sitesFieldLong = sitesFieldLong_
        self.sitesFieldLat = sitesFieldLat_
        self.sitesFieldName = sitesFieldName_
        self.sitesFieldId = sitesFieldId_
        self.adminsLayer = adminsLayer_
        self.adminsFieldName = adminsFieldName_
        self.sink = sink_
        self.fields = fields_
        

        self.anomalies1 = set()
        self.anomalies2 = set()
        self.anomalies3 = set()
        self.anomalies4 = set()
        self.anomalies5 = set()
        self.anomalies6 = set()

        self.longLatSet = set()
        self.nameSet = set()

    def checkAccuracy(self, number):
        ok = False
        s = str(number)
        if s.count('.') > 0:
            (size, precision) = s.split('.')
            if len(precision) >= 3:
                ok = True
        return ok

    def findDistrict(self, name):
        districts = []
        exp = QgsExpression("{} = \'{}\'".format(self.adminsFieldName, name))
        request = QgsFeatureRequest(exp)
        request.setInvalidGeometryCheck(QgsFeatureRequest.GeometrySkipInvalid)
        for d in self.adminsLayer.getFeatures(request):
            districts.append(d)
        return districts

    def checkAnomalies(self):
        i = 0
        count = self.sitesLayer.featureCount()        
        features = self.sitesLayer.getFeatures()
        for f in features:
            id = f[self.sitesFieldId]
            x = f[self.sitesFieldLong]
            y = f[self.sitesFieldLat]
            if x and y:
                if not (self.checkAccuracy(x) and self.checkAccuracy(y)):
                    self.anomalies2.add(id)
                longLat = str(round(x, 5)) + ',' + str(round(y, 5))
                if longLat in self.longLatSet:
                    self.anomalies3.add(longLat)
                else:
                    self.longLatSet.add(longLat)
            else:
                self.anomalies1.add(id)
            name = f[self.sitesFieldName]
            if name in self.nameSet:
                self.anomalies4.add(name)
            else:
                self.nameSet.add(name)

            districtName = f[self.sitesFieldUnit]
            districts = self.findDistrict(districtName)
            found = len(districts)
            if found == 0:
                self.anomalies6.add(id)
            elif found > 1:
                error = "Multiple District \'" + districtName + "\' in Admin file"
                raise QgsProcessingException(error)
            elif found == 1:
                if f.hasGeometry() and districts[0].hasGeometry():
                    if not f.geometry().within(districts[0].geometry()):
                        results = districts[0].geometry().closestSegmentWithContext(f.geometry().asPoint())
                        (sqrDist, minDistPoint, afterVertex, _) = results
                        distance = QgsDistanceArea()
                        crs = QgsCoordinateReferenceSystem()
                        crs.createFromSrsId(4326)
                        distance.setSourceCrs(crs, self.context.transformContext())
                        distance.setEllipsoid('WGS84')
                        m = distance.measureLine(f.geometry().asPoint(), minDistPoint)
                        if m <= 2000:
                            self.anomalies5.add(id)
                        else:
                            self.anomalies6.add(id)

            i = i + 1
            percent = ((i/float(count)) * 50)
            self.feedback.setProgress(percent)

    def writeOutput(self):
        i = 0
        count = self.sitesLayer.featureCount()
        features = self.sitesLayer.getFeatures()
        for f in features:
            id = f[self.sitesFieldId]
            x = f[self.sitesFieldLong]
            y = f[self.sitesFieldLat]
            if x and y:
                longLat = str(round(x, 5)) + ',' + str(round(y, 5))
            name = f[self.sitesFieldName]
            newFeature = QgsFeature(self.fields)
            newFeature.setGeometry(f.geometry())
            columns = f.fields()
            for c in columns:
                value = f[c.name()]
                newFeature[c.name()] = value

            if id in self.anomalies1:
                newFeature[self.STR_ANOMALY_1] = 1
            elif id in self.anomalies2:
                newFeature[self.STR_ANOMALY_2] = 1
            if longLat in self.anomalies3:
                newFeature[self.STR_ANOMALY_3] = 1
            if name in self.anomalies4:
                newFeature[self.STR_ANOMALY_4] = 1
            if id in self.anomalies5:
                newFeature[self.STR_ANOMALY_5] = 1
            if id in self.anomalies6:
                newFeature[self.STR_ANOMALY_6] = 1

            # Now we take the features from input layer and add them to the
            # output. Method features() returns an iterator, considering the
            # selection that might exist in layer and the configuration that
            # indicates should algorithm use only selected features or all
            # of them
            self.sink.addFeature(newFeature, QgsFeatureSink.FastInsert)
            i = i + 1
            percent = ((i/float(count)) * 50) + 50
            self.feedback.setProgress(percent)

    def execute(self, context, feedback):
        self.context = context
        self.feedback = feedback
        self.feedback.setProgressText('Checking for anomalies...')
        self.checkAnomalies()
        self.feedback.setProgressText('Saving results...')
        self.writeOutput()
        self.feedback.setProgressText('Done!')

        # There is nothing more to do here. We do not have to open the
        # layer that we have created. The framework will take care of
        # that, or will handle it if this algorithm is executed within
        # a complex model