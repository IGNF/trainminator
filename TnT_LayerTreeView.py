# -*- coding: utf-8 -*-
"""
/***************************************************************************
TnT_LayerTreeView
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
import inspect

from qgis.core import QgsLayerTreeModel, QgsRasterLayer, QgsVectorLayer
from qgis.gui import QgsLayerTreeView


from PyQt5 import QtCore
from PyQt5.QtWidgets import (QSizePolicy, QWidget,  QLabel, 
                             QSlider,QSpacerItem, QVBoxLayout, QHBoxLayout)


class TnTLayerTreeView(QWidget):
    def __init__(self, parentWindow=None, widgetParent=None, layerTreeRoot=None):
        super(TnTLayerTreeView, self).__init__(widgetParent)
        
        self.parentWindow=parentWindow   
        self.layerTreeRoot=layerTreeRoot
        self.layerTreeView=QgsLayerTreeView(widgetParent)

        self.model=QgsLayerTreeModel(layerTreeRoot)
    
        #self.model.Flag( QgsLayerTreeModel.UseEmbeddedWidgets )
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.layerTreeView.setModel(self.model)
        self.currentLayer=None
        
        self.setupUi()
        
        self.slider.valueChanged.connect(self.sliderGroup_label.setNum)
        self.slider.valueChanged.connect(self.changeOpacity)
        self.layerTreeView.currentLayerChanged.connect(self.currentLayerChanged)
        

    def lineno(self):
         "Returns the current line number"
         return inspect.currentframe().f_back.f_lineno 

    def setParentWindow(self, parentWindow):
        self.parentWindow=parentWindow 

    def getParentWindow(self):
        return self.parentWindow       

    def setLayerTreeRoot(self, layerTreeRoot):
        self.layerTreeRoot=layerTreeRoot

    def getLayerTreeRoot(self):
        return self.layerTreeRoot

    def setLayerTreeView(self , layerTreeView:QgsLayerTreeView):
        self.layerTreeView=layerTreeView

    def getLayerTreeView(self):
        return self.layerTreeView

    def setupUi(self): 
        self.layout = QVBoxLayout(self) 
        self.layout.setContentsMargins(-1, 1, -1, 1)
        
        self.sliderGroup=self.setSliderGroup(QWidget(self))
        self.layout.addWidget(self.sliderGroup)
    
        self.layout.addWidget(self.layerTreeView)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)

         
    def setSliderGroup(self, widget):
        #print(f"line:{self.lineno()},TnTLayerTreeView->setSliderGroup()")            
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
            
        self.sliderGroup_Layout = QHBoxLayout(widget)
        self.sliderGroup_Layout.setContentsMargins(-1, 1, -1, 1)
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.sliderGroup_Layout.addItem(spacerItem)
        
        self.slider = QSlider(QtCore.Qt.Horizontal,widget)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(25)
        self.slider.setTickPosition(QSlider.TicksAbove) 
        self.slider.setPageStep(25)
        self.slider.setSingleStep(5)    
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.slider.setSizePolicy(sizePolicy)
        
        self.slider.setValue(100)
        self.sliderGroup_Layout.addWidget(self.slider)
        
        self.sliderGroup_label = QLabel(widget)               
        self.sliderGroup_label.setNum(self.slider.value())
        self.sliderGroup_label.setSizePolicy(sizePolicy)
        self.sliderGroup_Layout.addWidget(self.sliderGroup_label)
              
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.sliderGroup_Layout.addItem(spacerItem1)
       
        return widget
    
    def hideNodes(self, layerTreeView , model, listNodes):
        #print(f"line:{self.lineno()},TnTLayerTreeView->hideNodes(layerTreeView:{layerTreeView}, model:{model}, listNodes:{listNodes})") 
        for node in listNodes :
            index = model.node2index( node )
            layerTreeView.setRowHidden( index.row(), index.parent(), True )
            node.setCustomProperty( 'nodeHidden', 'true')
            layerTreeView.setCurrentIndex(model.node2index(self.layerTreeRoot))
            
    #def printCurrentOpacity(self):
        #print(f"line:{self.lineno()},TnTLayerTreeView->printCurrentOpacity()") 


    def changeOpacity(self):
        #print(f"line:{self.lineno()},TnTLayerTreeView->changeOpacity()")      
        op=self.slider.value()/100
        if isinstance(self.currentLayer, QgsRasterLayer): self.currentLayer.renderer().setOpacity(op)
        elif isinstance(self.currentLayer, QgsVectorLayer): self.currentLayer.setOpacity(op)
        self.getParentWindow().getCanvas().refresh()
        
    def currentLayerChanged (self, layer):
        #print(f"line:{self.lineno()},TnTLayerTreeView->currentLayerChanged(layer:{layer}") 
        self.currentLayer=layer
        op=0
        if isinstance(self.currentLayer, QgsRasterLayer): op=self.currentLayer.renderer().opacity()         
        elif isinstance(self.currentLayer, QgsVectorLayer): op=self.currentLayer.opacity()
        self.slider.setValue(op*100)
       
    