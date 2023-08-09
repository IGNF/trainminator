# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:19:09 2023

@author: YLe-Borgne
"""
import os
import inspect
import re

from qgis.utils import iface
from qgis.core  import (QgsProject, QgsVectorLayer, QgsLayerTreeLayer,
                        QgsWkbTypes, QgsRuleBasedRenderer, QgsVectorFileWriter,
                        QgsFillSymbol,QgsField, QgsPalLayerSettings,
                        QgsTextFormat, QgsTextBufferSettings,
                        QgsVectorLayerSimpleLabeling,
                        QgsLinePatternFillSymbolLayer)

from PyQt5           import QtCore, Qt
from PyQt5.QtCore    import QVariant

from PyQt5.QtWidgets import QProgressDialog, QMessageBox
from PyQt5.QtGui     import (QColor, QFont)


def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno

class TnTProjectChecker():
    """
        This class controls the current Qgis project
    """

    def __init__(self, project=QgsProject.instance() ):

        self.project = project
        self.projectName = self.project.baseName()
        self.absoluteFilePath = self.project.absoluteFilePath()
        self.absolutePath = self.project.absolutePath()
        self.layerTreeRoot = self.project.layerTreeRoot()

        self.vintages = []

        self.mandatoryGroups=None
        self.projectValid=True
        self.messages=[]

        self.setMandatoryGroups()

    def checkIsDifferential(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        groups = self.layerTreeRoot.findGroups(recursive=False)
        groups_name = []
        for group in groups:
            result = re.search("CONTEXT_[0-9][0-9][0-9][0-9]", group.name())
            if result:
                groups_name.append(result.group(0))

        if groups_name :

            self.vintages = self.setVintages(groups_name)
            return True
        else :
            self.vintages = []
            return False

    def setVintages(self, names):
        """
        Creation of the Vintages list from the group name list.
        return  a simple ascending sort of the vintages list.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        vintages = []
        for name in names:
            vintages.append(name.split('_')[1])
        vintages.sort()
        return vintages

    def getVintages(self):
        """
        Returns the sorted vintages list.
        """
        return self.vintages

    def setMandatoryGroups(self):
        """
        Initialize the list of mandatory groups.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.mandatoryGroups=['CONTEXT',
                              'SEGMENTED_DATA',
                              'LABELED_DATA',
                              'FINAL_DATA']

    def updateMandatoryGroups(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        vintages = self.vintages.copy()
        vintages.reverse()

        self.mandatoryGroups.remove('CONTEXT')
        for vintage in vintages :
            self.mandatoryGroups.insert(0,f"CONTEXT_{vintage}")


    def setAllVisibility(self, checked=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        for groupName in self.mandatoryGroups:
            self.setVisibility( groupName=groupName,
                                checked=checked
                              )

    def setVisibility(self, groupName=None, checked=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeGroup = self.layerTreeRoot.findGroup(groupName)
        layerTreeGroup.setItemVisibilityChecked(checked)


    def setAllExpanded(self, expanded=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        for groupName in self.mandatoryGroups:
            self.setExpanded( groupName=groupName,
                              expanded=expanded
                            )

    def setExpanded(self, groupName=None, expanded=False):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        layerTreeGroup = self.layerTreeRoot.findGroup(groupName)
        layerTreeGroup.setExpanded(expanded)


    def checkProject(self):
        """
        Test the content of the current QGis project.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.checkMandatoryGroups()
        self.cleanGroups(["LABELED_DATA", "FINAL_DATA"])

        self.sorting_SegmentedData("SEGMENTED_DATA")

        if not self.projectValid:
            self.showMessage(self.messages)

        return self.projectValid

    def checkMandatoryGroups(self):
        """
        Checks for the existence of required groups.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        for groupsName in self.mandatoryGroups:
            if not self.layerTreeRoot.findGroup(groupsName):
                msg=f'Mandatory group:{groupsName} doesn\'t exist.'
                self.messages.append(msg)
                self.projectValid=False
            else:
                self.checkLayersValidity(groupsName)


    def checkLayersValidity (self, groupName, removeOnly=True):
        """
            param groupName:The name of the target group.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        group=self.layerTreeRoot.findGroup(groupName)
        tLayers=group.findLayers()

        for tLayer in tLayers :
            if not tLayer.layer().isValid():
                if removeOnly :
                    id_layer=tLayer.layer().id()
                    self.project.removeMapLayer(id_layer)
                else :
                    msg=f'layer:{tLayer.layer().name()} not valid.'
                    self.messages.append(msg)
                    self.projectValid=False

    def cleanGroups(self, groupName_List):
        """
         Remove all group cards from the list.
            param groupName_List:list of groups.
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        for groupName in groupName_List:
            self.cleanGroup(groupName)

    def cleanGroup(self, groupName):
        """
         Remove all maps from the target group "groupName"
            param groupName:The name of the group to clean
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        group=self.layerTreeRoot.findGroup(groupName)
        tLayers=group.findLayers()
        for tLayer in tLayers:
            id_layer=tLayer.layer().id()
            self.project.removeMapLayer(id_layer)

    def sorting_SegmentedData(self, groupName):
        """ Sort data from segmented data group """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        sorted_segs = []
        sorted_segs = self.sortAscending_SegmentedData( groupName )
        self.writing_SortedSegmentedData( sorted_segs )

    def sortAscending_SegmentedData(self, groupName):
        """ Sort segmented data from most to least segmented """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        segmentedDataGroup = self.layerTreeRoot.findGroup(groupName)
        sorted_segments = []
        segments = {}
        for tLayer in segmentedDataGroup.findLayers():
            polygonNumber = 0

            for feat in tLayer.layer().getFeatures():
                geom = feat.geometry()
                if geom.type() == QgsWkbTypes.PolygonGeometry:
                    polygonNumber += 1
            segments[tLayer] = polygonNumber

        sort_segments = sorted(segments.items(),
                               key=lambda x: x[1],
                               reverse=False
                               )
        for values in sort_segments:
            tLayer = values[0]
            tLayer.setExpanded(False)
            tLayer.setItemVisibilityChecked(False)
            sorted_segments.append(tLayer)
        return sorted_segments

    def writing_SortedSegmentedData(self, sortedSegmentedData):
        """ writing sorted segmented data in group parent. """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        index = 1
        for segmentedData in sortedSegmentedData:
            vLayer = self.project.mapLayersByName(
                segmentedData.layer().name()
            )[0]
            vLayer_treeLayer = self.layerTreeRoot.findLayer(vLayer.id())

            vLayer_treeLayer_clone = vLayer_treeLayer.clone()

            parent_group = vLayer_treeLayer.parent()
            parent_group.insertChildNode(index,
                                         vLayer_treeLayer_clone
                                         )
            vLayer_treeLayer_clone.setExpanded(False)
            vLayer_treeLayer_clone.setItemVisibilityChecked(False)

            parent_group.removeChildNode(segmentedData)
            index += 1

    def clear(self):
        """
        This method is executed when the project is cleared (and additionally
        when an open project is cleared just before a new project is read).
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        self.project = None
        self.projectName = None
        self.absoluteFilePath = None
        self.absolutePath = None
        self.layerTreeRoot = None

        self.mandatoryGroups=None
        self.projectValid=True
        self.messages=[]


    def showMessage(self, messages, icon=QMessageBox.Information):
        """
        Show errors.
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        messageBox = QMessageBox()
        messageBox.setIcon(icon)
        messageBox.setWindowTitle("TrainMinaTor message")
        messageBox.setText('\n'.join(messages))
        messages.clear()
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

