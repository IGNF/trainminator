# -*- coding: utf-8 -*-/
"""
/***************************************************************************
TnT_AdditionalView
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

from qgis.core import QgsProject
from qgis.gui import QgsLayerTreeMapCanvasBridge


from PyQt5           import  QtCore
from PyQt5.QtGui     import (QIcon, QPixmap)
from PyQt5.QtWidgets import (QSizePolicy, QWidget, QMainWindow, 
                             QPushButton, QVBoxLayout, QGridLayout, 
                             QHBoxLayout, QSpacerItem, QGroupBox, 
                             QDockWidget)

   
from .TnT_MapCanvas import TnTmapCanvas
from .TnT_LayerTreeView import TnTLayerTreeView
from .TnT_Communicate import TnTcommunicate



class TnTadditionalView(QMainWindow):
   
    def __init__(self, parent=None):
        #QMainWindow.__init__(self, parent)
        super(TnTadditionalView, self).__init__(parent)
        
        self.comm = TnTcommunicate()
        self.comm.closeAdditionalView.connect(self.close)
        
        self.windowParent=parent
        self.tntLayerTreeView=None    
        self.canvas=None      
            
        self.setupUi()
        
        self.setWindowFlags(self.windowFlags() # reuse initial flags
                            & ~QtCore.Qt.WindowCloseButtonHint # and unset flag
                           )
        self.show()
        
    def lineno(self):
         "Returns the current line number"
         return inspect.currentframe().f_back.f_lineno 
     
    def flocals(self):   
        return inspect.currentframe().f_back.f_locals["self"]
    
    def module(self):   
        return inspect.getmodule(self)


    def setCanvas(self, canvas=None):
        self.canvas=canvas
        
    def getCanvas(self):
        return self.canvas
        
    def unsetCanvas(self):
        self.setCanvas()
              
    def setSlave(self, slave=None):
        #print(f"{self.lineno()}-{self.flocals()} TnTadditionalView : Passe setSlave()")
        #self.canvas=None
        self.canvas.setSlave(slave)
        
    def unsetSlave(self):
        #print(f"{self.lineno()} TnTadditionalView : Passe unsetSlave()")
        self.canvas=None
        #self.setSlave()
        
    def getSlave(self):
        #print(f"{self.lineno()} TnTadditionalView : Passe getSlave()")
        return None
        #return self.canvas.getSlave()
    
    def setupUi(self):
        self.setObjectName("Additional View")
        self.resize(1300, 900)
        
        self.centralwidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        
        self.verticalLayout = QVBoxLayout(self.centralwidget)
               
        self.topWidget = self.setTopWidget( QWidget(self.centralwidget) )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topWidget.sizePolicy().hasHeightForWidth())
        self.topWidget.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.topWidget) 
        
        self.widget_middle = QWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_middle.sizePolicy().hasHeightForWidth())
        self.widget_middle.setSizePolicy(sizePolicy)
        self.widget_middle.setObjectName("widget_middle")
        self.horizontalLayout_middle = QHBoxLayout(self.widget_middle)
        self.horizontalLayout_middle.setObjectName("horizontalLayout_middle") 
        
        self.canvas=TnTmapCanvas(self.widget_middle, 
                                 "Canvas_AdditionalView") 
                                    
        self.horizontalLayout_middle.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.widget_middle)
        self.setCentralWidget(self.centralwidget)
       
        self.dockWidget_west = QDockWidget(self)
        
        self.dockWidget_west.setFeatures(self.dockWidget_west .features() & ~QDockWidget.DockWidgetClosable)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_west.sizePolicy().hasHeightForWidth())
        self.dockWidget_west.setSizePolicy(sizePolicy)
       
        self.dockWidgetContents_west = QWidget()
        self.gridLayout_west = QGridLayout(self.dockWidgetContents_west)

        #Used clone of initial layerRoot:
        # Allows the selection of layers without affecting the state of the project LayerTreeRoot 
        self.tntLayerTreeView=TnTLayerTreeView( self, self.dockWidgetContents_west, QgsProject.instance().layerTreeRoot().clone() )
        self.tntLayerTreeView.setParentWindow(self)

        #sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tntLayerTreeView.sizePolicy().hasHeightForWidth())
        self.tntLayerTreeView.setSizePolicy(sizePolicy)
        self.gridLayout_west.addWidget(self.tntLayerTreeView, 0, 0, 1, 1)
               
        self.dockWidget_west.setWidget(self.dockWidgetContents_west)

        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_west)
        
        self.layerTreeMapCanvasBridge=QgsLayerTreeMapCanvasBridge(self.tntLayerTreeView.getLayerTreeRoot(), self.getCanvas())
        
        self.centerAll_pushButton.clicked.connect( self.centerAll )
        #Calling <synchro_AdditionalView()> method, on clicking button <synchro_pushButton>
        self.synchro_pushButton.clicked.connect( self.synchro_AdditionalView ) 
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, target):
        _translate = QtCore.QCoreApplication.translate
        target.setWindowTitle(_translate("Additional View", "Additional View"))
        
    
    def setTopWidget(self, widget):
        
        # Init layout of this widget_top
        self.verticalLayout_top = QVBoxLayout(widget)
        self.verticalLayout_top.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_top.setSpacing(0)
           
        # Init Group box contains buttons which manage additional view
        self.groupBox_view = QGroupBox(widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_view.sizePolicy().hasHeightForWidth())
        self.groupBox_view.setSizePolicy(sizePolicy)
        
        self.horizontalLayout_view = QHBoxLayout(self.groupBox_view)
        self.horizontalLayout_view.setContentsMargins(4, 2, 4, 2)
        self.horizontalLayout_view.setSpacing(4)         
        
        
        self.centerAll_pushButton = QPushButton(self.groupBox_view)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerAll_pushButton.sizePolicy().hasHeightForWidth())
        self.centerAll_pushButton.setSizePolicy(sizePolicy)
        
        self.centerAll_pushButton.setText("Center ALL")
        self.centerAll_pushButton.setIconSize(QtCore.QSize(22, 22))
        self.horizontalLayout_view.addWidget(self.centerAll_pushButton)
        
    
        # Spacer : push all  buttons on right side
        spacerItem = QSpacerItem(558, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_view.addItem(spacerItem)
                  
        self.synchro_pushButton = QPushButton(self.groupBox_view)  
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.synchro_pushButton.sizePolicy().hasHeightForWidth())
        self.synchro_pushButton.setSizePolicy(sizePolicy)
            
        self.synchro_pushButton.setText("Synchro View")
        self.synchro_pushButton.setCheckable(True)
        self.synchro_pushButton.setChecked(False)
        
        self.horizontalLayout_view.addWidget(self.synchro_pushButton)
        self.verticalLayout_top.addWidget(self.groupBox_view)
      
        return widget
     
    
    def synchro_AdditionalView(self):  
        # Change state of button Synchro/UnSynchro         
        self.toggleTextButton(self.synchro_pushButton, "Synchro View", "UnSynchro View")
        
        wp=self.windowParent
        # Force checked for toggleTextButton() method
        wp.synchro_pushButton.setChecked( not wp.synchro_pushButton.isChecked() )
        wp.toggleTextButton(wp.synchro_pushButton, "Synchro View", "UnSynchro View")
        
        wp.getActiveCanvas().toggleStateSynchroMode()
        self.getCanvas().toggleStateSynchroMode()
        
        
        
    def toggleTextButton(self, pushButton, textON, textOFF):
        t=(lambda:textON, lambda:textOFF)[pushButton.isChecked()]()
        pushButton.setText(t)
        
    
    def toggleIconButton(self, pushButton, offStateImpage, onStateImage, sizeIcon):
    	icon = QIcon()
    	# 'Off' state = unchecked state of pushButton
    	icon.addPixmap( QPixmap( offStateImpage ), QIcon.Normal, QIcon.Off )
    	# 'On' state = checked state of pushButton
    	icon.addPixmap( QPixmap( onStateImage ), QIcon.Normal, QIcon.On )
    	pushButton.setIcon( icon )
    	pushButton.setIconSize(sizeIcon)
    	pushButton.setCheckable( True )
        
           
    def centerAll(self):
        self.getCanvas().zoomToFullExtent()
        
    
    