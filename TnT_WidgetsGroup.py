"""
Created on Fri Jun  2 11:12:13 2023

@author: YLe-Borgne
"""
import os.path
import csv
import inspect
import sys



from qgis.core import( QgsLayerTreeModel, QgsRasterLayer, QgsVectorLayer,
                       QgsProject, QgsLayerTreeNode, QgsLayerTreeLayer,
                       QgsWkbTypes, QgsRuleBasedRenderer, QgsVectorFileWriter,
                       QgsFillSymbol,QgsField, QgsPalLayerSettings,
                       QgsTextFormat, QgsTextBufferSettings,
                       QgsVectorLayerSimpleLabeling,
                       QgsLinePatternFillSymbolLayer,
                       QgsLineSymbol, QgsSymbol, QgsSimpleFillSymbolLayer, Qgis
                      )

from qgis.gui import ( QgsLayerTreeView )

from PyQt5 import QtCore
from PyQt5.QtCore    import( Qt, QVariant )
from PyQt5.QtGui     import( QColor, QBrush, QPalette,
                             QFont, QKeySequence
                           )

from PyQt5.QtWidgets import( QSizePolicy, QPushButton, QComboBox,
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QGroupBox,
                             QDockWidget, QMenu, QMenuBar,
                             QShortcut, QMainWindow,
                             QLabel, QAction, QSlider,
                             QTreeWidget,  QTreeWidgetItem
                           )

from .TnT_MapCanvas import mapCanvas
from .TnT_CaptureManager import ( TnTmapToolEmitPoint,
                                  TnTmapToolEmitPline,
                                  TnTmapToolEmitPolygon
                                )
from .TnT_ProjectManager import( TnTLayersManager )
from .TnT_SavingLabeledData import ( TnTSavingLabeledData )


def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno

