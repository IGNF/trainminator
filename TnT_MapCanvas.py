# -*- coding: utf-8 -*-/
"""
/***************************************************************************
TnT_MapCanvas
                                 A QGIS plugin
Labelisation de données segmentées.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-01-25
        git sha              : $Format:%H$
        copyright            : (C) 2021 by IGN
        authors              : Yann Le Borgne
        email                : yann.le-borgne@ign.fr
        version              : 1.3.0
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
import inspect

from qgis.gui import( QgsMapCanvas, QgsVertexMarker, QgsMapTool )

from PyQt5.QtCore    import( Qt, QEvent )
from PyQt5.QtGui     import( QColor, QMouseEvent, QEnterEvent, QKeySequence )

from qgis.core import QgsGeometry, QgsPoint
from PyQt5.QtWidgets import QLabel, QShortcut
import numpy as np

def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno

class mapCanvas(QgsMapCanvas):
    """
    Canvas handling class.
    """

    def __init__(self, parent=None, objectName="mapCanvas"):
        super().__init__(parent)

        self.setObjectName(objectName)
        self.setAccessibleName(objectName)

        self.marker = None
        self.synchroMode = False
        self.displayMode = False
        self.setMapTool(QgsMapTool(self),False)

        self.setUpUi()

        #self.getMainWindow()


    def setUpUi(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setCanvasColor(Qt.black)
        self.setDefaultMarker()


    def getMasterWindow(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        parent = self.parent()
        while parent.objectName()!="TraiNminaTor2Dialog_Master" :
            parent = parent.parent()
        return parent

    def setDefaultMarker(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.marker = QgsVertexMarker( self )
        self.marker.setColor( QColor( 255,255,255 ) )
        self.marker.setIconSize( 25 )
        self.marker.setIconType( QgsVertexMarker.ICON_CROSS )
        self.marker.setPenWidth( 1 )

    def setDisplayMode(self):
        if self.displayMode == True:
            self.displayMode = False
        else:
            self.displayMode = True

    def zoomAllToFullExtent(self):
        """Zoom to the full extent of all layers currently visible in
            the canvas. Executed when user press Fit All button.
            Applied to all open canvases if Synchro mode is enabled"""
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        self.zoomToFullExtent()
        if self.getSynchroMode() :
            canvas_list = self.getAllCanvas()
            for canvas in canvas_list :
                canvas.zoomToFullExtent()
                

    def manageSynchroConnections(self, state=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.setSynchroMode(state)
        if state :
            self.setSynchroZoom()
        else :
            self.unsetSynchroZoom()

    def setSynchroZoom(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.extentsChanged.connect(self.synchroExtents)
        

    def unsetSynchroZoom(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        try :
            self.extentsChanged.disconnect()
        except TypeError:
            pass
        

    def synchroExtents(self):
        """
        Synchronization of the zoom/pan between the main and additional view.
            returns none:
        # """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        canvas_list = self.getAllCanvas()
        for canvas in canvas_list :
            if canvas.isVisible() :
                canvas.unsetSynchroZoom()
                canvas.setExtent(self.extent())
                canvas.refresh()
                canvas.setSynchroZoom()
                

    def setSynchroMode(self, state=False):
        """
        This method return state of synchronization mode.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.synchroMode = state
        

    def getSynchroMode(self):
        """
        This method return state of synchronization mode.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.synchroMode

    def getMainWindow(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        parent = self.parent()
        while not parent.objectName() != "TraiNminaTor2Dialog_Master":
            parent = parent.parent()
        return parent


    def getAllCanvas(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        masterWindow = self.getMasterWindow()
        canvas_list = masterWindow.findChildren(mapCanvas, "mapCanvas")
        canvas_list.remove(self)
        return canvas_list
    

    def showMousePointerMarker(self, p):
        """
        This method display the mouse pointer (marker) at <p> position
        in canvas of slave view.
            param p: mouse pointer position  QgsPointXY.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.marker.setCenter(p)
        self.marker.show()


    def mouseMoveEvent(self, event:QMouseEvent):
        """
            returns none:
        """
        if self.getSynchroMode() :
            qgspointXY =self.mapTool().toMapCoordinates(event.pos())
            canvas_list= self.getAllCanvas()
            for canvas in canvas_list :
                canvas.showMousePointerMarker(qgspointXY)
            
        if self.displayMode:
            qgspointXY = self.mapTool().toMapCoordinates(event.pos())
            geo_pt =  QgsGeometry.fromPoint(QgsPoint(qgspointXY.x(), qgspointXY.y()))
            self.showDisplayLabels(geo_pt)       
            
        return QgsMapCanvas.mouseMoveEvent(self, event)

    def showDisplayLabels(self, geo_pt):
        layer = self.currentLayer()
        feats = [feat for feat in layer.getFeatures()]
        id = -1
        for feat in feats:
            if geo_pt.within(feat.geometry()):
                id = feat.id()
                break            
        
        years = []
        for att in layer.fields().names():
            if 'class' in att:
                years.append(att)
            
        masterWindow = self.getMasterWindow()
        labels_year0 = masterWindow.findChildren(QLabel, "label_year0_class")
        labels_year1 = masterWindow.findChildren(QLabel, "label_year1_class")
        
        if id != -1:
            for label in labels_year0:
                label.setText(f"Classe {years[0][-4:]} : {feats[id].attribute(years[0])}")
            for label in labels_year1:
                label.setText(f"Classe {years[1][-4:]} : {feats[id].attribute(years[1])}")

    def leaveEvent(self, event:QEvent):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if self.getSynchroMode() :
            canvas_list= self.getAllCanvas()
            for canvas in canvas_list :
                canvas.marker.hide()
        
        if self.displayMode:
            pass
        
        return QgsMapCanvas.leaveEvent(self, event)


    def enterEvent(self, event:QEnterEvent):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
      
        return QgsMapCanvas.enterEvent(self, event)


    def event(self, event: QEvent):
        evt_Type=event.type()
        if (evt_Type==QEvent.KeyPress or evt_Type==QEvent.KeyRelease) and event.key()==Qt.Key_W:
            masterWindow = self.getMasterWindow()

            showContext = evt_Type==QEvent.KeyPress
            masterWindow.showContext(showContext=showContext, keepGroup=f"CONTEXT_{masterWindow.getVintage()}")

            associatedWindow = masterWindow.associatedWindow
            associatedWindow.showContext(showContext=showContext, keepGroup=f"CONTEXT_{associatedWindow.getVintage()}")
            return True
    
        return QgsMapCanvas.event(self, event)