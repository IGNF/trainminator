
from qgis.core import (QgsProject, QgsVectorLayer,
                       QgsLayerTreeLayer, QgsVectorFileWriter, Qgis)

from .TnT_MapCanvas import mapCanvas

import os
import inspect
import processing
import glob
from qgis.utils import iface


def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno


class TnTSavingLabeledData:

    def __init__(self, masterWindow):
        self.masterWindow = masterWindow

        self.workGroupName='FINAL_DATA'


    
    def cleanData(self):
        """
            Remove previous final layer (in FINAL_DATA group)
        """
        
        layerTreeWidget = self.masterWindow.getTnTLayerTreeWidget()
        root = layerTreeWidget.layerTreeRoot()
        group = root.findGroup(self.workGroupName)
        
        layers = group.findLayers()
        if layers :
            vLayer = layers[0].layer()
            id_vLayer = vLayer.id()
             
            QgsProject.instance().removeMapLayer(id_vLayer)
            group.removeAllChildren()
            
        absolutePathFinalData=self.getAbsolutePathFinalData()
        if absolutePathFinalData :
            files = glob.glob(f"{absolutePathFinalData}/*.*")
            for f in files:
                os.remove(f)


    def getAbsolutePathFinalData(self):
        
        return self.absolutePathFinalData


    def setAbsolutePathFinalData(self, path:str=None):
        
        self.absolutePathFinalData = path


    def createDir(self, dirName:str=None):
        
        projectAbsolutePath=QgsProject.instance().absolutePath()
        AbsolutePath_FinalData=f"{projectAbsolutePath}/{dirName}"
        os.makedirs(AbsolutePath_FinalData, exist_ok=True)
        self.setAbsolutePathFinalData(AbsolutePath_FinalData)


    def createFinalLayer(self, group=None, vLayer=None):
        
        transformContext = QgsProject.instance().transformContext()
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = vLayer.dataProvider().storageType()

        AbsolutePath_FinalData = self.getAbsolutePathFinalData()

        finalFileName = vLayer.name()+"_Final"
        fullPathName_FinalData = AbsolutePath_FinalData+"/"+finalFileName+".shp"

        error = QgsVectorFileWriter.writeAsVectorFormatV3(
            vLayer,
            fullPathName_FinalData,
            transformContext,
            options
        )

        if error[0] != QgsVectorFileWriter.NoError:
            print(f"line:{lineno()}, writeAsVectorFormatV3 fail")

        vlayer_Final = QgsVectorLayer(fullPathName_FinalData,
                                      finalFileName,
                                      "ogr"
                                      )

        self.idVlayer_Final = vlayer_Final.id()

        new_renderer = vLayer.renderer().clone()
        vlayer_Final.setRenderer(new_renderer)

        QgsProject.instance().addMapLayer(vlayer_Final, False)

        tLayer_Final = QgsLayerTreeLayer(vlayer_Final)
        tLayer_Final.setExpanded(False)

        group.insertChildNode(-1, tLayer_Final)


    def getMostSegmentedLayer(self):
        """
        get the most segmented layer
        """
        layerTreeWidget = self.masterWindow.getTnTLayerTreeWidget()
        root = layerTreeWidget.layerTreeRoot()

        vintage = self.masterWindow.getVintage()
        if vintage:
            groupName = f"LABELED_DATA_{vintage}"
        else:
            groupName = "LABELED_DATA"
        group = root.findGroup(groupName)
        layers = group.findLayers()
        return layers[-1].layer()
    
    
    def request(self, vlayerFinal, field_Code1, field_Code2):
        param_sel1 = {'INPUT': vlayerFinal,
                              'FIELD': field_Code1,
                              'OPERATOR': 8,  # 8= 'is null'
                              'METHOD': 0
                              }
        processing.run('qgis:selectbyattribute', param_sel1)

        param_sel2 = {'INPUT': vlayerFinal,
                              'FIELD': field_Code2,
                              'OPERATOR': 9,  # 9= 'is not null'
                              'METHOD': 3
                              }
        result = processing.run('qgis:selectbyattribute', param_sel2)
        return result


    def returnErrorMessage(self, count0, count1, vintages, vlayerFinal:QgsVectorLayer):
        # return error message
        iface.messageBar().pushMessage("Error", "{} features are not completed in vintage {} and {} in vintage {}".format(count0, vintages[0], count1, vintages[1]), level=Qgis.Critical)
        
        # Zoom on the first feature not completely labelised
        feature0 = vlayerFinal.selectedFeatures()[0]
        geometry = feature0.geometry()
        bbox = geometry.boundingBox()
        map_Canvas = self.masterWindow.findChild(mapCanvas)
        map_Canvas.setExtent(bbox)

        map_Canvas_associated_window = self.masterWindow.associatedWindow.findChild(mapCanvas)
        map_Canvas_associated_window.setExtent(bbox)

        masterSliderGroup = self.masterWindow.getSliderGroup()
        masterSliderGroup.setMaximum()

        associatedSliderGroup = self.masterWindow.associatedWindow.getSliderGroup()
        associatedSliderGroup.setMaximum()


    def checkCompletion(self, vlayerFinal):

        error = True
        # get vintages
        vintages = self.masterWindow.getVintages()

        # Get field_codes
        field_codes = ["code_{}".format(vintage) for vintage in vintages]
        
        # First request : features not labelised in vintage 1 and labelised in vintage 2
        result0 = self.request(vlayerFinal, field_codes[0], field_codes[1])
        count0 = result0['OUTPUT'].selectedFeatureCount()

        result1 = self.request(vlayerFinal, field_codes[1], field_codes[0])
        count1 = result1['OUTPUT'].selectedFeatureCount()

        if count0 > 0 or count1 > 0:
            if count1 == 0:
                self.request(vlayerFinal, field_codes[0], field_codes[1])
            self.returnErrorMessage(count0, count1, vintages, vlayerFinal)
        else:
            iface.messageBar().pushMessage("Success !", "", level=Qgis.Success, duration=0)
            error = False

        vlayerFinal.removeSelection()
        return error


    def save(self):
        
        # get most segmented layer
        masterMostSegmentedLayer = self.getMostSegmentedLayer()

        # Check that each feature labelised in a vintage is labelised in the other vintage
        error = self.checkCompletion(masterMostSegmentedLayer)
        
        # get nomenclature name : final layer will be saved in "FINAL_DATA/[nomenclature_name]"
        nomenclatureWidget = self.masterWindow.getTnTnomenclatureWidget()
        nomenclatureName = nomenclatureWidget.getComboBox().currentText()

        # create directory "FINAL_DATA/[nomenclature_name]"
        self.createDir(dirName=f"{self.workGroupName}/{nomenclatureName.upper()}")

        # remove previous final layer
        self.cleanData()

        if not error:

            # create final layer
            layerTreeWidget = self.masterWindow.getTnTLayerTreeWidget()
            root = layerTreeWidget.layerTreeRoot()
            finalGroup = root.findGroup(self.workGroupName)
            self.createFinalLayer(group=finalGroup, vLayer=masterMostSegmentedLayer)

            finalGroup.setExpanded(True)
            finalGroup.setItemVisibilityChecked(False)