class groupQWidgets(QGroupBox):
    def __init__( self,
                  parent=None,
                  objectName="groupQWidgets"
                 ):
        super().__init__(parent)

        self.setTitle(objectName)
        self.setObjectName(objectName)
        self.setAccessibleName(objectName)

        self.setupLayout()
        self.setDefaultSizePolicy()

        self.setupUi()


    def setupLayout(self):
        layout=QHBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setupUi(self):
        pass

    def setDefaultSizePolicy(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sizePolicy = QSizePolicy( QSizePolicy.Preferred,
                                  QSizePolicy.Minimum
                                )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def getLongName(self, targetName, parentName):
        return f"{targetName}_{parentName}"

    def setConnections(self):
        pass

    def setShortCuts(self):
        pass

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

    def getDockWidgetParent(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        parent = self.parent()
        while not isinstance(parent, QDockWidget):
        # while not parent.objectName().startswith("nomenclature_dockWidget"):
            parent = parent.parent()
        return parent

    def getTnTnomenclatureWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        # masterWindow =self.getMasterWindow()
        # nomenclatureWidget = masterWindow.getTnTnomenclatureWidget()
        
        mainWindow =self.getMainWindow()
        nomenclatureWidget = mainWindow.getTnTnomenclatureWidget()
        
        return nomenclatureWidget

    def getTnTmapToolEmit(self):
        """
        Retrieve the current maptool (ie TnTmapToolEmitPoint,
        TnTmapToolEmitPline or TnTmapToolEmitPolygon) assigned to
        the mapCanvas.

        return : mapToolEmit the current maptool.
        """
        mainWindow =self.getMainWindow()
        map_Canvas = mainWindow.findChild(mapCanvas)
        mapToolEmit = map_Canvas.mapTool()
        return mapToolEmit

    # def getGroupsTypeList(self):
    #     return []


    def getVintage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        pass
    

    def setVintage(self, vintage:str=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        pass
        
    
    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        pass

    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        pass

class groupQPushButton(groupQWidgets):

    def __init__( self,
                  parent = None,
                  objectName = "groupQPushButton",
                  mutually_exclusif = False
                ):

        super().__init__( parent = parent,
                          objectName = objectName,
                        )

        self.setMutuallyExclusif_Connections(mutually_exclusif)

    def setQPushButton( self,
                        button,
                        checkable=False,
                        enabled=True,
                        checked=False,
                        text = None,
                        icon = None,
                        objectName = "None",
                        accessibleName ="None",
                        toolTip=None,
                        keySequence=None
                      ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        button.setCheckable(checkable)
        button.setEnabled(enabled)
        button.setChecked(checked)

        sizePolicy = QSizePolicy( QSizePolicy.Maximum,
                                  QSizePolicy.Maximum
                                )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        button.setSizePolicy(sizePolicy)

        if text :
            button.setText(text)
        if icon :
            button.setIcon(icon)
        button.setObjectName(objectName)
        button.setAccessibleName(accessibleName)

        if toolTip:
            button.setToolTip(toolTip)

        if keySequence:
            shortcut= QShortcut(QKeySequence(keySequence),self)
            shortcut.activated.connect(button.animateClick)

        return button

    def setMutuallyExclusif_Connections(self, mutually_exclusif=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if mutually_exclusif :
            children = self.findChildren(QPushButton)
            for child in children :
                child.clicked.connect(self.mutually_Exclusif)

    def mutually_Exclusif(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sender = self.sender()
        children = self.findChildren(QPushButton)
        children.remove(sender)
        for child in children :
            if isinstance(child, QPushButton):
                child.setEnabled(True)
                child.setChecked(False)

    def animateClickButton(self, textButton):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
  
        button  = self.findChild(QPushButton, textButton)
        button.animateClick()

    def changeVisiblePushButton(self, textButton):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        button  = self.findChild(QPushButton, textButton)
        try :
            currentState = button.isVisible()
            button.setVisible(not currentState)
        except AttributeError :
            pass

    def changeBackGroundColor(self, pushButton, color_one, color_two):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        current_color = pushButton.palette().button().color().name().upper()
        color = (lambda:color_one, lambda:color_two)\
                [current_color==color_one.upper()]()
        pushButton.setStyleSheet(f"background-color: {color}")


    def switchTextButton(self, pushButton, text_one, text_two):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        t = (lambda:text_one, lambda:text_two)[pushButton.text()==text_one]()
        pushButton.setText(t)


    def toggleTextButton(self, pushButton, textOFF, textON):
        """
            param pushButton: The target button whose text we change.
            param textON:
            param textOFF:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        t=(lambda:textOFF, lambda:textON)[pushButton.isChecked()]()
        pushButton.setText(t)

class startStopToolsGroup(groupQPushButton):
    def __init__( self,
                  parent = None,
                  objectName = "startStopToolsGroup",
                  mutually_exclusif = False
                ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                        )
        self.setTitle("startStopToolsGroup")
        self.setConnections()

    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()

        button1 = self.setQPushButton( QPushButton(self),
                                       checkable=False,
                                       enabled=True,
                                       text="Start",
                                       objectName="start",
                                       accessibleName="start",
                                       toolTip="start labeling",
                                       keySequence=None
                                    )
        layout.addWidget(button1)

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        start_pushButton = self.findChild(QPushButton, "start")
        start_pushButton.clicked.connect(self.startAndStop)
        start_pushButton.clicked.connect(self.activateSynchroLevels)
        start_pushButton.clicked.connect(self.activateDisplayLabelsShortcut)

    def startAndStop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        sender = self.sender()
        t = sender.text()
        self.switchTextButton(sender, "Start", "Stop")
        self.changeBackGroundColor(sender, "#1CC88A", '#E74A3B')
        # Execute appropriate method.
        (getattr(self, t.lower()))()


    def activateSynchroLevels(self):
        masterWindow = self.getMasterWindow()
        synchroLevels_Buttons = masterWindow.findChildren(QPushButton, "synchro_Levels")
        for synchroButton in synchroLevels_Buttons:
            synchroButton.setEnabled(True)

    def activateDisplayLabelsShortcut(self):
        masterWindow = self.getMasterWindow()
        
        master_displayLabels = masterWindow.findChild(displayLabelsGroup, "displayLabels_Group")
        differ_displayLabels = masterWindow.associatedWindow.findChild(displayLabelsGroup, "displayLabels_Group")

        master_displayLabels.displayShortcut.setEnabled(True)
        differ_displayLabels.displayShortcut.setEnabled(True)
        
        mapCanvas_list = masterWindow.findChildren(mapCanvas, "mapCanvas")
        for canvas in mapCanvas_list:
            master_displayLabels.displayShortcut.activated.connect(canvas.setDisplayMode)
            differ_displayLabels.displayShortcut.activated.connect(canvas.setDisplayMode)

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        # self.parent().start()
        # self.widgetsToAnimateClick()

        masterWindow=self.getMasterWindow()
        masterWindow.start()

    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        # self.widgetsToAnimateClick()
        # self.parent().stop()

        masterWindow=self.getMasterWindow()
        masterWindow.stop()


class taskToolsGroup(groupQPushButton):
    def __init__( self,
                  parent = None,
                  objectName = "taskToolsGroup",
                  mutually_exclusif = True
                ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                        )
       
        self.setTitle("taskToolsGroup")
        self.setConnections()


    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()

        labeling_Button = self.setQPushButton(
                            QPushButton(self),
                            checkable=True,
                            text="Labeling",
                            objectName="labeling",
                            accessibleName="labeling",
                            toolTip="Labeling selecting entities",
                            keySequence=None
                                             )
        layout.addWidget(labeling_Button)

        delete_All_Button = self.setQPushButton(
                            QPushButton(self),
                            checkable=True,
                            text="Delete All",
                            objectName="delete_All",
                            accessibleName="delete_All",
                            toolTip="Deleting all selecting entities",
                            keySequence=None
                                               )
        layout.addWidget(delete_All_Button)

        delete_Current_Button = self.setQPushButton(
                            QPushButton(self),
                            checkable=True,
                            text="Delete Current",
                            objectName="delete_Current",
                            accessibleName="delete_Current",
                            toolTip="Deleting only current entities",
                            keySequence=None
                                                    )
        layout.addWidget(delete_Current_Button)


    def setConnections(self):
        """
        No connections are necessary.
        The capture manager class check the state of the buttons, and applies
        the method depending on the state of these buttons.
        (see TnTmapToolEmitPoint_V2.processUserInput)
        if button.isChecked
            Labeling-> TnTmapToolEmitPoint_V2.applyClass()
            Delete All-> TnTmapToolEmitPoint_V2.removeAllClass()
            Delete Current-> TnTmapToolEmitPoint_V2.removeCurrentClass()

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setEnabled(True)
        labeling_button = self.findChild(QPushButton,"labeling")
        labeling_button.animateClick()


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        labeling_button = self.findChild(QPushButton,"labeling")
        if not labeling_button.isDown():
            labeling_button.animateClick()

        self.setEnabled(False)


class selectingToolsGroup(groupQPushButton):
    def __init__( self,
                  parent = None,
                  objectName = "selectingToolsGroup",
                  mutually_exclusif = True
                ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                        )
        # self.setTitle("Selecting")
        self.setTitle("selectingToolsGroup")
        self.setConnections()

    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()

        button1 = self.setQPushButton(
                    QPushButton(self),
                    checkable=True,
                    text="Point",
                    objectName="point",
                    accessibleName="point",
                    toolTip="Selecting entities by point",
                    keySequence=None
                                    )
        layout.addWidget(button1)

        button2 = self.setQPushButton(
                    QPushButton(self),
                    checkable=True,
                    text="Line",
                    objectName="line",
                    accessibleName="line",
                    toolTip="Selecting entities by line",
                    keySequence=None
                                    )
        layout.addWidget(button2)

        button3 = self.setQPushButton(
                    QPushButton(self),
                    checkable=True,
                    text="Large-Polygon",
                    objectName="large_Polygon",
                    accessibleName="large_Polygon",
                    toolTip="select the entities that intersect the polygon.",
                    keySequence=None
                                    )
        layout.addWidget(button3)

        button4 = self.setQPushButton(
                    QPushButton(self),
                    checkable=True,
                    text="Strict-Polygon",
                    objectName="strict_Polygon",
                    accessibleName="strict_Polygon",
                    toolTip="select the entities that are in the polygon.",
                    keySequence=None
                                     )
        layout.addWidget(button4)

    def getTask(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        taskTools_Group = self.parent().findChild(taskToolsGroup)
        pushButtons_list = taskTools_Group.findChildren(QPushButton)
        for pushButton in pushButtons_list :
            if pushButton.isChecked():
                return pushButton.text()
        return None

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        mainWindow = self.getMainWindow()
        canvasZone_Group = mainWindow.findChild(QGroupBox, "canvasZoneGroup")
        map_canvas = canvasZone_Group.findChild(mapCanvas, "mapCanvas")

        point_Button = self.findChild(QPushButton, "point")
        point_Button.clicked.connect(
            lambda: (self.enterModePoint(map_canvas))
        )

        line_Button = self.findChild(QPushButton, "line")
        line_Button.clicked.connect(
            lambda: (self.enterModePline(map_canvas))
        )

        largePol_Button = self.findChild(QPushButton, "large_Polygon")
        largePol_Button.clicked.connect(
            lambda: (self.enterModeLPolygon(map_canvas))
        )

        strictPol_Button = self.findChild(QPushButton, "strict_Polygon")
        strictPol_Button.clicked.connect(
            lambda: (self.enterModeSPolygon(map_canvas))
        )

    def enterModePoint(self, canvas=None):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclatureWidget = self.getTnTnomenclatureWidget()
        self.mapTool = TnTmapToolEmitPoint(self,
                                      canvas,
                                      nomenclatureWidget
                                      )
        canvas.setMapTool(self.mapTool)

    def enterModePline(self, canvas=None):
        """
            param canvas:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->\
        #       {inspect.currentframe().f_code.co_name}()")

        nomenclatureWidget = self.getTnTnomenclatureWidget()
        self.mapTool = TnTmapToolEmitPline( self,
                                            canvas,
                                            nomenclatureWidget
                                          )
        canvas.setMapTool(self.mapTool)

    def enterModeSPolygon(self, canvas=None):
        """
            param canvas:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclatureWidget = self.getTnTnomenclatureWidget()
        self.mapTool = TnTmapToolEmitPolygon( self,
                                              canvas,
                                              nomenclatureWidget,
                                              strictMode=True
                                            )
        canvas.setMapTool(self.mapTool)

    def enterModeLPolygon(self, canvas=None):
        """
            param canvas:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclatureWidget = self.getTnTnomenclatureWidget()
        self.mapTool = TnTmapToolEmitPolygon( self,
                                              canvas,
                                              nomenclatureWidget,
                                              strictMode=False
                                            )
        canvas.setMapTool(self.mapTool)

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setEnabled(True)

        point_button = self.findChild(QPushButton,"point")
        point_button.animateClick()


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        point_button = self.findChild(QPushButton,"point")
        if not point_button.isDown() :
            point_button.animateClick()

        self.setEnabled(False)


class displayToolsGroup(groupQPushButton):
    def __init__( self,
                  parent = None,
                  objectName = "displayToolsGroup",
                  mutually_exclusif = False
                ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                        )
        # self.setTitle("Display")
        self.setTitle("displayToolsGroup")

        self.setConnections()

    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()

        button1 = self.setQPushButton(QPushButton(self),
                                      checkable=True,
                                      text="Show Current",
                                      objectName="show_Current",
                                      accessibleName="show_Current",
                                      toolTip="Show only cuurent class.",
                                      keySequence=None
                                      )
        button1.setEnabled(False)
        layout.addWidget(button1)

        button2 = self.setQPushButton(QPushButton(self),
                                      checkable=True,
                                      text="Show Codes",
                                      objectName="show_Codes",
                                      accessibleName="show_Codes",
                                      toolTip="Show segment code.",
                                      keySequence=None
                                      )
        button2.setEnabled(False)
        layout.addWidget(button2)

        button3 = self.setQPushButton(QPushButton(self),
                                      checkable=False,
                                      text="Show Context",
                                      objectName="show_Context",
                                      accessibleName="show_Context",
                                      toolTip="Display only layers of the CONTEXT group",
                                      keySequence=None
                                      )
        layout.addWidget(button3)

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        showCurrent_pushButton = self.findChild(QPushButton, "show_Current")
        showCurrent_pushButton.clicked.connect(self.showCurrentClass)

        showCodes_pushButton = self.findChild(QPushButton, "show_Codes")
        showCodes_pushButton.clicked.connect(self.showCodes)

        showContext_pushButton = self.findChild(QPushButton, "show_Context")
        showContext_pushButton.pressed.connect(self.showContext)
        showContext_pushButton.released.connect(self.showContext)


    def showCurrentClass(self, showCurrentClass:bool=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sender = self.sender()
        self.toggleTextButton(sender,
                              "Show Current",
                              "Show all"
                              )
        showCurrentClass = sender.isChecked()

        mainWindow = self.getMainWindow()
        mainWindow.showCurrentClass(showCurrentClass=showCurrentClass)


    def showCodes(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

        # sender = self.sender()
        # self.toggleTextButton(sender,
        #                       "Show Codes",
        #                       "Hide Codes"
        #                       )
        # showCodes = sender.isChecked()

        # mainWindow = self.getMainWindow()
        # mainWindow.showCodes(showCodes=showCodes)


    def showContext(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sender = self.sender()

        mainWindow = self.getMainWindow()
        qLabel = mainWindow.findChild(QLabel, "labelValue_CurrentVintage")
        if qLabel:
            vintage = qLabel.text()
            keepGroup = f"CONTEXT_{vintage}"
        else:
            keepGroup = "CONTEXT"

        showContext = sender.isDown()
        mainWindow = self.getMainWindow()
        mainWindow.showContext(showContext=showContext, keepGroup=keepGroup)

        associatedWindow = mainWindow.associatedWindow
        associatedWindow.showContext(showContext=showContext, keepGroup=f"CONTEXT_{associatedWindow.getVintage()}")

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setEnabled(True)
        

    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setEnabled(False)


class displayLabelsGroup(groupQPushButton):
    def __init__( self,
                  parent = None,
                  objectName = "displayLabels_Group"
                ):

        super().__init__( parent = parent,
                          objectName = objectName
                        )
        self.setTitle("displayLabels_Group")
        self.displayShortcut = QShortcut(QKeySequence(Qt.Key_I),self)
        self.displayShortcut.setEnabled(False)

    def setupLayout(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)
        
    def setupUi(self):
        layout = self.layout()

        label_2016_class = QLabel(self)
        label_2016_class.setText("Classe 2016 :")
        label_2016_class.setObjectName("label_2016_class")
        label_2016_class.setAccessibleName("label_2016_class")
        label_2016_class.setAutoFillBackground(True)
        label_2016_class.setEnabled(True)

        layout.addWidget(label_2016_class)

        label_2019_class = QLabel(self)
        label_2019_class.setText("Classe 2019 :")
        label_2019_class.setObjectName("label_2019_class")
        label_2019_class.setAccessibleName("label_2019_class")
        label_2019_class.setAutoFillBackground(True)
        label_2019_class.setEnabled(True)

        layout.addWidget(label_2019_class)
    
    def start(self):
        self.setEnabled(True)
        self.displayShortcut.setEnabled(True)
        
    def stop(self):
        self.setEnabled(False)
        self.displayShortcut.setEnabled(False)

    
class attributSelectingToolsGroup(groupQPushButton):
    def __init__( self,
                  parent = None,
                  objectName = "attributSelectingToolsGroup",
                  mutually_exclusif = True
                 ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                         )
        # self.setTitle("Filtering")
        self.setTitle("attributSelectingToolsGroup")
        self.setConnections()

    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()

        button1 = self.setQPushButton(QPushButton(self),
                                      checkable=True,
                                      text="Only Unlabelled",
                                      objectName="only_Unlabelled",
                                      accessibleName="only_Unlabelled",
                                      toolTip="",
                                      keySequence=None
                                      )
        button1.setEnabled(False)
        layout.addWidget(button1)

        button2 = self.setQPushButton(QPushButton(self),
                                      checkable=True,
                                      text="All Entities",
                                      objectName="all_Entities",
                                      accessibleName="all_Entities",
                                      toolTip="",
                                      keySequence=None
                                      )
        button2.setEnabled(False)
        layout.addWidget(button2)

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        only_Unlabelled_pushButton = self.findChild(
            QPushButton, "only_Unlabelled"
        )

        only_Unlabelled_pushButton.clicked.connect(self.onlyUnlabelled)

        all_Entities_pushButton = self.findChild(QPushButton, "all_Entities")
        all_Entities_pushButton.clicked.connect(self.allEntities)

    def onlyUnlabelled(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def allEntities(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.setEnabled(True)


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.setEnabled(False)

class mergeToolsGroup(groupQPushButton):

    def __init__( self,
                  parent = None,
                  objectName = "mergeToolsGroup",
                  mutually_exclusif = False
                ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                         )
        # self.setTitle("Merging")
        self.setTitle("mergeToolsGroup")

        self.setConnections()
        self.mergingLabeledData = None
        self.setSavingLabeledData()

    def setupLayout(self):
        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)


    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()

        button = self.setQPushButton( QPushButton(self),
                                      checkable=False,
                                      text="Fill Pyramid",
                                      objectName="fill_Pyramid",
                                      accessibleName="fill_Pyramid",
                                      toolTip="",
                                      keySequence=None
                                    )
        layout.addWidget(button)

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        fill_Pyramid_pushButton = self.findChild(QPushButton, "fill_Pyramid")
        fill_Pyramid_pushButton.clicked.connect(self.fillPyramid)

    def setSavingLabeledData(self):
        
        masterWindow = self.getMasterWindow()
        self.savingLabeledData = TnTSavingLabeledData(masterWindow)       
        

    def fillPyramid(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        # masterWindow = self.getMasterWindow()
        # mergingLabeledData = TnTmergingLabeledData(masterWindow=masterWindow)
        
        self.savingLabeledData.save()
       
        


class toolsGroup_Base(groupQWidgets):
    def __init__( self,
                  parent = None,
                  objectName = "toolsGroup_Base"
                ):

        super().__init__( parent = parent,
                          objectName = objectName
                        )
        self.setTitle("toolsGroup_Base")


    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout=QVBoxLayout(self)
        self.setLayout(layout)

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(4)


    def getListGroupWhenStartOrStop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return []

    def getListGroupWhenCurrentNomenclatureChanged(self):
        print(f"line:{lineno()},{self.__class__.__name__}->"+
                f"{inspect.currentframe().f_code.co_name}()")

        return []

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #         f"{inspect.currentframe().f_code.co_name}()")

        groupsTypeList=self.getListGroupWhenStartOrStop()
        for groupType in groupsTypeList :
            group = self.findChild(groupType)
            group.start()


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #         f"{inspect.currentframe().f_code.co_name}()")

        groupsTypeList=self.getListGroupWhenStartOrStop()
        for groupType in groupsTypeList :
            group = self.findChild(groupType)
            group.stop()

    def currentNomenclatureChanged(self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                  ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #         f"{inspect.currentframe().f_code.co_name}()")

        groupsTypeList=self.getListGroupWhenCurrentNomenclatureChanged()
        for groupType in groupsTypeList :
            group = self.findChild(groupType)
            group.setEnabled(True)


class toolsGroup_Differential(toolsGroup_Base):
    def __init__( self,
                  parent = None,
                  objectName = "toolsGroup_Differential"
                ):

        super().__init__( parent = parent,
                          objectName = objectName
                        )
        self.setTitle("toolsGroup_Differential")


    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #         f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()
        taskTools_Group = taskToolsGroup( parent=self )
        layout.addWidget( taskTools_Group )

        selectingTools_Group = self.setupSelectingToolsGroup( parent=self )
        layout.addWidget(selectingTools_Group)

        # Spacer : push all  buttons on right side
        vSpacerItem = QSpacerItem( 100,
                                   25,
                                   QSizePolicy.Minimum,
                                   QSizePolicy.Expanding
                                 )
        layout.addItem(vSpacerItem)

        displayLabels_Group = displayLabelsGroup(parent=self)
        layout.addWidget(displayLabels_Group)


    def setupSelectingToolsGroup( self, parent=None ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #         f"{inspect.currentframe().f_code.co_name}()")
        
        selectingTools_Group =selectingToolsGroup( parent=parent )
        return selectingTools_Group

    def getListGroupWhenStartOrStop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return [taskToolsGroup,selectingToolsGroup,displayLabelsGroup]


class toolsGroup_Master(toolsGroup_Differential):
    def __init__( self,
                  parent = None,
                  objectName = "toolsGroup_Master",
                ):

        super().__init__( parent = parent,
                          objectName = objectName
                        )
        self.setTitle("toolsGroup_Master")

    def setupUi(self):

        layout = self.layout()

        startStopTools_Group = startStopToolsGroup( parent=self )
        layout.addWidget( startStopTools_Group )

        mergeTools_Group = mergeToolsGroup( parent=self )
        layout.addWidget( mergeTools_Group )

        taskTools_Group = taskToolsGroup ( parent=self )
        layout.addWidget( taskTools_Group )

        selectingTools_Group = self.setupSelectingToolsGroup( parent=self )
        layout.addWidget(selectingTools_Group)

        attributSelecting_Group = attributSelectingToolsGroup( parent=self )
        layout.addWidget(attributSelecting_Group)

        displayTools_Group = displayToolsGroup( parent=self )
        layout.addWidget(displayTools_Group)

        displayLabels_Group = displayLabelsGroup(parent=self)
        layout.addWidget(displayLabels_Group)

        # Spacer : push all  buttons on right side
        vSpacerItem = QSpacerItem( 100,
                                   25,
                                   QSizePolicy.Minimum,
                                   QSizePolicy.Expanding
                                 )
        layout.addItem(vSpacerItem)


    def getListGroupWhenStartOrStop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return [ taskToolsGroup,
                 selectingToolsGroup,
                 attributSelectingToolsGroup,
                 displayToolsGroup,
                 displayLabelsGroup
               ]

    def getListGroupWhenCurrentNomenclatureChanged(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return [startStopToolsGroup]


class viewsManagerGroup(groupQPushButton):

    def __init__( self,
                  parent = None,
                  objectName = "viewsManagerGroup",
                  mutually_exclusif = False
                 ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                        )
        self.setTitle("viewsManagerGroup")
        self.setConnections()

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()


        # Spacer : push all  buttons on right side
        hSpacerItem = QSpacerItem( 100,
                                   25,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Minimum
                                 )
        layout.addItem(hSpacerItem)

        button1 = self.setQPushButton( QPushButton(self),
                                      checkable=False,
                                      text="Fit All",
                                      objectName="fit_All",
                                      accessibleName="fit_All",
                                      toolTip="",
                                      keySequence=None
                                     )
        layout.addWidget(button1)

        button2 = self.setQPushButton( QPushButton(self),
                                      checkable=True,
                                      checked=True,
                                      enabled=True,
                                      text="Synchro Views",
                                      objectName="synchro_Views",
                                      accessibleName="synchro_Views",
                                      toolTip="",
                                      keySequence=None
                                    )
        layout.addWidget(button2)

        button3 = self.setQPushButton( QPushButton(self),
				              checkable=True,
                              checked=False,
                              enabled=False,
				              text="Synchro Levels",
				              objectName="synchro_Levels",
				              accessibleName="synchro_Levels",
				              toolTip="",
				              keySequence=None
				              )
        layout.addWidget(button3)

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        fit_All_pushButton = self.findChild(QPushButton, "fit_All")
        fit_All_pushButton.clicked.connect(self.fitAll)

        synchro_Views_pushButton = self.findChild(QPushButton, "synchro_Views")
        synchro_Views_pushButton.clicked.connect(self.synchroViews)

        synchro_Levels_pushButton = self.findChild(QPushButton, "synchro_Levels")
        synchro_Levels_pushButton.clicked.connect(self.synchroLevels)

    def fitAll(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        mainWindow = self.getMainWindow()
        map_canvas = mainWindow.findChild(mapCanvas, "mapCanvas")
        map_canvas.zoomAllToFullExtent()

    def updateChecked_AllButtons(self, sender):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        masterWindow = self.getMasterWindow()
        name = sender.objectName()
        button_list = masterWindow.findChildren(QPushButton, name)
        
        state = sender.isChecked()
        button_list.remove(sender)
        for button in button_list:
            button.setChecked(state)

    def synchroViews(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sender = self.sender()
        state = sender.isChecked()
        
        self.updateChecked_AllButtons(sender)
        self.setSynchroMode_Canvas(state)

    def setSynchroMode_Canvas(self, state=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        masterWindow = self.getMasterWindow()
        canvas_list = masterWindow.findChildren(mapCanvas, "mapCanvas")
        for canvas in canvas_list :
            if canvas.isVisible() :
                canvas.manageSynchroConnections(state)

    def synchroLevels(self):
        sender = self.sender()
        state = sender.isChecked()
        
        self.updateChecked_AllButtons(sender)
        self.setSynchroLevels_Slider(state)
        
    def setSynchroLevels_Slider(self, state=False):
        masterWindow = self.getMasterWindow()
        slider_list = masterWindow.findChildren(sliderGroup, "sliderGroup")
        for slider in slider_list:
            slider.manageSynchroLevels(state)

class viewsManagerGroup_Master(viewsManagerGroup):

    def __init__( self,
                  parent = None,
                  objectName = "viewsManagerGroup_Master",
                  mutually_exclusif = False
                ):
        super().__init__( parent = parent,
                          objectName = objectName,
                          mutually_exclusif = mutually_exclusif
                         )
        self.setTitle("viewsManagerGroup_Master")
        self.setConnections()

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().setupUi()
        layout = self.layout()

        label = QLabel(self)
        label.setText("Standard labeling mode")
        label.setObjectName("labeling_Mode")
        label.setAccessibleName("labeling_Mode")
        layout.addWidget(label)

        layout.insertWidget(0, label)

        button2 = self.setQPushButton( QPushButton(self),
                                       checkable=True,
                                       text="Add View",
                                       objectName="add_View",
                                       accessibleName="add_View",
                                       toolTip="",
                                       keySequence=None
                                     )
        layout.addWidget(button2)

        synchroViews_Button = self.findChild(QPushButton, "synchro_Views")
        synchroViews_Button.setEnabled(False)

        synchroLevels_Button = self.findChild(QPushButton, "synchro_Levels")
        synchroLevels_Button.setEnabled(False)

    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        labelingMode_Button = self.findChild(QLabel, "labeling_Mode")
        labelingMode_Button.setText("Standard labeling mode")
        self.changeVisiblePushButton("add_View")
        
        synchroViews_Button = self.findChild(QPushButton, "synchro_Views")
        synchroViews_Button.setEnabled(True)

        synchroLevels_Button = self.findChild(QPushButton, "synchro_Levels")
        synchroLevels_Button.setEnabled(True)


    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        labelingMode_Button = self.findChild(QLabel, "labeling_Mode")
        labelingMode_Button.setText("Differential labeling mode.")
        self.changeVisiblePushButton("add_View")
        
        synchroViews_Button = self.findChild(QPushButton, "synchro_Views")
        synchroViews_Button.setEnabled(True)

        synchroLevels_Button = self.findChild(QPushButton, "synchro_Levels")
        synchroLevels_Button.setEnabled(False)

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        super().setConnections()
        addView_Button = self.findChild( QPushButton, "add_View" )
        addView_Button.clicked.connect( self.addView )
        addView_Button.clicked.connect( self.setEnabledButton_SynchroViews )
        addView_Button.clicked.connect( self.setEnabledButton_SynchroLevels )

    def setEnabledButton_SynchroViews(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        synchro_Views_pushButton = self.findChild(QPushButton, "synchro_Views")
        sender=self.sender()
        synchro_Views_pushButton.setEnabled(sender.isChecked())
        
    def setEnabledButton_SynchroLevels(self):
        synchroLevels_pushButton = self.findChild(QPushButton, "synchro_Levels")
        sender=self.sender()
        synchroLevels_pushButton.setEnabled(sender.isChecked())
        

    def addView(self):
        """ show/hide view in standard mode only"""
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        sender = self.sender()
        masterWindow = self.getMasterWindow()
        if sender.isChecked()  :
            masterWindow.associatedWindow.show()
        else :
            masterWindow.associatedWindow.hide()

        self.toggleTextButton( sender,
                               "Add View",
                               "Hide View"
                             )

class infoSelectionGroup(groupQWidgets):
    def __init__( self,
                  parent = None,
                  objectName = "infoSelectionGroup",
                ):
        super().__init__( parent=parent,
                          objectName=objectName
                        )
        self.setTitle("infoSelectionGroup")

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout = self.layout()
        self.layout().setSpacing(1)

        self.setPairLabelValues("NOMENCLATURE", ["CurrentNomenclature"])

        spacerItem = QSpacerItem( 40,
                                  20,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Minimum
                                )
        layout.addItem(spacerItem)

        self.setPairLabelValues("VINTAGE", ["CurrentVintage"], visible=False)

        spacerItem = QSpacerItem( 40,
                                  20,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Minimum
                                  )
        layout.addItem(spacerItem)

        self.setPairLabelValues( "SELECTION",
                                 ["CurrentColor",
                                  "CurrentCode",
                                  "CurrentClass"]
                               )

    def setPairLabelValues( self,
                            textLabel="no text",
                            labelValueIDs=["no_id"],
                            visible=True):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layout = self.layout()

        label = QLabel(self)
        label.setText(f"{textLabel}")
        longName = self.getLongName( "label",
                                     textLabel.lower().replace(' ','')
                                   )
        label.setObjectName(longName)
        label.setAccessibleName(longName)
        label.setVisible(visible)
        layout.addWidget(label)

        labelSeparator = QLabel(self)
        labelSeparator.setText(":")
        longName = self.getLongName( "labelSeparator",
                                     textLabel.lower().replace(' ','')
                                   )
        labelSeparator.setObjectName(longName)
        labelSeparator.setAccessibleName(longName)
        labelSeparator.setVisible(visible)
        layout.addWidget(labelSeparator)

        for labelValueID in labelValueIDs :
            label_value = QLabel(self)
            label_value.setText("No value")
            name = f"labelValue_{labelValueID}"
            label_value.setObjectName(name)
            label_value.setAccessibleName(name)
            label_value.setVisible(visible)
            layout.addWidget(label_value)

    def setNomenclatureValue(self, value:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        label = self.findChild(QLabel, "labelValue_CurrentNomenclature")
        label.setText(value)


    def setColorValue(self, value:QColor):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        label = self.findChild(QLabel, "labelValue_CurrentColor")
        label.setText("text")
        palette = QPalette()
        palette.setColor(QPalette.Window, value)
        palette.setColor(QPalette.WindowText, value)
        label.setAutoFillBackground(True)
        label.setPalette(palette)


    def setCodeValue(self, value:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        label = self.findChild(QLabel, "labelValue_CurrentCode")
        label.setText(value)


    def setClassValue(self, value:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        label = self.findChild(QLabel, "labelValue_CurrentClass")
        label.setText(value)


    def setVisibilityVintage(self, visibility=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        label_vintage= self.findChild( QLabel, "label_vintage")
        label_vintage.setVisible(visibility)

        separator_vintage = self.findChild( QLabel, "labelSeparator_vintage" )
        separator_vintage.setVisible(visibility)

        value_vintage = self.findChild( QLabel, "labelValue_CurrentVintage")
        value_vintage.setVisible(visibility)

    def setVintage(self, vintage:str=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        value_vintage = self.findChild( QLabel, "labelValue_CurrentVintage" )
        value_vintage.setText(vintage)
        
    def getVintage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        value_vintage = self.findChild( QLabel, "labelValue_CurrentVintage" )
        return value_vintage.text()
    
    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        #Hide Qlabel contain vintage value
        self.setVisibilityVintage()
        self.setValueVintage()

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setVisibilityVintage(visibility=True)
        self.setVintage(vintage=self.getMainWindow().getVintage())

    def currentNomenclatureChanged( self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                  ):

        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setNomenclatureValue(nomenclatureName)


    def itemSelectionChanged(self, itemSelected:QTreeWidgetItem=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        colorValue = itemSelected.background(0).color()
        codeValue = itemSelected.text(1)
        classValue =itemSelected.text(2)

        self.setColorValue(colorValue)
        self.setCodeValue(codeValue)
        self.setClassValue(classValue)


class sliderGroup(groupQWidgets):
    def __init__( self,
                  parent = None,
                  objectName = "sliderGroup",
                ):
        super().__init__( parent=parent,
                          objectName=objectName,
                        )
        self.setTitle("sliderGroup")

        self.synchroMode = False
        self.setConnections()
        self.setShortCuts()

        self.listLabeledLayers = []

        # Still locked to construction.
        # Unlocking by action on the start button
        self.setEnabled(False)


    def setupUi(self):

        layout = self.layout()

        sizePolicy = QSizePolicy( QSizePolicy.Maximum,
                                  QSizePolicy.Minimum
                                )
        labelSlider = QLabel( self )
        longName = self.getLongName( "labelSlider", self.objectName() )
        labelSlider.setObjectName( longName )
        labelSlider.setAccessibleName( longName )
        labelSlider.setText( "No level" )
        labelSlider.setSizePolicy( sizePolicy )
        layout.addWidget( labelSlider )

        sizePolicy.setHorizontalPolicy(
                                        QSizePolicy.Expanding

                                      )
        slider = QSlider( Qt.Horizontal, self )
        longName = self.getLongName( "slider", self.objectName() )
        slider.setObjectName( longName )
        slider.setAccessibleName( longName )
        slider.setMinimum( 1 )
        slider.setMaximum( 10 )
        slider.setPageStep( 1 )
        slider.setTickPosition( QSlider.TicksAbove )
        slider.setSizePolicy( sizePolicy )
        layout.addWidget( slider )

    def nextLevel(self):
        """
        This method is executed each time the TAB key is pressed.
        Increments the current value of the slider with the value of the next segment level.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->\
        #       {inspect.currentframe().f_code.co_name}()")

        slider = self.findChild(QSlider, "slider_sliderGroup")
        if slider.isEnabled() :
            if slider.value()== slider.maximum():
                slider.setValue(slider.minimum())
            else:
                slider.setValue(slider.value()+1)

    def previousLevel(self):
        """
        This method is executed each time the SHIFT+TAB keys is pressed.
        Decrement the value of the slider with the value of the previous segment level.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->\
        #       {inspect.currentframe().f_code.co_name}()")

        slider = self.findChild(QSlider, "slider_sliderGroup")
        if slider.isEnabled():
            if slider.value()==slider.minimum():
                slider.setValue(slider.maximum())
            else:
                slider.setValue(slider.value()-1)

    def setSliderShortcut(self):
        """
        Instantiation of the shortcuts assigned to the slider.
        TAB, key pressed = next level of segmentation
        CTRL+TAB, key pressed = prev level of segmentation.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->\
        #       {inspect.currentframe().f_code.co_name}()")

        Shortcut_NextLevel=QShortcut(QKeySequence("Tab"),self)
        Shortcut_NextLevel.activated.connect(self.nextLevel)
        Shortcut_PreviousLevel=QShortcut(QKeySequence("Shift+Tab"),self)
        Shortcut_PreviousLevel.activated.connect(self.previousLevel)

    # def setMimimum(self, mimimum:int=1):
    #     slider = self.findChild(QSlider, "slider_sliderGroup")
    #     slider.setMimimum(mimimum)

    # def setMaximun(self, maximum:int=10):
    #     slider = self.findChild(QSlider, "slider_sliderGroup")
    #     slider.setMaximum(maximum)

    def setMaximum(self):
        slider = self.findChild(QSlider, "slider_sliderGroup")
        slider.setValue(slider.maximum())

    # def value(self):
    #     slider = self.findChild(QSlider, "slider_sliderGroup")
    #     slider.value()

    # def setValue(self, value:int):
    #     slider = self.findChild(QSlider, "slider_sliderGroup")
    #     slider.setValue(value)

    def updateTextLabelSlider(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        slider = self.sender()
        value = int(slider.value())

        labelSlider = self.findChild(QLabel, "labelSlider_sliderGroup")
        labelSlider.setText(f"level{value}")


    def resetSlider(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.listLabeledLayers=[]

        slider = self.findChild(QSlider)
        slider.setMinimum( 1 )
        slider.setMaximum( 6 )
        slider.setPageStep( 1 )
        slider.setValue( 1 )
        slider.setEnabled(False)

        labelSlider = self.findChild(QLabel, "labelSlider_sliderGroup")
        labelSlider.setText("No level")

    def initSlider(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setListLabeledLayers()
        layers_list = self.getListLabeledLayers()

        slider = self.findChild(QSlider, "slider_sliderGroup")
        slider.setEnabled(True)

        maximum = len(layers_list)
        slider.setMaximum( maximum )

        slider.setValue(1)
        layers_list[0].setItemVisibilityChecked(True)
        layers_list[-1].setItemVisibilityChecked(True)

        mainWindow = self.getMainWindow()
        layerTreeWidget = mainWindow.findChild(TnTLayerTreeWidget)
        layerTreeWidget.view.setCurrentLayer(layers_list[0].layer())

        # # And set MapLayer to canvas  (ie is an active mapLayer)
        map_Canvas = mainWindow.findChild(mapCanvas)
        map_Canvas.setCurrentLayer(layers_list[0].layer())

        labelSlider = self.findChild(QLabel, "labelSlider_sliderGroup")
        labelSlider.setText(f"level{slider.value()}")

    def activateSegmentLevel(self, newIndex):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layers_list = self.getListLabeledLayers()

        if layers_list:
            
            # Initialize all visibility to false, except last layer
            for i in range(len(layers_list)-1):
                layer = layers_list[i]
                layer.setItemVisibilityChecked(False)

            layers_list[newIndex].setItemVisibilityChecked(True)
            
            
            # Display or hide yellow outline for the most segmented layer
            mainWindow = self.getMainWindow()
            layerTreeWidget = mainWindow.findChild(TnTLayerTreeWidget)
            lastLayer = layers_list[-1]
            nomenclatureWidget = layerTreeWidget.getTnTnomenclatureWidget()
            associationTable = nomenclatureWidget.getAssociationTable()
            vintage = layerTreeWidget.getVintage()
            fieldName=f"code_{vintage}"
            if newIndex == len(layers_list)-1:
                # Display yellow outline
                renderer = layerTreeWidget.createFillSymbolLastLayer(
                    associationTable=associationTable,
                    fieldName=fieldName,
                    yellowOutline=True
                )
            
            else:
                # Hide yellow outline
                renderer = layerTreeWidget.createFillSymbolLastLayer(
                    associationTable=associationTable,
                    fieldName=fieldName,
                    yellowOutline=False
                )
            lastLayer.layer().setRenderer(renderer)

            # And set MapLayer to canvas  (ie is an active mapLayer)
            mainWindow = self.getMainWindow()
            layerTreeWidget = mainWindow.findChild(TnTLayerTreeWidget)
            layerTreeWidget.view.setCurrentLayer(layers_list[newIndex].layer())

            # # And set MapLayer to canvas  (ie is an active mapLayer)
            map_Canvas = mainWindow.findChild(mapCanvas)
            map_Canvas.setCurrentLayer(layers_list[newIndex].layer())


    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        slider = self.findChild(QSlider, "slider_sliderGroup")
        slider.valueChanged.connect(self.updateTextLabelSlider)
        slider.valueChanged.connect(
                    lambda:(self.activateSegmentLevel(int(slider.value()-1)))
                                   )
        slider.valueChanged.connect(self.setSynchroLevels)

    def manageSynchroLevels(self, state):

        self.synchroMode = state
        self.setSynchroLevels()

    def setSynchroLevels(self):
        if self.synchroMode == True:  
            mainWindow = self.getMainWindow()
            main_slider = mainWindow.findChild(QSlider, "slider_sliderGroup")
            value = main_slider.value()

            if mainWindow == self.getMasterWindow():
                associatedWindow = mainWindow.associatedWindow
            else:
                associatedWindow = self.getMasterWindow()
                  
            associatedSlider = associatedWindow.findChild(QSlider, "slider_sliderGroup")
            associatedSlider.setValue(value)
            associatedLaberSlider = associatedWindow.findChild(QLabel, "labelSlider_sliderGroup")
            associatedLaberSlider.setText(f"level{value}")

        else:
            pass

    def getListLabeledLayers(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.listLabeledLayers

    def setListLabeledLayers(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTree_Widget = self.getMainWindow().findChild(TnTLayerTreeWidget)
        root = layerTree_Widget.root

        groups = [child for child in root.children()
                 if child.name().startswith("LABELED_DATA")]

        group = groups[0]

        if not group.itemVisibilityChecked():
            group.setItemVisibilityChecked(True)
        if not group.isExpanded() :
           group.setExpanded(True)

        self.listLabeledLayers = group.findLayers()


    def setShortCuts(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setSliderShortcut()

    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def start(self):
        """
        Unlocks at the action of the START button
        Loads the list of layers from the LABELLED_DATA group,
        and initializes the slider which drives the display of
        these segmented layers.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setEnabled(True)
        self.initSlider()

    def stop(self):
        """
        locks at the action of the STOP button
        Clear the list of layers from the LABELLED_DATA group.
        and reset the slider that controlled the display of
        these segmented layers.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.resetSlider()
        self.setEnabled(False)

class menu_widget(QMenu):
    def __init__( self,
                  title = "no_title",
                  menuBar:QMenuBar = None,
                  objectName = "menuGroup"
                ):
        super().__init__(title, menuBar)

        super().setObjectName(objectName)
        super().setAccessibleName(objectName)


    def createAction( self,
                      text = "no_text",
                      objectName = "action",
                      shortcut = None,
                      statusTip = None
                    ):
        menuBar=self.parent()
        mainWindow = menuBar.parent()
        action = QAction(text, mainWindow)
        action.setObjectName(objectName)
        if shortcut:
            action.setShortcut(shortcut)
        if statusTip:
            action.setStatusTip(statusTip)

        self.addAction(action)
        menuBar.addAction(self.menuAction())
        return action

##################################################################################################

class TnTnomenclatureWidget( groupQWidgets ):
    def __init__( self,
                  parent = None,
                  objectName = "TnTnomenclatureWidget"
                ):

        super().__init__( parent = parent,
                          objectName = objectName,
                        )

        self.defaultHeader = []
        self.setDefaultHeader()
        
        self.vintage = None

        self.attributsTable = []
        self.setAttributsTable()

        self.selectedValuesAsDict = {}
        self.associationTable = {}

        self.setConnections()

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        treeWidget = self.getTreeWidget()
        treeWidget.itemSelectionChanged.connect( self.itemSelectionChanged )
        treeWidget.currentItemChanged.connect( self.currentItemChanged )

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()
        treeWidget = self.initTreeWidget()
        layout.addWidget(treeWidget)

    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout=QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def initTreeWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        treeWidget = QTreeWidget(self)
        longName = self.getLongName( "treeWidget",
                                     self.objectName()
                                   )
        treeWidget.setObjectName( longName )
        treeWidget.setAccessibleName( longName )
        #self.setHeaderTreeWidget(treeWidget)

        return treeWidget

    def getTreeWidget(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        longName = self.getLongName( "treeWidget", self.objectName() )
        widget = self.findChild( QTreeWidget, longName )
        return widget

#################################################"
# Attribute table and treeWidget header

    def getDefaultHeader(self) :
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.defaultHeader

    def setDefaultHeader(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.defaultHeader = ["color", "code" ,"class"]

    def getHeader(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.getDefaultHeader()

    def setHeader(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setDefaultHeader()

    def getAttributsTable(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.attributsTable

    def setAttributsTable(self, vintage="No value"):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.attributsTable = []
        for headerValue in self.getHeader():
            val=(lambda:f"{headerValue}",
                  lambda:f"{headerValue}_{vintage}")[vintage!="No value"]()
            self.attributsTable.append(val)

        # print(f"self.attributsTable={self.attributsTable}")


    def setVintage(self, vintage:str=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.vintage = vintage

    def getVintage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.vintage

    def setHeaderItem(self, treeWidget):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        labels = self.getHeader()
        treeWidget.setColumnCount(len(labels))
        treeWidget.setHeaderLabels(labels)
        treeWidget.header().setDefaultAlignment(Qt.AlignCenter)
        for i in range(len(labels)):
            treeWidget.setColumnWidth(i,75)

    def getHeaderItem(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        treeWidget = self.getTreeWidget()
        return treeWidget.headerItem()

    def getSelectedValuesAsDict(self):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        keys = self.getAttributsTable()
        values = self.getSelectedValues()
        i=0
        for key in keys :
            self.selectedValuesAsDict[key]=values[i]
            i+=1
        return self.selectedValuesAsDict
    
    def getAssociationTable(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.associationTable

    def getSelectedValues(self):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        item = self.getSelectedItems()
        colorValue = item.background(0).color().value()
        codeValue = item.text(1)
        classValue =item.text(2)
        values = [ colorValue,
                    codeValue,
                    classValue
                  ]
        return values

    def getSelectedItems(self):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        items = self.getTreeWidget().selectedItems()
        try :
            return items[0]
        except IndexError:
            return None

    def resizeAllColumnsToContents(self, treeWidget:QTreeWidget=None):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nb_columns =  treeWidget.columnCount()
        for i in range(nb_columns) :
            treeWidget.resizeColumnToContents(i)
            
            
    def rgb2hex(self, rgb=None):
        """
        Converting rgb color value into hexa color value.
            param rgb: rgb value to convert.
            return hex: hex value.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if rgb is None:
            rgb = [0, 0, 0]
        return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])


    def hex2rgb(self, hx):
        """
        Converting hexa color value into rgb color value.
            param hx: hexa value to convert.
            return rgb: rgb value
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return [ int(hx[0:2],16), int(hx[2:4],16) , int(hx[4:6],16)]
    

    def copyTreeWidgetSrcToDst( self,
                          treeWidgetSrc:QTreeWidget=None,
                          treeWidgetDst:QTreeWidget=None
                         ):
        """Copy each QTreeWidgetItems of treeWidgetSrc
        into treeWidgetDst"""
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.associationTable.clear()
        
        listItems = treeWidgetSrc.findItems("*",
                                            Qt.MatchWrap | Qt.MatchWildcard
                                           )
        
        if listItems:
            treeWidget = treeWidgetDst
            treeWidget.clear()

            header_Item = treeWidgetSrc.headerItem().clone()
            treeWidget.setHeaderItem(header_Item)
            for item in listItems:

                treeWidget.addTopLevelItem(item.clone())

                self.associationTable[item.text(1)] =\
                    item.background(0).color().name(QColor.HexRgb)

            self.resizeAllColumnsToContents(treeWidget)

            topLevelItem = treeWidget.topLevelItem(0)
            topLevelItem.setSelected(True)

            treeWidget.currentItemChanged.emit(topLevelItem, None)

            listItems.clear()

    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setAttributsTable()

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.setVintage(vintage=self.getMainWindow().getVintage())
        self.setAttributsTable(vintage=self.getVintage())
        


    def itemSelectionChanged(self):
        """TODO: la liste des selectedItems()" peut etre temporairement
                  vide au changement de nomenclature via le combobox.
                  deconnecter le signal  itemSelectionChanged avant de
                  changer de nomenclature puis le reconnecter apres chgt.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        item = self.getSelectedItems()
        if item :
            dockWidgetParent = self.getDockWidgetParent()
            dockWidgetParent.itemSelectionChanged(item)


    def lockGroupByType(self, groupsTypeList=None) :
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.parent().lockGroupByType(
            groupsTypeList=groupsTypeList
        )

    def unlockGroupByType(self, groupsTypeList=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.parent().unlockGroupByType(
            groupsTypeList=groupsTypeList
        )

    def currentNomenclatureChanged( self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                   ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.copyTreeWidgetSrcToDst(
            treeWidgetSrc=treeWidgetSrc,
            treeWidgetDst=self.getTreeWidget()
        )



    def currentItemChanged( self,
                            current:QTreeWidgetItem,
                            previous:QTreeWidgetItem
                          ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        if not previous :
            dockWidgetParent = self.getDockWidgetParent()
            groupsTypeList = [infoSelectionGroup]
            dockWidgetParent.unlockGroupByType(groupsTypeList=groupsTypeList)


class TnTnomenclatureWidget_Master(TnTnomenclatureWidget):
    """
    Class managing nomenclature file.
    """
    def __init__( self,
                  parent = None,
                  objectName = "TnTnomenclatureWidget_Master"
                ):

        super().__init__( parent = parent,
                          objectName = objectName
                        )
        self.nomenclaturesDict = {}
        # self.associationTable = {}

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().setConnections()
        comboBox = self.getComboBox()
        comboBox.currentTextChanged.connect(self.currentTextChanged)

        # comboBox.activated.connect( self.comboBox_activated )
        # comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)
        # comboBox.editTextChanged.connect(self.comboBox_editTextChanged)
        # comboBox.highlighted.connect(self.comboBox_highlighted)
        # comboBox.textActivated.connect(self.comboBox_textActivated)
        # comboBox.textHighlighted.connect(self.comboBox_textHighlighted)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().setupUi()
        layout = self.layout()
        comboBox = self.initComboBox()
        layout.insertWidget(0, comboBox)

    def initComboBox(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        comboBox = QComboBox(self)
        sizePolicy = QSizePolicy( QSizePolicy.Maximum,
                                  QSizePolicy.Maximum
                                )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        comboBox.setSizePolicy(sizePolicy)

        longName = self.getLongName( "comboBox",
                                     self.objectName()
                                   )
        comboBox.setObjectName( longName )
        comboBox.setAccessibleName( longName )
        inviteMessage = self.getInviteMessage()
        comboBox.addItem( inviteMessage, QVariant.String )
        comboBox.setEnabled(False)
        return comboBox

    def clearInviteMessage(self, comboBox:QComboBox = None):
        """ Clear combox if contains only """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        i_msg = self.getInviteMessage()
        index = comboBox.findText(i_msg)
        if index !=-1:
            comboBox.removeItem(index)

    # def getAssociationTable(self):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")

    #     return self.associationTable

    def getInviteMessage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return "Please select NOMENCLATURE from the menu."


    def getComboBox(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        widget = self.findChild(QComboBox)
        return widget


    def setNomenclaturesDict(self, nomenclatureFiles):
        """ Transforms the list passed as an argument into a dictionary.
            The search keys are the name without extension of the nomenclature
            files.
            Each key is passed to the ComboBox, to allow the user to select a
            nomenclature among those that user have been loaded """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.nomenclaturesDict.clear()
        for nomenclatureFile in nomenclatureFiles:
            key = (os.path.basename (nomenclatureFile ).split('.'))[0]
            value = nomenclatureFile
            self.nomenclaturesDict[key]=value

        comboBox = self.getComboBox()
        comboBox.setEnabled(True)
        comboBox.clear()

        keys = self.nomenclaturesDict.keys()
        for key in keys :
            comboBox.addItem(key)

    def detectDelimiter(self, header):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if header.find("|")!=-1:
            return "|"
        if header.find(",")!=-1:
            return ","
        if header.find("\t")!=-1:
            return ","
        return ";"

    def convertColor(self, colorValue):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        color_HEX="#000000"
        color_RGB=[0,0,0]

        if colorValue.startswith('#'):
            color_HEX = colorValue
            result = colorValue.split('#')[1]
            color_RGB=self.hex2rgb(result)

        elif colorValue.startswith('(') and colorValue.endswith(')'):
            res=(((colorValue.split('(')[1]).split(')'))[0]).split(',')
            color_RGB=[int(res[0]),int(res[1]),int(res[2])]
            color_HEX=self.rgb2hex(color_RGB)

        color=QColor()
        color.setRgb( color_RGB[0], color_RGB[1], color_RGB[2] )

        return color, color_HEX


    def dumpCSVFile(self, nomenclatureFile):
        """
        Load nomenclature CVS file.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        treeWidget = self.getTreeWidget()
        self.associationTable.clear()

        try :
            with open( nomenclatureFile,
                        mode = 'r',
                        encoding='utf-8') as csvFile:

                sample = csvFile.read(1024)
                dialect = csv.Sniffer().sniff(sample)
                if csv.Sniffer().has_header(sample):
                    tmp=(str(sample)).split('\n',1)
                    delimiter=self.detectDelimiter(tmp[0])
                    fieldnames = tmp[0].split(delimiter)

                    index_c = fieldnames.index('color')
                    color_v = fieldnames.pop(index_c)
                    fieldnames.insert(0, color_v)
                csvFile.seek(0)

                treeWidget.setHeaderLabels(fieldnames)

                csvReader = csv.DictReader(csvFile, dialect=dialect)
                for row in csvReader:

                    colorValue = row[fieldnames[0]]
                    color,color_HEX = self.convertColor(colorValue)

                    brush = QBrush()
                    brush.setStyle(Qt.SolidPattern)
                    brush.setColor(color)

                    item = QTreeWidgetItem()
                    item.setTextAlignment(0, Qt.AlignCenter)

                    # text is alway "color",
                    # color is embedded in back and foreground
                    item.setText(0, fieldnames[0])
                    item.setBackground(0, brush)
                    item.setForeground(0, brush)

                    item.setText(1, row[fieldnames[1]])
                    item.setText(2, row[fieldnames[2]])

                    treeWidget.addTopLevelItem(item)

                    self.associationTable[row[fieldnames[1]]]=color_HEX

                for i in range(treeWidget.columnCount()) :
                    treeWidget.resizeColumnToContents(i)

        except FileNotFoundError :
            QTreeWidgetItem(treeWidget, ["0","No LABEL","#000000"])


    def currentTextChanged(self, text:str):
        """
            this method is called when the user chooses another nomenclature
            in the combox.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        # Text maybe empty after clear() reset...
        if text:
            file = self.nomenclaturesDict[text]
            treeWidget = self.getTreeWidget()
            treeWidget.clear()
            self.dumpCSVFile(file)

            self.currentNomenclatureChanged(
                nomenclatureName=text,
                treeWidgetSrc=self.getTreeWidget()
            )
            treeWidget.topLevelItem(0).setSelected(True)
        else:
            pass

    def currentNomenclatureChanged( self,
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                  ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        mainWindow = self.getMainWindow()
        mainWindow.currentNomenclatureChanged (
                                           nomenclatureName = nomenclatureName,
                                           treeWidgetSrc = treeWidgetSrc
                                              )


        # groupsTypeList = [infoSelectionGroup, startStopToolsGroup]
        # dockWidgetParent.unlockGroupByType(groupsTypeList=groupsTypeList)

        # dockWidgetParent = self.getDockWidgetParent()
        # dockWidgetParent.currentNomenclatureChanged(
        #                                 nomenclatureName = nomenclatureName
        #                                            )

        # treeWidgetSrc = self.getTreeWidget()
        # self.updateTnTnomenclatureWidgetAssociated(
        #                                      treeWidgetSrc = treeWidgetSrc
        #                                           )


    # def showEvent(self, event:QShowEvent):
    #     """    """
    #     print(f"line:{lineno()},{self.__class__.__name__}->"+
    #           f"{inspect.currentframe().f_code.co_name}()")

    #     pass

    # def changeEvent(self, event:QEvent):
    #     print(f"line:{lineno()},{self.__class__.__name__}->"+
    #           f"{inspect.currentframe().f_code.co_name}()")

    #     pass

    # def event(self, event:QEvent):
    #     print(f"line:{lineno()},{self.__class__.__name__}->"+
    #           f"{inspect.currentframe().f_code.co_name}()")

    #     pass

    # def comboBox_activated(self, index:int):
    #     print(f"line:{lineno()},{self.__class__.__name__}->"+
    #           f"{inspect.currentframe().f_code.co_name}()")
    #     print(f"self.associationTable={self.associationTable}")
    #     pass

    # def comboBox_currentIndexChanged(self, index:int):
    #     print(f"comboBox_currentIndexChanged({index})")
    #     pass

    # def comboBox_editTextChanged(self, text:str):
    #     print(f"comboBox_editTextChanged({text})")
    #     pass

    # def comboBox_highlighted(self, index:int):
    #     print(f"comboBox_highlighted({index})")
    #     pass

    # def comboBox_textActivated(self, text:str):
    #     print(f"comboBox_textActivated({text})")
    #     pass

    # def comboBox_textHighlighted(self, text:str):
    #     print(f"comboBox_textHighlighted({text})")
    #     pass

##################################################################################################

class TnTLayerTreeWidget(groupQWidgets):
    """
    Table of contents management class.
    """
    def __init__( self,
                  parent = None,
                  objectName = "TnTLayerTreeWidget"
                ):

        super().__init__( parent = parent,
                          objectName = objectName
                        )
        self.setTitle(self.objectName())

        self.root = None
        self.model = None
        self.view = None
        self.groupsVisibilityState = {}

        #Instanciate root/model/view and and view in layout
        self.setUpLayerTreeView()
        self.addViewInLayout()
        
        self.vintage = None

        self.styleSheet_segmentedData = { "color":"",
                                          "outline_color":"#eeff01",
                                          "line_color":"#eeff01",
                                          "width_border":"0.25",
                                          "style":"solid line"
                                          }

        self.styleSheet_unlabeled = { "color":"",
                                      "outline_color":"yellow",
                                      "width_border":"0.20",
                                      "style":"no"
                                      }

        self.styleSheet_transparent = { "color":"",
                                      "style":"no",
                                      "outline_style":"no"
                                      }

        self.styleSheet_labeled = { "color":"",
                                    "style":"solid",
                                    "outline_style":"no"
                                    }

        self.styleSheet_Default = { "color":"" ,
                                    "outline_color":"black",
                                    "width_border":"0.05",
                                    "style":"no"
                                    }

        self.styleSheet_NoLabel = { "color":"transparent",
                                    "outline_color":"black",
                                    "width_border":"0,70",
                                    "style":"solid line"
                                  }


        # self.dictCodeRuleKey={}
        self.setConnections()

    def setConnections(self):
        pass

    def setupUi(self):
        pass

    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout=QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().setContentsMargins(4, 2, 4, 2)
        self.layout().setSpacing(4)

    def setDefaultSizePolicy(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def addViewInLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layout = self.layout()
        layout.addWidget(self.view)

    def layerTreeRoot(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        return self.root

    def setLayerTreeRoot(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.root = QgsProject.instance().layerTreeRoot().clone()

    def  setUpLayerTreeView(self):
        """
        Create a new QgsLayerTreeView based on  new QgsLayerTreeModel with
        given layer tree root node.
        The root node is the root node of the current project, and set flags
        of new QgsLayerTreeModel properly:

        the flags used are:

        UseEmbeddedWidgets: Layer nodes may optionally include extra embedded
            widgets (if used in QgsLayerTreeView)
        UseTextFormatting: Layer nodes will alter text appearance based on
            layer properties, such as scale based visibility.
        AllowNodeChangeVisibility: Allow user to set node visibility with
            a checkbox.
        ActionHierarchical: Check/uncheck action has consequences on
            children (or parents for leaf node)
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #   f"{inspect.currentframe().f_code.co_name}()")

        self.setLayerTreeRoot()

        self.view = QgsLayerTreeView(self)
        longName = self.getLongName("layerTreeView",self.objectName())
        self.view.setObjectName(longName)

        self.model = QgsLayerTreeModel(self.layerTreeRoot())
        longName = self.getLongName("layerTreeModel",self.objectName())
        self.model.setObjectName(longName)

        self.model.setFlag( QgsLayerTreeModel.UseEmbeddedWidgets)
        self.model.setFlag( QgsLayerTreeModel.UseTextFormatting)
        self.model.setFlag( QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag( QgsLayerTreeModel.ActionHierarchical)

        self.view.setModel(self.model)           

    def getGroupChildren(self, grouproot_name:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        group =self.layerTreeRoot().findGroup(grouproot_name)
        list_children = group.children()
        return list_children
    

    def getGroupLayers(self, grouproot_name:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        group = self.layerTreeRoot().findGroup(grouproot_name)
        layers = group.findLayers()
        return layers
    

    def renameGroup(self, oldName:str, newName:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")

        group = self.layerTreeRoot().findGroup(oldName)
        group.setName(newName)
        

    def removeAllChildren(self, groupName:str):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")

        root = self.layerTreeRoot()
        layerTreeGroup = root.findGroup(groupName)
        layerTreeGroup.removeAllChildren()
        layerTreeGroup.setExpanded (False)
        layerTreeGroup.setItemVisibilityChecked(False)
        

    def activateDisplayingRule(self, group=None, rukeKey:str = None):
        """
            for each mapLayer in group,
            If rukeKey not None:
                activate only the rule having as key rukeKey value,
                disable all others

            If rukeKey is None, activate ALL rules
        """
        print(f"line:{lineno()},{self.__class__.__name__}->" +
              f"{inspect.currentframe().f_code.co_name}()")

        activateAll = (lambda: False, lambda: True)[rukeKey == None]()
        for layerTreeLayer in group.findLayers():
            mapLayer = layerTreeLayer.layer()
            rootRule = mapLayer.renderer().rootRule().children()[0]

            for rule in rootRule.children():
                rule.setActive(activateAll)

            if rukeKey:
                rule = rootRule.findRuleByKey(rukeKey)
                rule.setActive(True)

            mapLayer.triggerRepaint()


    def createFillSymbolLessSegmentedLayers(self):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        symbol = QgsFillSymbol.createSimple(self.styleSheet_unlabeled)
        renderer = QgsRuleBasedRenderer(symbol)
        return renderer


    def createFillSymbolLastLayer(self,
                         associationTable:dict = None,
                         fieldName:str = "code",
                         yellowOutline:bool = False
                         ):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if yellowOutline:
            symbol = QgsFillSymbol.createSimple(self.styleSheet_unlabeled)
        else:
            symbol = QgsFillSymbol.createSimple(self.styleSheet_transparent)
        renderer = QgsRuleBasedRenderer(symbol)
        rootrule = renderer.rootRule().children()[0]

        for key in associationTable.keys():
            Hex_color = associationTable[key]
            self.styleSheet_labeled["color"] = str(Hex_color)
            sym_n = QgsFillSymbol.createSimple(self.styleSheet_labeled)
            sym_n.setOpacity(0.60)

            expression = f"{fieldName}={key}"
            ruleKey = f"{fieldName}_{key}"
            rule_n = QgsRuleBasedRenderer.Rule(sym_n, 0, 0, expression)
            rule_n.setRuleKey(ruleKey)

            rootrule.appendChild(rule_n)

        mainWindow = self.getMasterWindow()
        currentVintage = self.getVintage()
        otherVintage = None
        for vintage in mainWindow.getVintages():
            if vintage != currentVintage:
                otherVintage = vintage

        if otherVintage is not None:
            currentFieldCode = "code_{}".format(currentVintage)
            otherFieldCode = "code_{}".format(otherVintage)
            symbol_lyr_line = QgsLinePatternFillSymbolLayer()
            symbol_lyr_line.setColor(QColor("red"))
            symbol_lyr_line.setLineWidth(0.5)
            symbol_lyr_line.setCoordinateReference(Qgis.SymbolCoordinateReference.Viewport)
            sym_uncompleted = QgsFillSymbol()
            sym_uncompleted.deleteSymbolLayer(0)
            sym_uncompleted.appendSymbolLayer(symbol_lyr_line)
            for symbolLayer in sym_uncompleted.symbolLayers():
                symbolLayer.setRenderingPass(1)
            
            expression_uncompleted = f"({currentFieldCode} is null and {otherFieldCode} is not null)"
            rule_uncompleted = QgsRuleBasedRenderer.Rule(sym_uncompleted, 0, 0, expression_uncompleted)
            rootrule.appendChild(rule_uncompleted)

        return renderer

    
    def createFillSymbolFromList(self,
                          listLayers: list = None,
                          associationTable: dict = None,
                          fieldName: str = "code"
                          ):
        """ 
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        for i in range(len(listLayers)-1):
            
            tlayer = listLayers[i]
            renderer = self.createFillSymbolLessSegmentedLayers()
            tlayer.layer().setRenderer(renderer)

        renderer = self.createFillSymbolLastLayer(
            associationTable=associationTable,
            fieldName=fieldName
        )
        tlayer = listLayers[-1]
        tlayer.layer().setRenderer(renderer)
    
    
    def setVintage(self, vintage:str=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.vintage = vintage
    
    def getVintage(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return self.vintage
    
    def showCurrentClass(self, showCurrentClass: bool = False):
        print(f"line:{lineno()},{self.__class__.__name__}->" +
              f"{inspect.currentframe().f_code.co_name}()")

        root = self.layerTreeRoot()     
        vintage = self.getVintage()
        group = root.findGroup(f"LABELED_DATA_{vintage}")
        
        print(f"*********group={group}")
        print(f"*********group.name()={group.name()}")

        if showCurrentClass:
            self.activateDisplayingRule(group=group, rukeKey="code_2019_10")
        else:
            self.activateDisplayingRule(group=group)


    def showCodes(self, showCodes:bool = False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass
        
        # root = self.layerTreeRoot()   
        # vintage = self.getVintage()
        # group = root.findGroup(f"LABELED_DATA_{vintage}")
        
        # print(f"*********group={group}")
        # print(f"*********group.name()={group.name()}")
        
        # for layerTreeLayer in group.findLayers():
        #     mapLayer = layerTreeLayer.layer()
        #     mapLayer.setLabelsEnabled(showCodes)
        #     mapLayer.triggerRepaint()
            

    def showContext(self,
                    showContext:bool = False,
                    keepGroup:str = "CONTEXT"
                   ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if showContext:
            groupsName = self.layerTreeRoot().children()
            for group in groupsName:
                if group.name().startswith("LABELED_DATA"):
                    self.groupsVisibilityState[group] = True
                else:
                    self.groupsVisibilityState[group] = group.isVisible()
                if not group.name() == keepGroup:
                    group.setItemVisibilityChecked(not showContext)
        else:
            for group in self.groupsVisibilityState.keys():
                group.setItemVisibilityChecked(
                    self.groupsVisibilityState[group]
                )

            self.groupsVisibilityState.clear()


    def removedChild(self, node=None, indexFrom=None):
        """
        This method is only called by the instance of
        TnTLayerTreeWidget_Master; and only applies to LABELED_DATA
        and FINAL_DATA groups
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        root = self.layerTreeRoot()
        try:
            group = root.findGroup(node.name())

            layer = group.findLayers()[indexFrom]
            vLayer = layer.layer()
            id_vLayer = vLayer.id()
            
            QgsProject.instance().removeMapLayer(id_vLayer)
            
            group.removeChildNode(layer)

            group.setExpanded(False)
            group.setItemVisibilityChecked(False)

        except AttributeError:
            pass
            

    def addedChild(self, node=None, indexFrom=None):
        """
        This method is only called by the instance of
        TnTLayerTreeWidget_Master; and only applies to LABELED_DATA
        or FINAL_DATA groups
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        root = self.layerTreeRoot()
        try:
            treeLayer = node.findLayers()[indexFrom]
            vLayer_Clone = treeLayer.layer().clone()
            tLayer = QgsLayerTreeLayer(vLayer_Clone)

            vintage = self.getVintage()

            tLayer.setExpanded(False)
            #A corriger pb d'initialisation des visibilities
            #tLayer.setItemVisibilityChecked(False)

            QgsProject.instance().addMapLayer(
                vLayer_Clone,
                addToLegend=False
            )

            nodeName = node.name()
            
            if nodeName.startswith("LABELED_DATA"):
                groupName = f"LABELED_DATA_{vintage}"
                tLayer.setItemVisibilityChecked(False)
            else :
                groupName = node.name()
                tLayer.setItemVisibilityChecked(True)

            group = root.findGroup(groupName)
            group.addChildNode(tLayer)
            group.setExpanded(True)
            group.setItemVisibilityChecked(False)

        except AttributeError:
            pass


    def showContextVintageGroup(self):
        """
            Initialize all visibility and expanded group to false;
            except group named "CONTEXT_<vintage>".
            
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        root = self.model.rootGroup()
        groups = root.findGroups(recursive=False)
        
        for group in groups :
            group.setItemVisibilityCheckedRecursive(False)
            group.setExpanded(False)
        
        vintage = self.getVintage()
        group = root.findGroup(f"CONTEXT_{vintage}")
        group.setItemVisibilityCheckedRecursive(True)
        group.setExpanded(False)
     
        
    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.setVintage (self.getMainWindow().getVintage())
        self.showContextVintageGroup()

    def start(self,
              tntlayers_Manager:TnTLayersManager=None
             ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        vintage = self.getVintage()
        oldName = "LABELED_DATA"
        newName = f"{oldName}_{vintage}"  
        self.renameGroup(oldName, newName)
        
        root = self.layerTreeRoot()
        
        group = root.findGroup("FINAL_DATA")
        group.setExpanded(False)
        group.setItemVisibilityChecked(False)
        
        group = root.findGroup("SEGMENTED_DATA")
        group.setExpanded(False)
        group.setItemVisibilityChecked(False)
          
          
    def stop(self,
             tntlayers_Manager:TnTLayersManager = None
             ):
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")
 
        vintage = self.getVintage()
        newName = "LABELED_DATA"
        oldName = f"{newName}_{vintage}"

        self.removeAllChildren(oldName)
        self.renameGroup(oldName, newName)
         
        root = self.layerTreeRoot()
        
        group = root.findGroup("FINAL_DATA")
        group.setItemVisibilityChecked(False)
        
        group = root.findGroup("SEGMENTED_DATA")
        group.setExpanded(False)
        group.setItemVisibilityChecked(False)
        
    
    # def getActivatedLayer(self, grouproot_name):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")
    #     group =self.root.findGroup(grouproot_name)
    #     list_children = group.children()
    #     for child in list_children :
    #         if child.a
    #         print(f"child={child}-{child.name()}")



class TnTLayerTreeWidget_Master(TnTLayerTreeWidget):

    def __init__( self,
                  parent = None,
                  objectName = "TnTLayerTreeWidget_Master"
                ):

        super().__init__( parent= parent,
                          objectName = objectName
                        )

    def setLayerTreeRoot(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        self.root = QgsProject.instance().layerTreeRoot()


    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        super().setConnections()
        treeRoot = self.layerTreeRoot()

        treeRoot.removedChildren[QgsLayerTreeNode, int, int].connect(
            self.removedChildren
        )

        treeRoot.addedChildren[QgsLayerTreeNode, int, int].connect(
            self.addedChildren
        )
        

    def start( self,
               tntlayers_Manager:TnTLayersManager=None
             ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclatureWidget = self.getTnTnomenclatureWidget()
        associationTable = nomenclatureWidget.getAssociationTable()
        nomenclatureName = nomenclatureWidget.getComboBox().currentText()
        
        tntlayers_Manager.loadLabeledData(
            associationTable=associationTable,
            nomenclatureName=nomenclatureName
        )

        vintage = self.getVintage()

        oldName = "LABELED_DATA"
        newName = f"{oldName}_{vintage}"
        self.renameGroup(oldName, newName)

        root = self.layerTreeRoot()
        group = root.findGroup(newName)

        self.createFillSymbolFromList(
            listLayers=group.findLayers(),
            associationTable=associationTable,
            fieldName=f"code_{vintage}"
        )

        masterWindow = self.getMasterWindow()
        layerTreeWidget = masterWindow.associatedWindow.findChild(
            TnTLayerTreeWidget
        )
        vintage = masterWindow.associatedWindow.getVintage()
        newName = f"{oldName}_{vintage}"
        root = layerTreeWidget.layerTreeRoot()
        group = root.findGroup(newName)
        layerTreeWidget.createFillSymbolFromList(
            listLayers=group.findLayers(),
            associationTable=associationTable,
            fieldName=f"code_{vintage}"
        )

         
        group = root.findGroup("FINAL_DATA")
        group.setExpanded(False)
        group.setItemVisibilityChecked(False)
        
        group = root.findGroup("SEGMENTED_DATA")
        group.setExpanded(False)
        group.setItemVisibilityChecked(False)


    # def stop(self,
    #           tntlayers_Manager:TnTLayersManager=None
    #         ):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")

    #     vintage = self.getVintage()
    #     name = "LABELED_DATA"
    #     groupName = f"{name}_{vintage}"

    #     self.removeAllChildren(groupName)
    #     self.renameGroup(groupName, name)
        


    @QtCore.pyqtSlot( QgsLayerTreeNode, int, int)
    def removedChildren(self, node, indexFrom, indexTo):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if node.name() == "FINAL_DATA":
            masterWindow = self.getMasterWindow()
            layerTreeWidget = masterWindow.associatedWindow.findChild(
                TnTLayerTreeWidget
            )

            layerTreeWidget.removedChild(
                node=node,
                indexFrom=indexFrom
            )


    @QtCore.pyqtSlot( QgsLayerTreeNode, int, int)
    def addedChildren(self, node, indexFrom, indexTo):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nodeName = node.name()
        if nodeName.startswith("LABELED_DATA") or node.name() == "FINAL_DATA":
            masterWindow = self.getMasterWindow()
            layerTreeWidget = masterWindow.associatedWindow.findChild(
                TnTLayerTreeWidget
            )

            layerTreeWidget.addedChild(
                node=node,
                indexFrom=indexFrom
            )
