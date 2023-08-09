# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 14:43:12 2023

@author: YLe-Borgne
"""

import inspect

from PyQt5.QtWidgets import( QSizePolicy, QWidget, QVBoxLayout,
                             QDockWidget, QLabel, QTreeWidgetItem,
                             QTreeWidget
                           )

from .TnT_WidgetsGroup import( TnTnomenclatureWidget,
                               TnTnomenclatureWidget_Master,
                               TnTLayerTreeWidget,
                               TnTLayerTreeWidget_Master
                             )
from .TnT_ProjectManager import( TnTLayersManager )


def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno

class TraiNminaTor2_DockWidget( QDockWidget ):
    def __init__( self,
                  title="TraiNminaTor2_DockWidget",
                  parent=None,
                  objectName="TraiNminaTor2_DockWidget"
                 ):

        super().__init__( title,
                          parent
                        )
        super().setFeatures(super().features() & ~
                            QDockWidget.DockWidgetClosable)
        self.setObjectName(objectName)
        self.setAccessibleName(objectName)

        self.setupLayout()
        self.setDefaultSizePolicy()

        self.setupUi()

    def setDefaultSizePolicy(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sizePolicy = QSizePolicy(QSizePolicy.Minimum,
                                 QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)


    def setupLayout(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        dockWidgetContents = QWidget()
        dockWidgetContents.setLayout( QVBoxLayout(self) )
        layout = dockWidgetContents.layout()

        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(10)

        self.setWidget(dockWidgetContents)

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass



class TnTLayerTree_DockWidget( TraiNminaTor2_DockWidget ): 
    
    def __init__( self,
                  title="TnTLayerTree_DockWidget",
                  parent=None,
                  objectName="TnTLayerTree_DockWidget"
                 ):

        super().__init__( title = title,
                          parent = parent,
                          objectName = objectName
                        )

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        dockWidgetContents = self.widget()
        layout = dockWidgetContents.layout()
        layerTree_Widget = self.initTnTLayerTreeWidget(dockWidgetContents)
        layout.addWidget(layerTree_Widget)

    def initTnTLayerTreeWidget(self, parent:QWidget=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTree_Widget = TnTLayerTreeWidget(parent)
        return layerTree_Widget

    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.standardMode()

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.differentialMode()

        
    def start( self, 
               tntlayers_Manager:TnTLayersManager=None
             ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.start(tntlayers_Manager=tntlayers_Manager)

    
    def stop( self, 
              tntlayers_Manager:TnTLayersManager=None
            ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.stop(tntlayers_Manager=tntlayers_Manager)
        
        
    def showCurrentClass(self, showCurrentClass:bool=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.showCurrentClass(showCurrentClass=showCurrentClass)
        
        
    def showCodes(self, showCodes:bool=False, wantedGroupName:str="LABELED_DATA"):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.showCodes(showCodes=showCodes, wantedGroupName=wantedGroupName)
        
        
    def showContext(self, showContext:bool=False, keepGroup:str="CONTEXT" ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.showContext(showContext=showContext, keepGroup=keepGroup)
        

    # def lockGroupByType(self, groupsTypeList=None) :
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")
    #     pass

    # def unlockGroupByType(self, groupsTypeList=None):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")
    #     pass


class TnTLayerTree_DockWidget_Master( TnTLayerTree_DockWidget ): 
    
    def __init__( self,
                  title="TnTLayerTree_DockWidget_Master",
                  parent=None,
                  objectName="TnTLayerTree_DockWidget_Master"
                 ):

        super().__init__( title = title,
                          parent = parent,
                          objectName = objectName
                        )


    def initTnTLayerTreeWidget(self, parent:QWidget=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTree_Widget = TnTLayerTreeWidget_Master(parent)
        return layerTree_Widget

    # def standardMode(self):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")
    #     pass

    # def differentialMode(self,  vintage="No Value"):
    #     # print(f"line:{lineno()},{self.__class__.__name__}->"+
    #     #       f"{inspect.currentframe().f_code.co_name}()")
    #     layerTreeWidget = self.findChild(TnTLayerTreeWidget_Master)
    #     layerTreeWidget.differentialMode(vintage=vintage)
    
    def start( self, 
               tntlayers_Manager:TnTLayersManager=None
             ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.start(tntlayers_Manager=tntlayers_Manager)


    def stop( self, 
              tntlayers_Manager:TnTLayersManager=None
            ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTreeWidget = self.findChild(TnTLayerTreeWidget)
        layerTreeWidget.stop(tntlayers_Manager=tntlayers_Manager)
    
    
class TnTNomenclature_DockWidget( TraiNminaTor2_DockWidget ):
    def __init__( self,
                  title="TnTNomenclature_DockWidget",
                  parent=None,
                  objectName="TnTNomenclature_DockWidget"
                 ):

        super().__init__( title = title,
                          parent = parent,
                          objectName = objectName
                        )

    def setupUi(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        dockWidgetContents = self.widget()
        layout = dockWidgetContents.layout()
        nomenclature_Widget = self.initTnTnomenclatureWidget(dockWidgetContents)
        layout.addWidget(nomenclature_Widget)

    def initTnTnomenclatureWidget(self, parent:QWidget=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclature_Widget = TnTnomenclatureWidget(parent)
        return nomenclature_Widget

    def updateCurrentNomenclatureLabel( self,
                                        currentNomenclature_text:str="No value"
                                       ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        labelValue = self.parent().findChild(
            QLabel,
            "labelValue_CurrentNomenclature"
        )
        labelValue.setText(currentNomenclature_text)

    def currentNomenclatureChanged( self, 
                                    nomenclatureName:str=None,
                                    treeWidgetSrc:QTreeWidget=None
                                  ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclature_Widget = self.findChild(TnTnomenclatureWidget)
        nomenclature_Widget.currentNomenclatureChanged(
            treeWidgetSrc=treeWidgetSrc
        )

    def itemSelectionChanged(self, itemSelected:QTreeWidgetItem=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.parent().centralWidget().itemSelectionChanged(
            itemSelected=itemSelected
        )

    def standardMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def differentialMode(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        nomenclatureWidget = self.findChild(TnTnomenclatureWidget)
        nomenclatureWidget.differentialMode()

    def lockGroupByType(self, groupsTypeList=None) :
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.parent().centralWidget().lockGroupByType(
            groupsTypeList=groupsTypeList
        )

    def unlockGroupByType(self, groupsTypeList=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.parent().centralWidget().unlockGroupByType(
            groupsTypeList=groupsTypeList
        )

    def start(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass


    def stop(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass


class TnTNomenclature_DockWidget_Master( TnTNomenclature_DockWidget ):
    def __init__( self,
                  title="nomenclature_dockWidget_Master",
                  parent=None,
                  objectName="nomenclature_dockWidget_Master"
                ):

        super().__init__( title = title,
                          parent = parent,
                          objectName = objectName
                        )

    def initTnTnomenclatureWidget(self, parent:QWidget=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        nomenclature_Widget = TnTnomenclatureWidget_Master(parent)
        return nomenclature_Widget
