# -*- coding: utf-8 -*-/
"""
/***************************************************************************
TnT_communicate
                                 A QGIS plugin
 test de nouveau plugin
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-01-25
        git sha              : $Format:%H$
        copyright            : (C) 2021 by IGN
        email                : yann.le-borgne@ign.fr
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
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

class TnTcommunicate(QtCore.QObject):
    
    closeAdditionalView=pyqtSignal()
    
    lockAssociatedButton=pyqtSignal()
    unLockAssociatedButton=pyqtSignal()
    
    infoTextSignal=pyqtSignal()
    
    #Slider re init
    sliderInitValue=pyqtSignal()
    sliderResetValue=pyqtSignal()
    
    #Signal emit when userMode changed state
    userModeSignal=pyqtSignal()
    
    enableCustomizeWindowHint=pyqtSignal()
    disableWindowCloseButtonHint=pyqtSignal()
    