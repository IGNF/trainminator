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

from qgis.gui import ( QgsMapCanvas, QgsLayerTreeMapCanvasBridge )
from qgis.core import QgsProject

from PyQt5.QtGui import ( QShowEvent )
from PyQt5.QtCore import ( Qt, QEvent )

from PyQt5.QtWidgets import ( QSizePolicy, QVBoxLayout, QHBoxLayout,
                              QGroupBox, QMainWindow, QTreeWidgetItem,
                              QTreeWidget, QPushButton
                            )

from .TnT_WidgetsGroup import ( toolsGroup_Base,
                                toolsGroup_Differential,
                                toolsGroup_Master,
                                viewsManagerGroup,
                                viewsManagerGroup_Master,
                                infoSelectionGroup,
                                sliderGroup,
                                startStopToolsGroup,
                                selectingToolsGroup,
                                displayToolsGroup,
                                displayLabelsGroup,
                                mergeToolsGroup,
                                taskToolsGroup
                              )

from .TnT_MapCanvas import mapCanvas

# This loads your .ui file so that PyQt can populate your plugin with
# the elements from Qt Designer
# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'trainminator2_dialog_base.ui'))

def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno


class TraiNminaTor2Widget_Base(QGroupBox):
    """ QMainWindow base """
    def __init__( self,
                  parent = None,
                  objectName="TraiNminaTor2Widget_Base"
                 ):
        """Constructor."""
        super().__init__(parent)

        self.setObjectName(objectName)
        self.setAccessibleName(objectName)

        self.groupsTypeList=[]
        self.setGroupsTypeList()

        self.canvas = None
        self.bridge = None

        self.setupLayout()
        self.setDefaultSizePolicy()

        self.setupUi()


    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout=QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)


    def setupUi(self):
        """
        Returns
        -------
        None.

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setUpViewsManagerGroup()
        self.setUpSliderGroup()
        self.setUpInfoSelectionGroup()
        self.setUpCanvasZoneGroup()

        self.lockGroupByType()
      

    def setDefaultSizePolicy(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sizePolicy = QSizePolicy( QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)


    def setGroupsTypeList(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.groupsTypeList=[ viewsManagerGroup ]


    def getGroupsTypeList(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.groupsTypeList


    def lockGroupByType(self, groupsTypeList=None) :
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if not groupsTypeList :
            groupsTypeList=self.getGroupsTypeList()

        for groupType in groupsTypeList :
            group = self.findChild(groupType)
            group.setEnabled(False)


    def unlockGroupByType(self, groupsTypeList=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if not groupsTypeList :
            groupsTypeList=self.getGroupsTypeList()

        for groupType in groupsTypeList :
            group = self.findChild(groupType)
            group.setEnabled(True)


    def setUpViewsManagerGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()
        viewsManager_Group = self.initViewsManagerGroup(parent=self)
        layout.addWidget(viewsManager_Group)


    def getCanvasZoneGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        canvasZone_Group = self.findChild(
            QGroupBox,
            "canvasZoneGroup"
        )
        return canvasZone_Group


    def initViewsManagerGroup(self, parent=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        viewsManager_Group = viewsManagerGroup(parent=parent)
        return viewsManager_Group


    def setUpSliderGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def initSliderGroup(self, parent=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def setUpInfoSelectionGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def initInfoSelectionGroup(self, parent=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def setUpCanvasZoneGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        canvasZone_Group =self.initCanvasZoneGroup()
        mapcanvas = self.initMapCanvas(canvasZone_Group)
        canvasZone_Group.layout().addWidget(mapcanvas)

        layout = self.layout()
        layout.addWidget(canvasZone_Group)


    def initCanvasZoneGroup(self):
        """
        This zone is a sous group which contains a
        mapcanvas and the tools.

        Returns
        -------
        sub_group : TYPE
            DESCRIPTION.

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sub_group = QGroupBox(self)
        sub_group.setObjectName("canvasZoneGroup")
        sub_group.setAccessibleName("canvasZoneGroup")

        sub_group_layout = QHBoxLayout(sub_group)
        sub_group.setLayout(sub_group_layout)

        return sub_group


    def initMapCanvas(self, parent):
        """ """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        map_Canvas = mapCanvas(parent)
        return map_Canvas


    def initLayerTreeMapCanvasBridge(self):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        mainWindow = self.getMainWindow()
        layerTreeWidget = mainWindow.getTnTLayerTreeWidget()
        root = layerTreeWidget.layerTreeRoot()

        canvas = self.findChild(QgsMapCanvas, "mapCanvas")
        self.bridge = QgsLayerTreeMapCanvasBridge(root, canvas)
        #self.bridge.setAutoSetupOnFirstLayer(True)


    def removeLayerTreeMapCanvasBridge(self):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        del self.bridge


    def getMainWindow(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        parent = self.parent()
        while not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent


    def getMasterWindow(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        parent = self.parent()
        while parent.objectName()!="TraiNminaTor2Dialog_Master" :
            parent = parent.parent()
        return parent


    # def initCaptureConnections(self):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")

    #     pass


    def currentNomenclatureChanged( self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                  ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def itemSelectionChanged(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def standardMode(self):
        """ nothing to do pass """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        # here unlock viewsManagerGroup
        self.unlockGroupByType(groupsTypeList=[viewsManagerGroup])

        group = self.findChild(viewsManagerGroup)

        layout = group.layout()
        synchro_Views_pushButton = group.findChild(QPushButton, "synchro_Views")
        layout.removeWidget(synchro_Views_pushButton)

        synchro_Levels_pushButton = group.findChild(QPushButton, "synchro_Levels")
        layout.removeWidget(synchro_Levels_pushButton)


    def differentialMode(self):
        """ Update viewsManagerGroup by calling differentialMode method """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        # here unlock viewsManagerGroup
        self.unlockGroupByType(groupsTypeList=[viewsManagerGroup])


    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass

    def event(self, event:QEvent) -> bool:
        
        evt_Type=event.type()
        if (evt_Type==QEvent.KeyRelease or evt_Type==QEvent.KeyPress) and event.key()==Qt.Key_W:
            masterWindow = self.getMasterWindow()

            showContext = evt_Type==QEvent.KeyPress
            vintage = masterWindow.getVintage()
            if vintage:
                keepGroup = f"CONTEXT_{vintage}"
            else:
                keepGroup = "CONTEXT"
            masterWindow.showContext(showContext=showContext, keepGroup=keepGroup)

            associatedWindow = masterWindow.associatedWindow
            vintage = associatedWindow.getVintage()
            if vintage:
                keepGroup = f"CONTEXT_{vintage}"
            else:
                keepGroup = "CONTEXT"
            associatedWindow.showContext(showContext=showContext, keepGroup=keepGroup)
        return super().event(event)


class TraiNminaTor2Widget_Differential(TraiNminaTor2Widget_Base):

    """ QMainWindow in differential mode."""
    def __init__( self,
                  parent = None,
                  objectName="TraiNminaTor2Widget_Differential",
                ):
        """Constructor."""
        super().__init__( parent = parent,
                          objectName = objectName
                         )

        self.setTitle("TraiNminaTor2Widget_Differential")

     # def setUpViewsManagerGroup(self):
     #     "Already implement in mother class."

     # def initViewsManagerGroup(self):
     #     "Already implement in mother class."

    def setGroupsTypeList(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.groupsTypeList=[ sliderGroup,
                              infoSelectionGroup,
                              taskToolsGroup,
                              selectingToolsGroup,
                              displayLabelsGroup
                            ]


    def setUpSliderGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()
        slider_Group = self.initSliderGroup(parent=self)
        layout.addWidget(slider_Group)


    def initSliderGroup(self, parent=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        slider_Group = sliderGroup(parent=parent)
        return slider_Group


    def setUpInfoSelectionGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()
        infoSelection_Group = self.initInfoSelectionGroup(parent=self)
        layout.addWidget(infoSelection_Group)


    def initInfoSelectionGroup(self, parent=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        infoSelection_Group = infoSelectionGroup(parent=parent)
        return infoSelection_Group


    def setUpCanvasZoneGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().setUpCanvasZoneGroup()

        tools_Group =self.initToolsGroup()
        layout = tools_Group.parent().layout()
        layout.addWidget(tools_Group)


    def initToolsGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        canvasZone_Group = self.getCanvasZoneGroup()
        tools_Group = toolsGroup_Differential(canvasZone_Group)
        return tools_Group


    def currentNomenclatureChanged( self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                   ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        infoSelection_Group = self.findChild(infoSelectionGroup)
        infoSelection_Group.currentNomenclatureChanged(
                                        nomenclatureName=nomenclatureName
                                                      )


    def itemSelectionChanged(self, itemSelected:QTreeWidgetItem=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        infoSelection_Group = self.findChild(infoSelectionGroup)
        infoSelection_Group.itemSelectionChanged(
                                          itemSelected = itemSelected
                                                )

    def start_SliderGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        slider_Group = self.findChild(sliderGroup)
        slider_Group.start()

    def standardMode(self):
        """ nothing to do pass """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().standardMode()
        mainWindow = self.getMainWindow()
        layerTreeWidget = mainWindow.getTnTLayerTreeWidget()
        root = layerTreeWidget.layerTreeRoot()

        canvas = self.findChild(QgsMapCanvas, "mapCanvas")
        self.bridge = QgsLayerTreeMapCanvasBridge(root, canvas)

    def differentialMode(self):
        """ Update viewsManagerGroup by calling differentialMode method """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().differentialMode()
        self.initLayerTreeMapCanvasBridge()
        infoSelection_Group = self.findChild(infoSelectionGroup)
        infoSelection_Group.differentialMode()


    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        tools_Group = self.findChild(toolsGroup_Base)
        tools_Group.start()


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        slider_Group = self.findChild(sliderGroup)
        slider_Group.stop()

        tools_Group = self.findChild(toolsGroup_Base)
        tools_Group.stop()


class TraiNminaTor2Widget_Master(TraiNminaTor2Widget_Differential):
    """ QMainWindow master."""
    def __init__( self,
                  parent = None,
                  objectName="TraiNminaTor2Widget_Differential"
                ):
        """Constructor."""
        super().__init__( parent = parent,
                          objectName = objectName
                         )
        self.setTitle("TraiNminaTor2Widget_Master")

    # def setUpViewsManagerGroup(self):
    #     "Already implement in mother class."

    def setGroupsTypeList(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.groupsTypeList=[ sliderGroup,
                              infoSelectionGroup,
                              startStopToolsGroup,
                              mergeToolsGroup,
                              taskToolsGroup,
                              selectingToolsGroup,
                              displayToolsGroup,
                              displayLabelsGroup
                             ]

    def initViewsManagerGroup(self, parent=None):
        """Overload mother method """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        viewsManager_Group = viewsManagerGroup_Master(parent=parent)
        return viewsManager_Group


    # def setUpSliderGroup(self):
    #     "Already implement in mother class."

    # def initSliderGroup(self):
    #     "Already implement in mother class."

    # def setUpInfoSelectionGroup(self):
    #     "Already implement in mother class."

    # def initInfoSelectionGroup(self):
    #     "Already implement in mother class."


    def initToolsGroup(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        canvasZone_Group = self.getCanvasZoneGroup()
        tools_Group = toolsGroup_Master(canvasZone_Group)
        return tools_Group


    # def initCaptureConnections(self):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")

    #     pass


    def standardMode(self):
        """ Update viewsManagerGroup by calling standardMode method """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        super().standardMode()
        viewsManager_Group = self.findChild(viewsManagerGroup_Master)
        viewsManager_Group.standardMode()


        mergeTools_Group = self.findChild(mergeToolsGroup)
        mergeTools_Group.setEnabled(True)



    def differentialMode(self):
        """ Update viewsManagerGroup by calling differentialMode method """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        super().differentialMode()
        viewsManager_Group = self.findChild(viewsManagerGroup_Master)
        viewsManager_Group.differentialMode()
        
        #temporaire pour test
        # mergeTools_Group = self.findChild(mergeToolsGroup)
        # mergeTools_Group.setEnabled(True)

    def currentNomenclatureChanged( self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                  ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().currentNomenclatureChanged(
            nomenclatureName=nomenclatureName
        )

        tools_Group = self.findChild(toolsGroup_Base)
        tools_Group.currentNomenclatureChanged()
