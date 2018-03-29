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

from qgis.core import QgsProcessingProvider
# from processing.core.ProcessingConfig import Setting, ProcessingConfig
from .squad_tool_algorithm import SquadToolAlgorithm


class SquadToolProvider(QgsProcessingProvider):

    # MY_DUMMY_SETTING = 'MY_DUMMY_SETTING'

    def __init__(self):
        QgsProcessingProvider.__init__(self)

        # Deactivate provider by default
        self.activate = False

        # Load algorithms
        self.alglist = [SquadToolAlgorithm()]

    def initializeSettings(self):
        """In this method we add settings needed to configure our
        provider.

        Do not forget to call the parent method, since it takes care
        or automatically adding a setting for activating or
        deactivating the algorithms in the provider.
        """
        # AlgorithmProvider.initializeSettings(self)
        # ProcessingConfig.addSetting(Setting('Example algorithms',
        #     SquadToolProvider.MY_DUMMY_SETTING,
        #     'Example setting', 'Default value'))

    def unload(self):
        """Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded.
        """
        # AlgorithmProvider.unload(self)
        # ProcessingConfig.removeSetting(
        #     SquadToolProvider.MY_DUMMY_SETTING)
        pass

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'squad'        

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return 'SquadTool'

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()        

    # def icon(self):
        """We return the default icon.
        """
        # return AlgorithmProvider.getIcon(self)

    def loadAlgorithms(self):
        """Here we fill the list of algorithms in self.algs.

        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here.

        In this case, since the list is always the same, we assign from
        the pre-made list. This assignment has to be done in this method
        even if the list does not change, since the self.algs list is
        cleared before calling this method.
        """
        for alg in self.alglist:
            self.addAlgorithm( alg )