class TnTLayersManager():
    def __init__(self,
                 parent=None,
                 project=QgsProject.instance()
                 ):

        self.project = project
        self.projectName = self.project.baseName()
        self.absoluteFilePath = self.project.absoluteFilePath()
        self.absolutePath = self.project.absolutePath()
        self.layerTreeRoot = self.project.layerTreeRoot()

        self.parent = parent
        self.isDifferential = parent.isDifferential
        self.vintages = parent.getVintages()

        self.dictCodeRuleKey = {}

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

        self.styleSheet_labeled = { "color":"",
                                    "outline_color":"black",
                                    "width_border":"0.10",
                                    "style":"solid"
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

    def getVintages(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()"
        
        return self.vintages


    def addTreeLayerTreeControl(self, groupName, tLayer, suffixe="CTRL"):
        """

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        iface.setActiveLayer( tLayer.layer() )
        activeLayer = iface.activeLayer()
        new_layerName = f"{activeLayer.name()}_{suffixe}"

        new_layer=iface.addVectorLayer(activeLayer.source(),
                                       new_layerName,
                                       activeLayer.providerType())

        new_layer.setName(new_layerName)

        self.createFillSymbolControl(new_layer,'"code" IS NULL')

        target_group=self.getRootGroup().findGroup(groupName)
        target_group.setItemVisibilityChecked(True)


    def createAttributs( self,
                         vlayer=None,
                         attributs={"color":QVariant.Int,
                                    "code":QVariant.Int,
                                    "libelle":QVariant.String}
                       ):
        """

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pr = vlayer.dataProvider()
        field_names = [field.name() for field in pr.fields()]
        #for attribut in self.tableAttributs:
        for attribut in attributs.keys():
            if not attribut in field_names:
                # <name>, <type>
                pr.addAttributes([QgsField(attribut, attributs[attribut])])
        vlayer.updateFields()

    def createDataLabeled(self,
                          fullPathName=None,
                          layer_Source=None
                          ):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        vlayer_source = layer_Source.layer()
        data_name = vlayer_source.name()

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = vlayer_source.dataProvider().storageType()
        transformContext = self.project.transformContext()

        QgsVectorFileWriter.writeAsVectorFormatV3(vlayer_source,
                                                  fullPathName,
                                                  transformContext,
                                                  options
                                                  )

        vlayer_DataLabeled = QgsVectorLayer(fullPathName,
                                            data_name,
                                            "ogr")

        # print(f"creation fullPathName={fullPathName}")
        # print(f"creation data_name={data_name}")

        if self.isDifferential:
            attributs = {f"color_{self.vintages[0]}": QVariant.Int,
                         f"code_{self.vintages[0]}": QVariant.Int,
                         f"class_{self.vintages[0]}": QVariant.String,
                         f"color_{self.vintages[1]}": QVariant.Int,
                         f"code_{self.vintages[1]}": QVariant.Int,
                         f"class_{self.vintages[1]}": QVariant.String,
                         }
        else:
            attributs = {"color": QVariant.Int,
                         "code": QVariant.Int,
                         "class": QVariant.String
                         }

        self.createAttributs(vlayer=vlayer_DataLabeled,
                              attributs=attributs
                            )
        return vlayer_DataLabeled

    # def renameGroup(self, groupSrcName=None , groupDstName=None):
    #     print(f"line:{lineno()},{self.__class__.__name__}->"+
    #           f"{inspect.currentframe().f_code.co_name}()")

    def createGroup(self, grouName=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass


    def deleteGroup(self, grouName=None):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        pass

    def loadLabeledData(self,
                        associationTable=None,
                        nomenclatureName="OCS"
                       ):
        """
            param nomenclatureWidget:
            returns none:
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->" +
        #       f"{inspect.currentframe().f_code.co_name}()")

      
        # progress=self.showDialog(self.parent, "Loading", "Loading labeled data...")
        # progress.setMinimum(0)
        # progress.setMaximum(len(listDataSegmented))

        group_Name = "LABELED_DATA"
        AbsolutePath_DataLabeled = f"{self.absolutePath}/{group_Name}/{nomenclatureName.upper()}"
    
        labeled_Group = self.layerTreeRoot.findGroup(group_Name)

        segmented_Group = self.layerTreeRoot.findGroup("SEGMENTED_DATA")
        listDataSegmented = segmented_Group.children()

        # progress=self.showDialog(self.parent, "Loading", "Loading labeled data...")
        # progress.setMinimum(0)
        # progress.setMaximum(len(listDataSegmented))

        index = 1
        # progress.setValue(0)
        for dataSegmented in listDataSegmented:

            filedata_name = os.path.split(
                dataSegmented.layer().dataProvider().dataSourceUri())[1]
            data_name = filedata_name.split('.')[0]
            FullPathName_DataLabeled = AbsolutePath_DataLabeled+"/"+filedata_name

            if os.path.isfile(FullPathName_DataLabeled):
                vlayer_DataLabeled = QgsVectorLayer(FullPathName_DataLabeled,
                                                    data_name,
                                                    "ogr")
                #self.checkAttributs(nomenclatureWidget, vlayer_DataLabeled)

                if vlayer_DataLabeled.isValid():
                    print(f"Reload/Load data {FullPathName_DataLabeled}")
                else:
                    vlayer_DataLabeled = None
                    print("Layer failed to load!")

            else:
                os.makedirs(AbsolutePath_DataLabeled, exist_ok=True)
                vlayer_DataLabeled =self.createDataLabeled(
                                      fullPathName=FullPathName_DataLabeled,
                                      layer_Source=dataSegmented)
                                     
              
            if vlayer_DataLabeled:

                QgsProject.instance().addMapLayer(vlayer_DataLabeled, False)
                layerTreeLayer_DataLabeled = QgsLayerTreeLayer(
                    vlayer_DataLabeled
                )
                labeled_Group.insertChildNode(
                    index, layerTreeLayer_DataLabeled
                )

                layerTreeLayer_DataLabeled.setExpanded(False)
                layerTreeLayer_DataLabeled.setItemVisibilityChecked(False)

                # progress.setValue(progress.value()+1)
                index += 1

        # progress.setLabelText("Loading data Done.")
        # progress.setValue(progress.maximum())
        # progress.close()


    def createFillSymbol( self,
                          associationTable=None,
                          fieldName="code"
                        ):
        """
        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        symbol = QgsFillSymbol.createSimple(self.styleSheet_unlabeled)
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

        # layer.setRenderer(renderer)
        return renderer


    def createLabel(self, fieldName="code"):
        """
        Constructs simple labeling configuration with given initial settings.
        The text will contain the fieldName field value.
        Using when user want to show labels
            param fieldName:
            returns label: return a new simple labeling configuration with given initial settings.
        """

        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        settings=QgsPalLayerSettings()
        text_format = QgsTextFormat()
        text_format.setFont(QFont('Arial', 8))
        text_format.setColor(QColor('Black'))
        buffer = QgsTextBufferSettings()
        buffer.setEnabled(True)
        buffer.setSize(0.50)
        buffer.setColor(QColor('grey'))
        text_format.setBuffer(buffer)
        settings.setFormat(text_format)
        settings.fieldName = fieldName
        settings.isExpression = False
        label = QgsVectorLayerSimpleLabeling(settings)
        return label


    def  removeAllChildren(self, groupsName:list):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        for groupName in groupsName :
            layerTreeGroup = self.layerTreeRoot.findGroup(groupName)
            layerTreeGroup.removeAllChildren()
            layerTreeGroup.setExpanded (False)
            layerTreeGroup.setItemVisibilityChecked(False)


    def removedChild(self, groupName, index):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        layerTreeGroup = self.layerTreeRoot.findGroup(groupName)

        layerTreeNode = layerTreeGroup.findLayers()[index]
        layerTreeGroup.removeChildNode(layerTreeNode)

        layerTreeGroup.setExpanded (False)
        layerTreeGroup.setItemVisibilityChecked(False)


    def showMessage(self, messages, icon=QMessageBox.Information):
        """
        Parameters
        ----------
        messages : TYPE
            DESCRIPTION.
        icon : TYPE, optional
            DESCRIPTION. The default is QMessageBox.Information.

        Returns
        -------
        None.

        """
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        messageBox = QMessageBox()
        messageBox.setIcon(icon)
        messageBox.setWindowTitle("TrainMinaTor message")
        messageBox.setText('\n'.join(messages))
        messages.clear()
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def showDialog(self, windowTitle, labelText):
        """
            param parent:
            param windowTitle:
            param labelText:
            returns none:
        """
       # print(f"line:{lineno()},{self.__class__.__name__}->"+
       #       f"{inspect.currentframe().f_code.co_name}()")
       
        progress = QProgressDialog()
        progress.setWindowTitle(windowTitle)
        progress.setLabelText(labelText)
        progress.setCancelButtonText(None)
        progress.setMinimumDuration(5)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setAutoClose(False)
        progress.setAutoReset(False)
        return progress

class TnTProjectManager():
    """
        This class manages the data of the current project.
    """
    def __init__(self, parent, project=QgsProject.instance()):
        self.parent = parent
        self.project = project

        self.tnTProjectObject = None

        self.isValid = False
        self.isDifferential = False
        self.vintages = []

        self.setConnections()

    def setConnections(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.project.readProject.connect(self.updateProject)

    def setVintages(self, vintages):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.vintages = vintages

    def getVintages(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        return self.vintages


    def setUserInterface(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        if self.isDifferential :
            # print("mode differential")
            self.parent.differentialMode()
        else :
            # print("mode standard")
            self.parent.standardMode()


    def checkIsDifferential(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        
        self.isDifferential = self.tnTProjectObject.checkIsDifferential()
        if self.isDifferential :
            self.setVintages( self.tnTProjectObject.getVintages() )

        else :
            self.isDifferential=False

    def updateProject(self, domDocument):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")
        # =============================================
        #         print(f"domDocument={domDocument}")
        #         print(f"{domDocument.toString(4)}")
        # =============================================

        self.tnTProjectObject = TnTProjectChecker()

        self.checkIsDifferential()

        if self.isDifferential:
            self.tnTProjectObject.updateMandatoryGroups()

        self.isValid = self.tnTProjectObject.checkProject()

        if self.isValid:
            #All group not expanded , not visible
            self.tnTProjectObject.setAllExpanded(False)
            self.tnTProjectObject.setAllVisibility(False)

            # set visibility True for CONTEXT_* group
            for groupName in self.tnTProjectObject.mandatoryGroups:
                if groupName.startswith("CONTEXT"):
                    self.tnTProjectObject.setVisibility(
                        groupName=groupName,
                        checked=True
                    )

            self.tnTProjectObject = TnTLayersManager(parent=self)

            self.setUserInterface()
        else:
            print("project not valid!")


    def clear(self):
        # print(f"line:{lineno()},{self.__class__.__name__}->"+
        #       f"{inspect.currentframe().f_code.co_name}()")

        pass
