# -*- coding: utf-8 -*-/
"""
/***************************************************************************
TnT_CaptureManager
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

30/03/2022: Nettoyage rapide du code.
15/03/2022: Factorisation de l'ensemble des classes mapTool.
             Ajout de "traces" entree dans les méthodes.

TODO: gestion d'une stack undo/redo

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

from qgis import processing
from qgis.core import (QgsProject, QgsVectorLayer, QgsFeature,
                       QgsGeometry, QgsProcessingFeatureSourceDefinition,
                       QgsVectorDataProvider, QgsWkbTypes,QgsFeatureSource)

from qgis.gui import (QgsMapToolEmitPoint, QgsRubberBand, QgsMapCanvas)

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QApplication, QPushButton)
from PyQt5.QtGui import QColor, QKeyEvent

from .TnT_Features import TnTFeaturesManager

def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno


class TnTmapToolEmitPoint(QgsMapToolEmitPoint):

#=============================================================================
    """
    User capture management class.
    Associated geometry of point type.
    """
    def __init__(self, parent, canvas, nomenclaturewidget):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        super().__init__(canvas)
        
        self.parent=parent
        self.canvas=canvas
        self.nomenclaturewidget=nomenclaturewidget

        self.capture = False
        self.layer = None
        self.selectionLayer=None

        # self.tntundoredo=TnTUndoRedo()

        self.selectionRubberBand = self.createRubberBand(QgsWkbTypes.PointGeometry)
        self.setGraphicRenderingPoint_RubberBand(self.selectionRubberBand)
        self.selectionRubberBand.show()


# BEGIN About RUBBERBAND ############################

    def getListRubberBand(self):
        """


        Returns
        -------
        list
            DESCRIPTION.

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        return [self.selectionRubberBand]

    def createRubberBand(self, wkbTypes:QgsWkbTypes):
        """


        Parameters
        ----------
        wkbTypes : QgsWkbTypes
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return QgsRubberBand(self.canvas, wkbTypes)

    def setGraphicRenderingPoint_RubberBand(self,
                            rubberBand,
                            icon=QgsRubberBand.ICON_CIRCLE,
                            iconSize=6,
                            widthLine=0,
                            strokeColor=QColor(13, 195, 240, 200)
                            ):
        """
        Parameters
        ----------
        rubberBand : TYPE
            DESCRIPTION.
        icon : TYPE, optional
            DESCRIPTION. The default is QgsRubberBand.ICON_CIRCLE.
        iconSize : TYPE, optional
            DESCRIPTION. The default is 6.
        widthLine : TYPE, optional
            DESCRIPTION. The default is 0.
        strokeColor : TYPE, optional
            DESCRIPTION. The default is QColor(13, 195, 240, 200).

        Returns
        -------
        None.

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        rubberBand.setIcon       ( icon )
        rubberBand.setIconSize   ( iconSize    )
        rubberBand.setWidth      ( widthLine   )
        rubberBand.setStrokeColor( strokeColor )


    def resetRubberBand(self, listRubberBand):
        """
        Parameters
        ----------
        listRubberBand : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
       # print(f"line:{lineno()},{self.__class__.__name__}->"+
       #       f"{inspect.currentframe().f_code.co_name}()")
       
        for rubberBand in listRubberBand:
            typeGeometry=rubberBand.asGeometry().type()
            rubberBand.reset(typeGeometry)


    def addPoint2RubberBand(self, listRubberBand, point):
        """
        Add one point "point" to into geometry of rubber band.
            param point:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        for rubberBand in listRubberBand:
            rubberBand.addPoint(point,True)


    def removeLastPoint2RubberBand(self, listRubberBand):
        """
        Remove last point from rubber band geometry.
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        for rubberBand in listRubberBand:
            rubberBand.removeLastPoint()

# END About RUBBERBAND ############################

# BEGIN About CAPTURE ############################

    def getPredicate(self):
        """
        In TnTmapToolEmitPoint class , predicate is always 0 (0=intersect)

            returns: predicate
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return 0

    def setCapture(self, capture_state):
        """
            param capture_state:
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.capture=capture_state


    def getCapture(self):
        """
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return self.capture


    def toggleCapture(self):
        """
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.setCapture(not self.getCapture())

    def disable_selecting_tool_group(self):
        # NOTE résolution issue 1 freeze le changement de géométrie pendant saisie de géométrie

        masterWindow = self.parent.getMasterWindow()
        associatedWindow = masterWindow.associatedWindow
        associatedSelectingToolGroup = associatedWindow.getSelectingToolGroupWidget()
        masterSelectingToolGroup = masterWindow.getSelectingToolGroupWidget()
        masterSelectingToolGroup.disable_tool()
        associatedSelectingToolGroup.disable_tool()

    def enable_selecting_tool_group(self):
        # NOTE résolution issue 1 freeze le changement de géométrie pendant saisie de géométrie, réactivation
        masterWindow = self.parent.getMasterWindow()
        associatedWindow = masterWindow.associatedWindow
        associatedSelectingToolGroup = associatedWindow.getSelectingToolGroupWidget()
        masterSelectingToolGroup = masterWindow.getSelectingToolGroupWidget()
        masterSelectingToolGroup.enable_tool()
        associatedSelectingToolGroup.disable_tool()

    def enable_slider_group(self):
        # NOTE résolution issue 1 freeze le changement de slider pendant changement de géométrie, réactivation
        masterWindow = self.parent.getMasterWindow()
        associatedWindow = masterWindow.associatedWindow
        associatedSelectingToolGroup = associatedWindow.getSliderGroup()
        masterSelectingToolGroup = masterWindow.getSliderGroup()
        masterSelectingToolGroup.setEnabled(True)
        associatedSelectingToolGroup.setEnabled(True)

    def disable_slider_group(self):
        # NOTE résolution issue 1 freeze le changement de slider pendant saisie de géométrie
        masterWindow = self.parent.getMasterWindow()
        associatedWindow = masterWindow.associatedWindow
        associatedSelectingToolGroup = associatedWindow.getSliderGroup()
        masterSelectingToolGroup = masterWindow.getSliderGroup()
        masterSelectingToolGroup.setEnabled(False)
        associatedSelectingToolGroup.setEnabled(False)

    def startCapturing(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.lockAtStartCapture()

        #self.parent.labelInfo.setText("END=Mouse right click / ABORT=ESC / Ctrl+Z=deleting the last entry ")

        #self.layer=self.getActiveLabeledLayer().layer()
        self.layer=self.canvas.currentLayer()


        if self.layer.hasSpatialIndex() != QgsFeatureSource.SpatialIndexPresent:
            prov=self.layer.dataProvider()
            prov.createSpatialIndex()

        if not self.selectionLayer :
            self.selectionLayer=self.createTempVectorLayer()


        self.setCapture(True)
        # NOTE: résolution issue freeze sélection géométrie
        self.disable_selecting_tool_group()
        self.disable_slider_group()
        self.capturing(e)


    def capturing(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pt=self.toMapCoordinates(e.pos())
        self.addPoint2RubberBand(self.getListRubberBand(), pt)
        self.showSelected(self.selectionRubberBand, self.getPredicate())


    def endCapturing(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.setCapture(False)
        self.unLockAtEndCapture()
        
        #Refresh canvas to display red line around uncompleted segments
        parentSelectingToolGroup = self.parent
        masterWindow = self.parent.getMasterWindow()
        associatedWindow = masterWindow.associatedWindow
        masterSelectingToolGroup = masterWindow.getSelectingToolGroupWidget()
        # NOTE résolution issue 1 freeze le changement de saisie pendant géométries, réactivation

        if masterSelectingToolGroup == parentSelectingToolGroup:
            associatedCanvas = associatedWindow.centralWidget().findChild(QgsMapCanvas, "mapCanvas")
            associatedCanvas.refresh()
        else:
            masterCanvas = masterWindow.centralWidget().findChild(QgsMapCanvas, "mapCanvas")
            masterCanvas.refresh()
        self.enable_selecting_tool_group()
        self.enable_slider_group()

    def abortCapturing(self):
        """
            returns none:
        """
       # print(f"line:{lineno()},{self.__class__.__name__}->"+
       #       f"{inspect.currentframe().f_code.co_name}()")
        # NOTE résolution issue 1 freeze le changement de saisie pendant géométries, réactivation

        self.resetAll()
        self.layer.reload()
        self.unLockAtEndCapture()
        self.enable_selecting_tool_group()
        self.enable_slider_group()


    def lockAtStartCapture(self):
        """
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        #self.comm.lockAssociatedButton.emit()


    def unLockAtEndCapture(self):
        """
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        # NOTE résolution issue 1 freeze le changement de saisie pendant géométries, réactivation
        self.enable_selecting_tool_group()
        self.enable_slider_group()
        #self.comm.unLockAssociatedButton.emit()

 # END About CAPTURE ############################

 # BEGIN About Layer ############################

    def getActiveLabeledLayer(self):
        """
        Return a current active layer.
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return self.parent.getActiveLabeledLayer()

 # END About Layer ############################


