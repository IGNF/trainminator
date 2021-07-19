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
import inspect
import time 


from qgis import processing

from qgis.core import (QgsProject, QgsVectorLayer, QgsFeature, 
                       QgsGeometry, QgsProcessingFeatureSourceDefinition,QgsVectorDataProvider, 
                       QgsWkbTypes,QgsFeatureSource)

from qgis.gui import (QgsMapToolEmitPoint, QgsRubberBand)

from PyQt5.QtCore import Qt, QEvent 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QKeyEvent


 
class Timer(object):  
    def start(self):  
        if hasattr(self, 'interval'):  
            del self.interval  
        self.start_time = time.time()  
  
    def stop(self):  
        if hasattr(self, 'start_time'):  
            self.interval = time.time() - self.start_time  
            del self.start_time # Force timer reinit  

class TnTmapToolEmitPoint_V2(QgsMapToolEmitPoint):
    def __init__(self, parent, canvas, sender):      
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.parent=parent
        self.canvas = canvas
        #self.sender=sender
        self.capture = False
        self.layer = None
        self.selectionLayer=None
               
        iconSize       = 6
        strokeColor    = QColor(13, 195, 240, 200)
        widthLine      = 2
         
        self.rbPoint = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rbPoint.setIcon( QgsRubberBand.ICON_CIRCLE )
        self.rbPoint.setIconSize   ( iconSize    )
        self.rbPoint.setWidth      ( widthLine   )
        self.rbPoint.setStrokeColor( strokeColor )
        
        
    def lineno(self):
        "Returns the current line number"
        return inspect.currentframe().f_back.f_lineno
       
    def lockAtStartCapture(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:lockAtStartCapture()")
        self.parent.comm.lockAssociatedButton.emit()
               
    def unLockAtEndCapture(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:unLockAtStartCapture()")
        self.parent.comm.unLockAssociatedButton.emit()
      
    def getActiveLabeledLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPoint_v2:getActiveLabeledLayer()")
        return self.parent.getActiveLabeledLayer()
    
    def getNameOfActiveLabeledLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPoint_v2:getNameOfActiveLabeledLayer()")
        return self.parent.getNameOfActiveLabeledLayer()
    
    def resetAllRubberBand(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:resetAllRubberBand()")
        typeGeometry=self.rbPoint.asGeometry().type()
        self.rbPoint.reset(typeGeometry)      
        
    def addPoint2AllRubberBand(self, point):
        self.rbPoint.addPoint(point,True)
              
    def removeLastPoint2AllRubberBand(self):
        self.rbPoint.removeLastPoint()
        
    def removeSelection(self, e) :
        #print(f"line:{self.lineno()}, ->removeSelection({e})")
        identifiedSegments = self.identifyTool.identify(e.x(), e.y(), 
                                                        self.identifyMode, 
                                                        self.identifyType)
        self.layer.deselect(identifiedSegments[0].mFeature.id())

    def setCapture(self, captureState):
        #print(f"line:{self.lineno()}, ->->TnTmapToolEmitPoint_v2:setCapture({captureState})")
        self.capture=captureState
        
    def getCapture(self):
        return self.capture

    def toggleCapture(self):
        self.setCapture(not self.getCapture())
                    
    def startCapturing(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:startCapturing({e})")
        self.lockAtStartCapture()
        #self.parent.labelInfo.setText("END=Mouse right click / ABORT=ESC / Ctrl+Z=deleting the last entry ")
        
        
        self.layer=self.getActiveLabeledLayer().layer()
        if self.layer.hasSpatialIndex() != QgsFeatureSource.SpatialIndexPresent: 
            prov=self.layer.dataProvider()
            prov.createSpatialIndex()        
        if not self.selectionLayer : self.selectionLayer=self.createTempVectorLayer()
        
        self.setCapture(True)  
        self.capturing(e)
            
    def capturing(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:capturing({e})")
        pt=self.toMapCoordinates(e.pos()) 
        self.addPoint2AllRubberBand(pt)   
        self.showSelected()  
       
    def endCapturing(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:endCapturing()")
        self.setCapture(False)
        self.unLockAtEndCapture()
        #self.parent.labelInfo.setText("Stopping Capture mode.")
              
    def showSelected(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:showSelect()")
        geometry=self.rbPoint.asGeometry()
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
                  'PREDICATE':0,
                  'INTERSECT':QgsProcessingFeatureSourceDefinition(self.selectionLayer.id(), True)
                 }
        processing.run("qgis:selectbylocation", params) 
        
    
    def createTempVectorLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPoint_v2:createTempVectorLayer()")
        vl = QgsVectorLayer("Point", "temporary_points", "memory")
        vl.setCrs(self.layer.crs())
        #voir: ajout de la map au QgsProject????
        QgsProject.instance().addMapLayer(vl)
        return vl
    
    def addGeometry(self, tempLayer:QgsVectorLayer, geometry:QgsGeometry ):        
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPoint_v2:addGeometry()")     
        feature=None
        try :
            feature=next(tempLayer.getFeatures())
        except StopIteration :
             #Create first valid feature with geometry
            pr = tempLayer.dataProvider()
            feature = QgsFeature()
            feature.setGeometry(geometry)
            pr.addFeatures([feature])
        else :
            prov=tempLayer.dataProvider()
            caps=prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeGeometries:
                prov.changeGeometryValues({ 1 : geometry })          
                          
        tempLayer.updateExtents()
        return tempLayer
                 
    def unStack(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:unStack()")
        self.removeLastPoint2AllRubberBand()
        self.showSelected()
             
    def keyPressEvent(self , e:QKeyEvent):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:keyPressEvent({e})")  
        if QApplication.keyboardModifiers() == Qt.ControlModifier and e.key()==Qt.Key_Z: #CTRL+Z
            self.unStack()
        elif e.key()==Qt.Key_Escape:
            self.abortCapturing()
        else :
            pass
               
    def canvasPressEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:canvasPressEvent({e})")       
        if e.type()==QEvent.MouseButtonPress:
            if e.button() == Qt.LeftButton :
                if not self.getCapture() : self.startCapturing(e) 
                else : self.capturing(e)
            elif e.button() == Qt.RightButton and self.getCapture():
                self.endCapturing()
                #self.applyLabel()
                
                self.processUserInput()
            

    def abortCapturing(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:abortCapturing()")    
        self.resetAll()
        self.layer.reload()      
        self.unLockAtEndCapture()
    
    def resetAll(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:resetAll()")
        self.resetAllRubberBand()
        QgsProject.instance().removeMapLayer(self.selectionLayer)	
        self.selectionLayer=None
        self.setCapture(False)
            
    def processUserInput(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:processUserInput()")
        if self.parent.getLabelingMode():     self.applyClass()           
        elif self.parent.getDeleteAllMode() : self.removeAllClass()
        else :                                self.removeCurrentClass()        
        self.resetAll()   
        self.layer.reload()
        
        
    def removeAllClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:removeAllClass()")
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
                  
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
                          
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:None, index_label:'', index_labelColor:None }
                prov.changeAttributeValues({ featureId : attrs })
        
        self.layer.removeSelection()                     

    def removeCurrentClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:removeCurrentClass()")
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
          
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
        
        fieldCodeName=fieldNameHeader[0]
        codeValue=self.parent.mainWindow.nomenclatureWidget.classSelected[0]
        
        param_sel = { 'INPUT':self.layer,
                      'FIELD':fieldCodeName,
                      'OPERATOR':0,  #0  =
                      'VALUE':codeValue,
                      'METHOD':3
                     }       
        processing.run('qgis:selectbyattribute',param_sel)
             
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:None, index_label:'', index_labelColor:None }
                prov.changeAttributeValues({ featureId : attrs })

          
        self.layer.removeSelection()   

    
    def applyClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPoint_v2:applyClass()")             
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
        
        classSelected=self.parent.mainWindow.nomenclatureWidget.classSelected
        code=classSelected[0]
        label=classSelected[1]
        labelColor=classSelected[2]
        Int_color=int(labelColor.split('#')[1],16)
                         
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
                          
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:code, index_label:label, index_labelColor:Int_color }
                prov.changeAttributeValues({ featureId : attrs })
            
        self.layer.removeSelection()   

class TnTmapToolEmitPline_V2(QgsMapToolEmitPoint):
    def __init__(self, parent, canvas):    
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.parent         = parent
        self.canvas         = canvas
        self.capture        = False
        self.pendingCapture = False
        self.layer          = None
        self.selectionLayer = None

        strokeColor    = QColor(13, 195, 240, 200)
        iconSize       = 6
        widthLine      = 2
        widthDashLine  = 1

        self.rbLine   = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rbLine.setStrokeColor( strokeColor )
        self.rbLine.setWidth      ( widthLine   )
    
        self.rbPoint = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rbPoint.setIcon( QgsRubberBand.ICON_CIRCLE )
        self.rbPoint.setIconSize   ( iconSize    )
        self.rbPoint.setWidth      ( widthLine   )
        self.rbPoint.setStrokeColor( strokeColor )

        self.rbDashline  = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rbDashline.setStrokeColor( strokeColor )
        self.rbDashline.setLineStyle  ( Qt.DashLine )
        self.rbDashline.setWidth      ( widthDashLine )
       

    def lineno(self):
        "Returns the current line number"
        return inspect.currentframe().f_back.f_lineno  
      
    def lockAtStartCapture(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:lockAtStartCapture()")
        self.parent.comm.lockAssociatedButton.emit()
               
    def unLockAtEndCapture(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:unLockAtStartCapture()")
        self.parent.comm.unLockAssociatedButton.emit()

    def getCapture(self):
        return self.capture
    
    def setCapture(self, captureState):
        self.capture=captureState
    
    def toggleCapture(self):
        self.setCapture(not self.getCapture())
    

    def getActiveLabeledLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPolygon_V2:getActiveLabeledLayer()")
        return self.parent.getActiveLabeledLayer()
    
    def getNameOfActiveLabeledLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPolygon_V2:getNameOfActiveLabeledLayer()")
        return self.parent.getNameOfActiveLabeledLayer()    
        
    def resetAllRubberBand(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:resetAllRubberBand()")
        typeGeometry=self.rbLine.asGeometry().type()
        self.rbLine.reset(typeGeometry)
        
        typeGeometry=self.rbPoint.asGeometry().type()
        self.rbPoint.reset(typeGeometry)
        
        typeGeometry=self.rbDashline.asGeometry().type()
        self.rbDashline.reset(typeGeometry)
        
    def addPoint2AllRubberBand(self, point):
        self.rbLine.addPoint(point,True)
        self.rbPoint.addPoint(point,True)
        self.rbDashline.addPoint(point,True)
        
    def removeLastPoint2AllRubberBand(self):
        self.rbLine.removeLastPoint()
        self.rbPoint.removeLastPoint()
        self.rbDashline.removeLastPoint()

    def startCapturing(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:startCapturing({e})")
        self.lockAtStartCapture()
        #self.parent.labelInfo.setText("Starting  Capture mode: END=Mouse right click / ABORT=ESC")
           
        self.layer=self.getActiveLabeledLayer().layer()      
        if self.layer.hasSpatialIndex() != QgsFeatureSource.SpatialIndexPresent: 
            prov=self.layer.dataProvider()
            prov.createSpatialIndex()

        if not self.selectionLayer : self.selectionLayer=self.createTempVectorLayer() 
        
        self.setCapture(True)      
        self.capturing(e)

    def capturing(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:capturing({e})")
        pt=self.toMapCoordinates(e.pos())
        self.addPoint2AllRubberBand(pt)
        self.showSelected(self.rbLine, 0)
              
    def endCapturing(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:endCapturing()")     
        self.setCapture(False)
        self.rbDashline.reset(QgsWkbTypes.LineGeometry)  
        self.unLockAtEndCapture()
        #self.parent.labelInfo.setText("Stopping Capture mode.")
           
    def abortCapturing(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:abortCapturing()")
        self.resetAll()
        self.layer.reload()      
        self.unLockAtEndCapture()
        
    def unStack(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:unStack()")
        self.removeLastPoint2AllRubberBand()
        self.showSelected(self.rbLine, 0)
     
      
    def showSelected(self, rubberBand, predicate):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:showSelected(rubberBand={rubberBand} , predicate={predicate}") 
        geometry=rubberBand.asGeometry()
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
       
    
    def addGeometry(self, tempLayer:QgsVectorLayer, geometry:QgsGeometry ): 
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPline_V2:addGeometry()")     
        feature=None
        try :
            feature=next(tempLayer.getFeatures())
        except StopIteration :
             #Create first valid feature with geometry
            pr = tempLayer.dataProvider()
            feature = QgsFeature()
            feature.setGeometry(geometry)
            pr.addFeatures([feature])
        else :
            prov=tempLayer.dataProvider()
            caps=prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeGeometries:
                prov.changeGeometryValues({ 1 : geometry })          
                          
        tempLayer.updateExtents()
        return tempLayer
        
    def createTempVectorLayer(self):
        #print(f"line:{self.lineno()}, ->->TnTmapToolEmitPline_V2:createTempVectorLayer()")
        vl = QgsVectorLayer("LineString", "temporary_Lines", "memory")
        vl.setCrs(self.layer.crs())
        QgsProject.instance().addMapLayer(vl)
        
        return vl   
     
    def keyPressEvent(self , e:QKeyEvent):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:keyPressEvent({e})")
        if QApplication.keyboardModifiers() == Qt.ControlModifier and e.key()==Qt.Key_Z: #CTRL+Z
            self.unStack()               
        elif e.key()==Qt.Key_Escape:
            self.abortCapturing()
        
    def canvasPressEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:canvasPressEvent({e})")
        if e.type()==QEvent.MouseButtonPress:
            if e.button() == Qt.LeftButton :
                if not self.getCapture() : self.startCapturing(e) 
                else :
                    if self.pendingCapture : self.pendingCapture=False
                    self.capturing(e)
            elif (e.button() == Qt.RightButton and self.getCapture()) :
                self.endCapturing()
                self.processUserInput()
               
    def canvasMoveEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:self.getCapture():{self.getCapture()}") 
        if self.capture and not self.pendingCapture :
                self.capturing(e)

        pt=self.toMapCoordinates(e.pos())
        self.rbDashline.movePoint(pt)
                    
    def canvasReleaseEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:canvasReleaseEvent({e})")
        if e.button() == Qt.LeftButton and self.getCapture() :
            self.pendingCapture=True

    def resetAll(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:resetAll()")
        self.resetAllRubberBand()
        QgsProject.instance().removeMapLayer(self.selectionLayer)	
        self.selectionLayer=None
        self.setCapture(False)
        self.pendingCapture = False
        
             
    def processUserInput(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:processUserInput()")
        if self.parent.getLabelingMode():     self.applyClass()           
        elif self.parent.getDeleteAllMode() : self.removeAllClass()
        else :                                self.removeCurrentClass()  

        self.resetAll()   
        self.layer.reload()
        
        
    def removeAllClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:removeAllClass()")
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
                  
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
                          
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:None, index_label:'', index_labelColor:None }
                prov.changeAttributeValues({ featureId : attrs })
          
        self.layer.removeSelection()                  

    def removeCurrentClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:removeCurrentClass()")
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
          
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
        
        fieldCodeName=fieldNameHeader[0]
        codeValue=self.parent.mainWindow.nomenclatureWidget.classSelected[0]
        
        param_sel = { 'INPUT':self.layer,
                      'FIELD':fieldCodeName,
                      'OPERATOR':0,  #0  =
                      'VALUE':codeValue,
                      'METHOD':3
                     }       
        processing.run('qgis:selectbyattribute',param_sel)
             
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:None, index_label:'', index_labelColor:None }
                prov.changeAttributeValues({ featureId : attrs }) 
                             
        self.layer.removeSelection()   

    def applyClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPline_V2:applyLabel()") 
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
     
        code=self.parent.mainWindow.nomenclatureWidget.classSelected[0]
        label=self.parent.mainWindow.nomenclatureWidget.classSelected[1]
        labelColor=self.parent.mainWindow.nomenclatureWidget.classSelected[2]
        Int_color=  int(labelColor.split('#')[1],16)
                               
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
                               
                            
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:code, index_label:label, index_labelColor:Int_color }
                prov.changeAttributeValues({ featureId : attrs })
         
        self.layer.removeSelection()   
        
        

class TnTmapToolEmitPolygon_V2(QgsMapToolEmitPoint):
    
    def __init__(self, parent, canvas, strictMode=False):       
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.parent         = parent
        self.canvas         = canvas
        #self.sender         = sender
        self.strictMode     = strictMode
        self.capture        = False
        self.pendingCapture = False
        self.layer          = None
        self.selectionLayer = None

        fillColor      = QColor(255, 254, 181, 10)
        strokeColor    = QColor(13, 195, 240, 255) 
        iconSize       = 6
        widthLine      = 2
        widthDashLine  = 1

        self.rbPolygon   = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.rbPolygon.setFillColor  ( fillColor   )
        self.rbPolygon.setStrokeColor( strokeColor )
        self.rbPolygon.setWidth      ( widthLine   )
        self.rbPolygon.show()

        self.rbPoint = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rbPoint.setIcon( QgsRubberBand.ICON_CIRCLE )
        self.rbPoint.setIconSize   ( iconSize    )
        self.rbPoint.setWidth      ( widthLine   )
        self.rbPoint.setStrokeColor( strokeColor )
        self.rbPoint.show()

        self.rbDashline  = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rbDashline.setStrokeColor( strokeColor )
        self.rbDashline.setLineStyle  ( Qt.DashLine )
        self.rbDashline.setWidth      ( widthDashLine )
        self.rbDashline.show()

    def lineno(self):
        "Returns the current line number"
        return inspect.currentframe().f_back.f_lineno  

    def setCapture(self, captureState):
        self.capture=captureState

    def getCapture(self):
        return self.capture
    
    def toggleCapture(self):
        self.setCapture(not self.getCapture())
      
                  
    def lockAtStartCapture(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:lockAtStartCapture()")
        self.parent.comm.lockAssociatedButton.emit()
               
    def unLockAtEndCapture(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:unLockAtStartCapture()")
        self.parent.comm.unLockAssociatedButton.emit()
     
    
    def getPredicate(self):
        return (lambda:0, lambda:6)[self.strictMode]()
        
    def getActiveLabeledLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPolygon_V2:getActiveLabeledLayer()")
        return self.parent.getActiveLabeledLayer()
    
    def getNameOfActiveLabeledLayer(self):
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPolygon_V2:getNameOfActiveLabeledLayer()")
        return self.parent.getNameOfActiveLabeledLayer()    
        
    def resetAllRubberBand(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:resetAllRubberBand()")
        typeGeometry=self.rbPolygon.asGeometry().type()
        self.rbPolygon.reset(typeGeometry)
        
        typeGeometry=self.rbPoint.asGeometry().type()
        self.rbPoint.reset(typeGeometry)
        
        typeGeometry=self.rbDashline.asGeometry().type()
        self.rbDashline.reset(typeGeometry)
        
    def addPoint2AllRubberBand(self, point):
        self.rbPolygon.addPoint(point,True)
        self.rbPoint.addPoint(point,True)
        self.rbDashline.addPoint(point,True)
        
    def removeLastPoint2AllRubberBand(self):
        self.rbPolygon.removeLastPoint()
        self.rbPoint.removeLastPoint()
        self.rbDashline.removeLastPoint()

    def startCapturing(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:startCapturing({e})")
        self.lockAtStartCapture()
        #self.parent.labelInfo.setText("Starting  Capture mode: END=Mouse right click / ABORT=ESC")
        
        self.layer=self.getActiveLabeledLayer().layer()     
        if self.layer.hasSpatialIndex() != QgsFeatureSource.SpatialIndexPresent: 
            prov=self.layer.dataProvider()
            prov.createSpatialIndex()
       
        if not self.selectionLayer : self.selectionLayer=self.createTempVectorLayer()
            
        self.setCapture(True)      
        self.capturing(e)
      
        
    def capturing(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:capturing({e})")
        pt=self.toMapCoordinates(e.pos())
        self.addPoint2AllRubberBand(pt)
        if self.rbPoint.numberOfVertices()>2: self.showSelected(self.rbPolygon, self.getPredicate())
              
    def endCapturing(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:endCapturing()")   
        self.setCapture(False)
        self.rbDashline.reset(QgsWkbTypes.LineGeometry)  
        self.unLockAtEndCapture()
        #self.parent.labelInfo.setText("Stopping Capture mode.")
        
    def abortCapturing(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:abortCapturing()")
        self.resetAll()
        self.layer.reload()
        self.unLockAtEndCapture()
        
    def unStack(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:unStack()")
        self.removeLastPoint2AllRubberBand()
        if self.rbPoint.numberOfVertices()>2: self.showSelected(self.rbPolygon, self.getPredicate())
        
    def resetAll(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:resetAll()")
        self.resetAllRubberBand()
        QgsProject.instance().removeMapLayer(self.selectionLayer)	
        self.selectionLayer=None
        self.setCapture(False)
        self.pendingCapture = False
        
    def showSelected(self, rubberBand, predicate):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:showSelected(rubberBand={rubberBand} , predicate={predicate}") 
        geometry=rubberBand.asGeometry()
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
       
       
    def addGeometry(self, tempLayer:QgsVectorLayer, geometry:QgsGeometry ): 
        #print(f"line:{self.lineno()}, ->TnTmapToolEmitPolygon_V2:addGeometry()")     
        feature=None
        try :
            feature=next(tempLayer.getFeatures())
        except StopIteration :
             #Create first valid feature with geometry
            pr = tempLayer.dataProvider()
            feature = QgsFeature()
            feature.setGeometry(geometry)
            pr.addFeatures([feature])
        else :
            prov=tempLayer.dataProvider()
            caps=prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeGeometries:
                prov.changeGeometryValues({ 1 : geometry })          
                          
        tempLayer.updateExtents()
        return tempLayer
        
    def createTempVectorLayer(self):
        #print(f"line:{self.lineno()}, ->->TnTmapToolEmitPolygon_V2:createTempVectorLayer()")
        vl = QgsVectorLayer("Polygon", "temporary_polygons", "memory")
        vl.setCrs(self.layer.crs())
        vl.setOpacity(0.25)
        QgsProject.instance().addMapLayer(vl)
        return vl   
     
    def keyPressEvent(self , e:QKeyEvent):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:keyPressEvent({e})")
        if QApplication.keyboardModifiers() == Qt.ControlModifier and e.key()==Qt.Key_Z: #CTRL+Z
            self.unStack()               
        elif e.key()==Qt.Key_Escape:
            self.abortCapturing()
        
    def canvasPressEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:canvasPressEvent({e})")         
        if e.type()==QEvent.MouseButtonPress:
            if e.button() == Qt.LeftButton :
                if not self.getCapture() : self.startCapturing(e) 
                else :
                    if self.pendingCapture : self.pendingCapture=False
                    self.capturing(e)
                    
            elif (e.button() == Qt.RightButton and self.getCapture()): #or (self.flyOverMode and e.button() == Qt.RightButton):
                self.endCapturing()
                self.processUserInput()
               
    def canvasMoveEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:self.getCapture():{self.getCapture()}") 
        if self.capture and not self.pendingCapture :
            self.capturing(e)

        pt=self.toMapCoordinates(e.pos())
        self.rbDashline.movePoint(pt)
    
    def canvasReleaseEvent(self, e):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:canvasReleaseEvent({e})")
        if e.button() == Qt.LeftButton and self.getCapture() :
            self.pendingCapture=True
            
            
    def processUserInput(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:processUserInput()")
        if self.parent.getLabelingMode():     self.applyClass()           
        elif self.parent.getDeleteAllMode() : self.removeAllClass()
        else :                                self.removeCurrentClass()  

        self.resetAll()   
        self.layer.reload()
        
        
    def removeAllClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:removeAllClass()")
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
                  
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
                          
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:None, index_label:'', index_labelColor:None }
                prov.changeAttributeValues({ featureId : attrs })
        self.layer.removeSelection()                      

    def removeCurrentClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:removeCurrentClass()")
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
          
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
        
        fieldCodeName=fieldNameHeader[0]
        codeValue=self.parent.mainWindow.nomenclatureWidget.classSelected[0]
        
        param_sel = { 'INPUT':self.layer,
                      'FIELD':fieldCodeName,
                      'OPERATOR':0,  #0  =
                      'VALUE':codeValue,
                      'METHOD':3
                     }       
        processing.run('qgis:selectbyattribute',param_sel)
             
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:None, index_label:'', index_labelColor:None }
                prov.changeAttributeValues({ featureId : attrs })    
        self.layer.removeSelection()   
            
        
    def applyClass(self):
        #print(f"line:{self.lineno()},->TnTmapToolEmitPolygon_V2:applyClass()")     
        prov=self.layer.dataProvider()
        caps=prov.capabilities()
        
        classSelected=self.parent.mainWindow.nomenclatureWidget.classSelected
        code=classSelected[0]
        label=classSelected[1]
        labelColor=classSelected[2]
        Int_color=  int(labelColor.split('#')[1],16)
            
        fieldNameHeader=self.parent.mainWindow.nomenclatureWidget.fieldNameHeader             
        index_code=prov.fieldNameIndex(fieldNameHeader[0])
        index_label=prov.fieldNameIndex(fieldNameHeader[1])
        index_labelColor=prov.fieldNameIndex(fieldNameHeader[2])
                
        
        for featureId in self.layer.selectedFeatureIds():
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                attrs = {index_code:code, index_label:label, index_labelColor:Int_color }
                prov.changeAttributeValues({ featureId : attrs })
                    
        self.layer.removeSelection()   