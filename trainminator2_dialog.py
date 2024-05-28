#♠-*- coding: utf-8 -*-
"""
/***************************************************************************
 TraiNminaTor2Dialog
                                 A QGIS plugin
 Plugin de labellisation
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-06-02
        git sha              : $Format:%H$
        copyright            : (C) 2023 by IGN
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
import os


from qgis.core import QgsProject
from qgis.PyQt.QtCore import( QFile )

from PyQt5.QtCore import( Qt, QEvent )
from PyQt5 import QtCore
from PyQt5 import QtGui

from PyQt5.QtWidgets import( QFileDialog, QMenuBar, QMainWindow,
                             QTreeWidget, QLabel)

from .TnT_WidgetsGroup import( menu_widget, 
                               TnTnomenclatureWidget,
                               TnTnomenclatureWidget_Master,
                               TnTLayerTreeWidget,
                               sliderGroup,
                               mergeToolsGroup,
                               selectingToolsGroup,
                               startStopToolsGroup
                             )

from .TnT_DockWidget import( TnTLayerTree_DockWidget,
                             TnTLayerTree_DockWidget_Master,
                             TnTNomenclature_DockWidget,
                             TnTNomenclature_DockWidget_Master
                           )
from .trainminator2_Widget import( TraiNminaTor2Widget_Base,
                                   TraiNminaTor2Widget_Differential,
                                   TraiNminaTor2Widget_Master
                                 )
from .TnT_ProjectManager import TnTProjectManager
from .debug.logger import get_logger
logger = get_logger()

def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno

class TraiNminaTor2Dialog_Base(QMainWindow):
    def __init__( self,
                  parent = None,
                  objectName="TraiNminaTor2Dialog_Base"
                ):

        super().__init__( parent )
        self.setWindowFlags(
            self.windowFlags()  # reuse initial flags
        )
        self.setObjectName(objectName)
        self.setAccessibleName(objectName)
        self.vintage = None
        self.checkPatchCompletionDisabled = False
        self.IRC = False
        self.main_ortho = True

        self.resize(1300, 900)
        self.setStyleSheet()

        self.setupUi()

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.initCentralWidget()
        self.setUpLayerTreeView_dockWidget(QtCore.Qt.DockWidgetArea(1))

    def initCentralWidget( self ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        centralWidget = TraiNminaTor2Widget_Base(parent=self)
        self.setCentralWidget(centralWidget)

    def setStyleSheet(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        css_File="css/Default.css"
        cssFile=os.path.join(os.path.dirname(__file__), css_File)
        rc = QFile(cssFile)
        rc.open(QFile.ReadOnly)
        content = rc.readAll().data()
        super().setStyleSheet(str(content, "utf-8"))

    def setUpLayerTreeView_dockWidget(self, position:int):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        dockWidget = self.initLayerTreeView_dockWidget()
        self.addDockWidget(Qt.DockWidgetArea(position), dockWidget)

    def initLayerTreeView_dockWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        dockWidget = TnTLayerTree_DockWidget(parent=self)
        return dockWidget
    
    def setVintage(self, vintage:str=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.vintage = None
        
    def getVintage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return None
    
    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        pass
    
    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass
     
    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass
         
    def getDockWidget(self, typeDock):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()") 
        
        dockWidget = self.findChild(typeDock)
        return dockWidget

    def getSelectingToolGroupWidget(self):
        selectingToolGroupWidget =  self.findChild(selectingToolsGroup)
        return selectingToolGroupWidget
    
    def getTnTnomenclatureWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        nomenclatureWidget =  self.findChild(TnTnomenclatureWidget)
        return nomenclatureWidget
    
    def getTnTLayerTreeWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget =  self.findChild(TnTLayerTreeWidget)
        return layerTreeWidget

    def getSliderGroup(self):
        sliderGroupWidget = self.findChild(sliderGroup)
        return sliderGroupWidget
    
    
    def start_SliderGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.centralWidget().start_SliderGroup()

            
    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
         
        # layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        # layerTreeView_dock.start()
        
        # self.centralWidget().start()
        pass
    
    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        # self.centralWidget().stop()
        
        # layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        # layerTreeView_dock.stop()
        pass
    

    def showContext(self, showContext:bool=False, keepGroup:str="CONTEXT"):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.showContext(showContext=showContext, keepGroup=keepGroup)

    
    def change_IRC_RGB(self):
        self.IRC = not self.IRC
        
        vintage = self.getVintage()
        if vintage:
            context = f"CONTEXT_{vintage}"
        else:
            context = "CONTEXT"
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeWidget = layerTreeView_dock.findChild(TnTLayerTreeWidget)
        layerTreeWidget.change_IRC_RGB(context)


    def getContextNBBands(self):
        vintage = self.getVintage()
        if vintage:
            context = f"CONTEXT_{vintage}"
        else:
            context = "CONTEXT"
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeWidget = layerTreeView_dock.findChild(TnTLayerTreeWidget)
        return layerTreeWidget.getContextNBBands(context)



        
        
               
class TraiNminaTor2Dialog_Differential(TraiNminaTor2Dialog_Base):
    def __init__( self,
                  parent = None,
                  objectName="TraiNminaTor2Dialog_Differential"
                ):
        super().__init__( parent = parent,
                          objectName = objectName
                        )
        
    def setupUi(self):
        self.initCentralWidget()
        self.setUpLayerTreeView_dockWidget(QtCore.Qt.DockWidgetArea(1))
        self.setUpNomenclature_dockWidget(QtCore.Qt.DockWidgetArea(2))

    def initCentralWidget( self ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        centralWidget = TraiNminaTor2Widget_Differential(parent=self)
        self.setCentralWidget(centralWidget)

    def setUpNomenclature_dockWidget(self, position:int):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        dockWidget = self.initNomenclature_dockWidget()
        self.addDockWidget(Qt.DockWidgetArea(position), dockWidget)

    def initNomenclature_dockWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        dockWidget = TnTNomenclature_DockWidget(parent=self)
        return dockWidget
    
    
    def setVintage(self, vintage:str=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.vintage = vintage
        
    def getVintage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return self.vintage 
    
    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass
     
    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.centralWidget().differentialMode()
        
        nomenclature_dock = self.getDockWidget(TnTNomenclature_DockWidget)
        nomenclature_dock.differentialMode()
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.differentialMode()
        
        # And show it
        self.show()
    
    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        tntlayers_Manager = self.parent().projectManager.tnTProjectObject   
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.start(tntlayers_Manager=tntlayers_Manager)
         
        self.centralWidget().start()
        
    
    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        tntlayers_Manager = self.parent().projectManager.tnTProjectObject
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.stop(tntlayers_Manager=tntlayers_Manager)
        
        self.centralWidget().stop()

    
    def showCurrentClass(self, showCurrentClass:bool=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.showCurrentClass(showCurrentClass=showCurrentClass)


    def disableCheckPatchCompletion(self, disableCheckPatchCompletion):
        self.checkPatchCompletionDisabled = disableCheckPatchCompletion
   
        
    def currentNomenclatureChanged(self,
                                   nomenclatureName:str = None,
                                   treeWidgetSrc:QTreeWidget = None
                                   ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclature_DockWidget = self.getDockWidget(
            TnTNomenclature_DockWidget
        )
        
        nomenclature_DockWidget.currentNomenclatureChanged(
            treeWidgetSrc=treeWidgetSrc
        )
        
        self.centralWidget().currentNomenclatureChanged(
            nomenclatureName=nomenclatureName
        )

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent().close()

class TraiNminaTor2Dialog_Master(TraiNminaTor2Dialog_Differential):

    def __init__(self,
                 parent=None,
                 objectName="TraiNminaTor2Dialog_Master"
                 ):
        super().__init__(parent=parent,
                         objectName=objectName
                         )

        self.associatedWindow = TraiNminaTor2Dialog_Base(self)
        self.projectManager = TnTProjectManager(self)

        self.setConnections()

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.initCentralWidget()
        self.setUpMenus()
        self.setUpLayerTreeView_dockWidget(QtCore.Qt.DockWidgetArea(1))
        self.setUpNomenclature_dockWidget(QtCore.Qt.DockWidgetArea(2))

    def initCentralWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        centralWidget = TraiNminaTor2Widget_Master(parent=self)
        self.setCentralWidget(centralWidget)

    def get_start_stop_group(self):
        start_stop_group = self.findChild(startStopToolsGroup, name='startStopToolsGroup')
        return start_stop_group

    def initLayerTreeView_dockWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        dockWidget = TnTLayerTree_DockWidget_Master(parent=self)
        return dockWidget

    def initNomenclature_dockWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        dockWidget = TnTNomenclature_DockWidget_Master(parent=self)
        return dockWidget
    
    
    def getVintages(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
    
        projectManager = self.projectManager
        return projectManager.getVintages()

    def get_merge_tools_group(self):
        return self.findChild(mergeToolsGroup, "mergeToolsGroup")

    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        # Delete window if instance of TraiNminaTor2Dialog_Differential
        if isinstance(self.associatedWindow,
                      TraiNminaTor2Dialog_Differential):
            self.associatedWindow.hide()
            self.associatedWindow.close()
            self.associatedWindow = None

        # Instantiate TraiNminaTor2Dialog_Base window if not already exist
        if not self.associatedWindow:
            self.associatedWindow = TraiNminaTor2Dialog_Base(self)

        self.centralWidget().standardMode()

        labels_year1 = self.findChildren(QLabel, "label_year1_class")[0]
        labels_year1.hide()
        # do not show it. the user decides if he wants to see it or not.

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")

        # Delete window if instance of TraiNminaTor2Dialog_Base
        if isinstance(self.associatedWindow, TraiNminaTor2Dialog_Base):
            self.associatedWindow.hide()
            self.associatedWindow.close()
            self.associatedWindow = None

        # Instantiate TraiNminaTor2Dialog_Differential window
        # if not already exist
        if not self.associatedWindow:
            self.associatedWindow = TraiNminaTor2Dialog_Differential(self)

        projectManager = self.projectManager
        vintages = projectManager.getVintages()
        
        vintages = self.getVintages()
        oldest_vintage = vintages[0]
        recentest_vintage = vintages[1]
        
        self.setVintage(vintage=recentest_vintage)
        self.centralWidget().differentialMode()

        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.differentialMode()

        nomenclature_dock = self.getDockWidget(TnTNomenclature_DockWidget)
        nomenclature_dock.differentialMode()
        

        self.associatedWindow.setVintage(vintage=oldest_vintage)
        self.associatedWindow.differentialMode()

    def currentNomenclatureChanged(self,
                                   nomenclatureName: str = None,
                                   treeWidgetSrc: QTreeWidget = None
                                   ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.centralWidget().currentNomenclatureChanged(
            nomenclatureName=nomenclatureName
        )

        if self.projectManager.isDifferential:
            self.associatedWindow.currentNomenclatureChanged(
                nomenclatureName=nomenclatureName,
                treeWidgetSrc=treeWidgetSrc
            )
        
        
    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.associatedWindow.start()

        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        tntlayers_Manager = self.projectManager.tnTProjectObject
        layerTreeView_dock.start(tntlayers_Manager=tntlayers_Manager)

        self.centralWidget().start()
        
        self.start_SliderGroup()

        if self.projectManager.isDifferential:
            self.associatedWindow.start_SliderGroup()
        
    
    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        tntlayers_Manager = self.projectManager.tnTProjectObject
        layerTreeView_dock.stop(tntlayers_Manager=tntlayers_Manager)

        self.associatedWindow.stop()
        self.centralWidget().stop()

    def showCurrentClass(self, showCurrentClass:bool=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeView_dock.showCurrentClass(showCurrentClass=showCurrentClass)

        if self.projectManager.isDifferential:
            self.associatedWindow.showCurrentClass(showCurrentClass=showCurrentClass)

    
    def switch_ortho(self):
        self.main_ortho = not self.main_ortho

        vintage = self.getVintage()
        if vintage:
            main_context = f"CONTEXT_{vintage}"
        else:
            main_context = "CONTEXT"

        vintage = self.associatedWindow.getVintage()
        if vintage:
            associated_context = f"CONTEXT_{vintage}"
        else:
            associated_context = "CONTEXT"

        if self.main_ortho:
            new_context = main_context
            old_context = associated_context
        else:
            new_context = associated_context
            old_context = main_context
        
        layerTreeView_dock = self.getDockWidget(TnTLayerTree_DockWidget)
        layerTreeWidget = layerTreeView_dock.findChild(TnTLayerTreeWidget)
        layerTreeWidget.switch_ortho(new_context, old_context)

        
    def setUpMenus(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        menu_bar = QMenuBar(self)
        menu_bar.setObjectName(f"menuBar_{self.objectName()}")
        menu_bar.setAccessibleName(f"menuBar_{self.objectName()}")
        self.setMenuBar(menu_bar)

        self.setupMenuNomenclature()
        self.setupMenuTools()
        self.setupMenuHelp()

    def initMenu(self,
                 title="no_title",
                 menuBar: QMenuBar = None,
                 objectName="menu"
                 ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        menu = menu_widget(
            title=title,
            menuBar=menuBar,
            objectName=objectName
        )
        return menu

    def setupMenuNomenclature(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        title = "Nomenclature"
        menu = self.initMenu(
            title=title,
            menuBar=self.menuBar(),
            objectName=f"menu_{title}"
        )

        text = 'Open Nomenclatures'
        action = menu.createAction(
            text=text,
            objectName=f"action_{text.replace(' ','')}",
            shortcut='Ctrl+O',
            statusTip=text
        )
        action.triggered.connect(self.openNomenclatures)

    def openNomenclatures(self):
        """
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        where = QgsProject.instance().absolutePath()
        if os.path.exists(where+"/NOMENCLATURE"):
            where = where+"/NOMENCLATURE"

        filterName = 'Nomenclature File (*.csv)'
        nomenclatures = QFileDialog.getOpenFileNames(
            self,
            'Open Nomenclatures',
            where,
            filterName
        )

        #Keep only files (reject filterName)
        nomenclatureFiles = nomenclatures[0]
        if nomenclatureFiles:
            """
            On fixe la nomenclature ici
            """
            nomenclatureWidget = self.findChild(
                TnTnomenclatureWidget_Master,
                "TnTnomenclatureWidget_Master"
            )
            logger('set nomenclature')
            nomenclatureWidget.setNomenclaturesDict(nomenclatureFiles)
            #user chose nomenclature, unlock group

        else:
            pass

    def setupMenuTools(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        title = "Tools"
        menu = self.initMenu(
            title=title,
            menuBar=self.menuBar(),
            objectName=f"menu_{title}"
        )

        text = 'Chart tool'
        action = menu.createAction(
            text=text,
            objectName=f"action_{text.replace(' ','')}",
            shortcut='Ctrl+C',
            statusTip=text
        )
        action.triggered.connect(self.startChartTool)

        text = 'Control tool'
        action = menu.createAction(
            text=text,
            objectName=f"action_{text.replace(' ','')}",
            shortcut='Ctrl+V',
            statusTip=text
        )
        action.triggered.connect(self.startControlTool)

    def setupMenuHelp(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        title = "Help"
        menu = self.initMenu(
            title=title,
            menuBar=self.menuBar(),
            objectName=f"menu_{title}"
        )
        
        text = 'Open Documentation'
        action = menu.createAction(
            text=text,
            objectName=f"action_{text.replace(' ','')}",
            shortcut='Ctrl+H',
            statusTip=text
        )

        action.triggered.connect(self.openDocumentation)

    def startChartTool(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def startControlTool(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def openDocumentation(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.projectManager.project.readProject.disconnect()
        self.associatedWindow.destroy()
        self.destroy()
        QgsProject.instance().clear()