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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'André William dos Santos Silva'
__date__ = '2018-03-06'
__copyright__ = '(C) 2018 by André William dos Santos Silva'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SquadPlugin class from file SquadPlugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .squad_plugin import SquadPluginPlugin
    return SquadPluginPlugin(iface)