# BEGIN About Selection ############################

    def unStack(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.removeLastPoint2RubberBand(self.getListRubberBand())
        self.showSelected(self.selectionRubberBand,self.getPredicate())


    def removeSelection(self, e) :
        """
        Deselect selected segments at position e.x() e.y().
            param e:
            returns
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        identifiedSegments = self.identifyTool.identify(e.x(), e.y(),
                                                        self.identifyMode,
                                                        self.identifyType)
        self.layer.deselect(identifiedSegments[0].mFeature.id())


    def showSelected(self, rubber_band, predicate):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        geometry=rubber_band.asGeometry()

        self.selectionLayer=self.addGeometry(self.selectionLayer,geometry)
        self.selectionLayer.selectAll()

        #PREDICATE values
        # 0 — intersect
        # 1 — contain
        # 2 — disjoint
        # 3 — equal
        # 4 — touch
        # 5 — overlap
        # 6 — are within
        # 7 — cross

        params = {'INPUT':self.layer,
                  'PREDICATE':predicate,
                  'INTERSECT':QgsProcessingFeatureSourceDefinition(self.selectionLayer.id(), True)
                 }
        processing.run("qgis:selectbylocation", params)


    def addGeometry(self, temp_layer:QgsVectorLayer, geometry:QgsGeometry ):
        """
            param temp_layer:
            param geometry:
            returns temp_layer:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        feature=None
        try :
            feature=next(temp_layer.getFeatures())
        except StopIteration :
             #Create first valid feature with geometry
            pr=temp_layer.dataProvider()
            feature=QgsFeature()
            feature.setGeometry(geometry)
            pr.addFeatures([feature])
        else :
            prov=temp_layer.dataProvider()
            caps=prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeGeometries:
                prov.changeGeometryValues({ 1 : geometry })

        temp_layer.updateExtents()
        return temp_layer


# END About Selection ############################

# BEGIN About Class ############################

    def getAttributeValues( self,
                            provider=None,
                            attributs:dict=None
                          ):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        fieldsAndValues = self.nomenclaturewidget.getSelectedValuesAsDict()
        
        for key in fieldsAndValues.keys():
            index = provider.fieldNameIndex(key)
            attributs[index]=fieldsAndValues[key]
        return attributs


    def removeAllClass(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        prov=self.layer.dataProvider()

        attrs = {}
        attrs = self.getAttributeValues(provider=prov, attributs=attrs)

        for key in attrs.keys():
            attrs[key]=None

        masterWindow = self.parent.getMasterWindow()
        tntFeaturesManager: TnTFeaturesManager = masterWindow.projectManager.tnTProjectObject.tntFeaturesManager
        tntFeaturesLevel = tntFeaturesManager.getTnTFeaturesLevel(self.layer)

        parents = []
        for featureId in self.layer.selectedFeatureIds():
            tntFeature = tntFeaturesLevel.features[featureId]
            tntFeature.removeAll(attrs)
            if tntFeature.parent is not None:
                parents.append(tntFeature.parent)

        for parent in set(parents):
            parent.check(attrs, attrs)

        self.layer.removeSelection()

    def removeCurrentClass(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        prov=self.layer.dataProvider()

        attrs = {}
        attrs = self.getAttributeValues(provider=prov, attributs=attrs)

        key = list(attrs.keys())[1]
        codeValue = attrs[key]

        for k in attrs.keys():
            attrs[k]=None

        masterWindow = self.parent.getMasterWindow()
        tntFeaturesManager:TnTFeaturesManager = masterWindow.projectManager.tnTProjectObject.tntFeaturesManager
        tntFeaturesLevel = tntFeaturesManager.getTnTFeaturesLevel(self.layer)

        parents = []
        for featureId in self.layer.selectedFeatureIds():
            tntFeature = tntFeaturesLevel.features[featureId]
            if str(tntFeature.getAttributes()[key])==codeValue:
                tntFeature.removeCurrentClass(attrs, codeValue)
                if tntFeature.parent is not None:
                    parents.append(tntFeature.parent)

        for parent in set(parents):
            parent.check(attrs, attrs)

        self.layer.removeSelection()


    def resetAll(self):
        """
            returns none:
        """
       # print(f"line:{lineno()},{self.__class__.__name__}->"+
       #       f"{inspect.currentframe().f_code.co_name}()")
       
        self.resetRubberBand(self.getListRubberBand())
        QgsProject.instance().removeMapLayer(self.selectionLayer)
        self.selectionLayer=None
        self.setCapture(False)

    
    def getLayers(self):
        """
            returns layers of the vintage
        """
        mainWindow = self.parent.getMainWindow()
        layerTreeWidget = mainWindow.getTnTLayerTreeWidget()
        root = layerTreeWidget.layerTreeRoot()
        vintage = mainWindow.getVintage()
        if vintage:
            groupName = f"LABELED_DATA_{vintage}"
        else:
            groupName = "LABELED_DATA"

        group = root.findGroup(groupName)
        layers = group.findLayers()

        return layers



    def applyClass(self):
    
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        prov=self.layer.dataProvider()

        attrs = {}
        attrs = self.getAttributeValues(provider=prov, attributs=attrs)

        attrsNull = {}
        for k in attrs.keys():
            attrsNull[k]=None

        masterWindow = self.parent.getMasterWindow()
        tntFeaturesManager:TnTFeaturesManager = masterWindow.projectManager.tnTProjectObject.tntFeaturesManager
        tntFeaturesLevel = tntFeaturesManager.getTnTFeaturesLevel(self.layer)

        parents = []
        for featureId in self.layer.selectedFeatureIds():
            tntFeature = tntFeaturesLevel.features[featureId]
            tntFeature.changeAttribute(attrs)
            if tntFeature.parent is not None:
                parents.append(tntFeature.parent)

        for parent in set(parents):
            parent.check(attrs, attrsNull)

        self.layer.removeSelection()


    def processUserInput(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        task = self.parent.getTask()
        if task == "Labeling" :
            self.applyClass()
        # elif self.parent.getDeleteAllMode():
        elif task == "Delete All":
            self.removeAllClass()
        else:
            self.removeCurrentClass()
        self.resetAll()
        self.layer.reload()

# END About Class ############################

# BEGIN About Event ##########################
    def keyPressEvent(self , e:QKeyEvent):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        if QApplication.keyboardModifiers() == Qt.ControlModifier and e.key()==Qt.Key_Z: #CTRL+Z
            self.unStack()
        elif e.key()==Qt.Key_Escape:
            self.abortCapturing()
        else :
            pass

    def canvasPressEvent(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        if e.type()==QEvent.MouseButtonPress:
            if e.button() == Qt.LeftButton :
                if not self.getCapture() :
                    self.startCapturing(e)
                else :
                    self.capturing(e)
            elif e.button() == Qt.RightButton and self.getCapture():

                self.endCapturing()
                self.processUserInput()
                

# END About Event ##########################

    def createTempVectorLayer(self):
        """
            returns vl:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        vl = QgsVectorLayer("Point", "temporary_points", "memory")
        vl.setCrs(self.layer.crs())
        QgsProject.instance().addMapLayer(vl)
        return vl

class TnTmapToolEmitPline(TnTmapToolEmitPoint):
    """
    User capture management class.
    Associated geometry of line type.
    """
    def __init__(self, parent, canvas, nomenclaturewidget):
        TnTmapToolEmitPoint.__init__(self, parent, canvas, nomenclaturewidget)

        self.pendingCapture = False

        self.selectionRubberBand = self.createRubberBand(QgsWkbTypes.LineGeometry)
        self.setGraphicRenderingLine_RubberBand(self.selectionRubberBand)
        self.selectionRubberBand.show()

        self.rbPoint    = self.createRubberBand(QgsWkbTypes.PointGeometry)
        self.setGraphicRenderingPoint_RubberBand(self.rbPoint)
        self.rbPoint.show()

        self.dashRubberBand=self.createRubberBand(QgsWkbTypes.LineGeometry)
        self.setGraphicRenderingLine_RubberBand(self.dashRubberBand, Qt.DashLine, 1)
        self.dashRubberBand.show()


# BEGIN About RUBBERBAND ############################
    def getListRubberBand(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return [self.selectionRubberBand,self.rbPoint,self.dashRubberBand]

    def setGraphicRenderingLine_RubberBand (self,
                                        rubberBand,
                                        lineStyle=Qt.SolidLine,
                                        widthLine=2,
                                        strokeColor=QColor(13, 195, 240, 200)
                                       ):
        """
        Styles line available are Qt.SolidLine,
                                  Qt.DashLine,
                                  Qt.DotLine,
                                  Qt.DashDotLine,
                                  Qt.DashDotDotLine,
                                  Qt.CustomDashLine
        rubberBand  :
        lineStyle   : line style, (default Qt.SolidLine style).
        widthLine   :
        strokeColor :
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        rubberBand.setLineStyle  ( lineStyle )
        rubberBand.setWidth      ( widthLine )
        rubberBand.setStrokeColor( strokeColor )
# END About RUBBERBAND ############################


# BEGIN About CAPTURE ############################

    def endCapturing(self):
        """
            returns none:
        """
      # print(f"line:{lineno()},{self.__class__.__name__}->"+
      #       f"{inspect.currentframe().f_code.co_name}()")
        # NOTE résolution issue 1 freeze le changement de saisie pendant géométries, réactivation

        self.setCapture(False)
        self.dashRubberBand.reset(QgsWkbTypes.LineGeometry)
        self.unLockAtEndCapture()
        self.enable_selecting_tool_group()
        self.enable_slider_group()


# End About CAPTURE   ############################

# BEGIN About Class ############################
    def setPendingCapture(self, pendingCapture):
        """
            returns none:
        """
       # print(f"line:{lineno()},{self.__class__.__name__}->"+
       #       f"{inspect.currentframe().f_code.co_name}()")
       
        self.pendingCapture=pendingCapture


    def resetAll(self):
        """
            returns none:
        """
      # print(f"line:{lineno()},{self.__class__.__name__}->"+
      #       f"{inspect.currentframe().f_code.co_name}()")
      
        self.resetRubberBand(self.getListRubberBand())
        QgsProject.instance().removeMapLayer(self.selectionLayer)
        self.selectionLayer=None
        self.setCapture(False)
        self.setPendingCapture(False)

# END About Class ############################

# BEGIN About Event ##########################
    def canvasPressEvent(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        if e.type()==QEvent.MouseButtonPress:
            if e.button() == Qt.LeftButton:
                if not self.getCapture():
                    self.startCapturing(e)
                else :
                    if self.pendingCapture:
                        self.pendingCapture=False
                    self.capturing(e)
            elif (e.button() == Qt.RightButton and self.getCapture()) :
                self.endCapturing()
                self.processUserInput()

    def canvasMoveEvent(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        if self.capture and not self.pendingCapture :
            self.capturing(e)

        pt=self.toMapCoordinates(e.pos())
        self.dashRubberBand.movePoint(pt)

    def canvasReleaseEvent(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        if e.button() == Qt.LeftButton and self.getCapture() :
            self.pendingCapture=True
            # END About Event ##########################

    def createTempVectorLayer(self):
        """
            returns vl:
        """
       # print(f"line:{lineno()},{self.__class__.__name__}->"+
       #       f"{inspect.currentframe().f_code.co_name}()")
       
        vl = QgsVectorLayer("LineString", "temporary_Lines", "memory")
        vl.setCrs(self.layer.crs())
        QgsProject.instance().addMapLayer(vl)
        return vl

class TnTmapToolEmitPolygon(TnTmapToolEmitPline):
    """
    User capture management class.
    Associated geometry of polygon type.
    """

    def __init__(self, parent, canvas, nomenclaturewidget, strictMode=False):
        TnTmapToolEmitPline.__init__(self, parent, canvas, nomenclaturewidget)

        self.strictMode=strictMode

        self.selectionRubberBand = self.createRubberBand(QgsWkbTypes.PolygonGeometry)
        self.setGraphicRenderingPoly_RubberBand(self.selectionRubberBand)
        self.selectionRubberBand.show()

# BEGIN About RUBBERBAND ############################
    def setGraphicRenderingPoly_RubberBand (self,
                                       rubberBand,
                                       lineStyle=Qt.SolidLine,
                                       widthLine=2,
                                       strokeColor=QColor(13, 195, 240, 255),
                                       fillColor=QColor(255, 254, 181, 10)
                                          ):
        """
        rubberBand  :
        lineStyle   :
        widthLine   :
        strokeColor :
        fillColor   :
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        rubberBand.setLineStyle  ( lineStyle )
        rubberBand.setWidth      ( widthLine   )
        rubberBand.setStrokeColor( strokeColor )
        rubberBand.setFillColor  ( fillColor   )
# END About RUBBERBAND ############################

# BEGIN About CAPTURE #############################
    def getPredicate(self):
        """
        In TnTmapToolEmitPolygon class , predicate is 0 (0=intersect) or 6 (6=are within)
        following the value of self.strictMode.
            returns predicate.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return (lambda:0, lambda:6)[self.strictMode]()

    def capturing(self, e):
        """
            param e:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pt=self.toMapCoordinates(e.pos())
        self.addPoint2RubberBand(self.getListRubberBand(), pt)
        if self.rbPoint.numberOfVertices()>2:
            self.showSelected(self.selectionRubberBand, self.getPredicate())

# End About CAPTURE   ############################


    def createTempVectorLayer(self):
        """
            returns vl:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        vl = QgsVectorLayer("Polygon", "temporary_polygons", "memory")
        vl.setCrs(self.layer.crs())
        QgsProject.instance().addMapLayer(vl)
        return vl
