from copy import deepcopy

from qgis.core  import (QgsVectorLayer, QgsSpatialIndex, QgsFeature, NULL, QgsVectorDataProvider, Qgis)
from typing import List
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.utils import iface


class TnTFeatures:

    def __init__(self, feature:QgsFeature, layer:QgsVectorLayer) -> None:
        self.feature = feature
        self.layer = layer
        self.children = []
        self.parent = None
        self.attrs = self.feature.attributes()
        

    def addChild(self, feature):
        if feature not in self.children:
            self.children.append(feature)

    def setParent(self, parent):
        self.parent = parent

    def changeAttrs(self, attrs):
        for k in attrs.keys():
            self.attrs[k]=attrs[k]

    def getChildren(self, patch_ok=False):
        """
        Return children of feature
        If it is the patch layer, return children only if patch_ok=True
        """
        if self.layer.name()=="patches":
            if patch_ok:
                return self.children
            return []
        return self.children

    def getParent(self, patch_ok=False):
        if self.parent is None:
            return None
        if self.parent.layer.name()=="patches":
            if patch_ok:
                return self.parent
            return None
        return self.parent


    def getLastLevelChildren(self):
        """
        Get all children of this feature in the most segmented layer
        """
        children = self.getChildren(patch_ok=True)
        if len(children) == 0:
            return [self]
        else:
            lastLevelChildrenList = []
            for child in children:
                for c in child.getLastLevelChildren():
                    lastLevelChildrenList.append(c)
            return lastLevelChildrenList


    def getCodeValue(self):
        """
        Return code values for all vintages
        """
        prov = self.layer.dataProvider()
        fieldNameMap = prov.fieldNameMap()
        codeValues = []
        for key in fieldNameMap.keys():
            if key[:5]=="code_":
                index = fieldNameMap[key]
                codeValues.append(self.getAttributes()[index])
        return codeValues
    
    
    def checkPatches(self, differentialMode):
        """
        Check that each children of last level of the patch are completed in differential mode
        """
        if self.layer.name()!="patches" or not differentialMode:
            return True, None
        
        lastLevelChildrenList = self.getLastLevelChildren()
        for child in lastLevelChildrenList:
            codeValues = child.getCodeValue()
            if (codeValues[0] == NULL and codeValues[1] != NULL) or (codeValues[0] != NULL and codeValues[1] == NULL):
                return False, child.feature
        return True, None


    def changeAttribute(self, attrs):
        """
        Change attributes of the feature
        """
        if self.layer.name()=="patches":
            key = list(attrs.keys())[0]
        else:
            key = list(attrs.keys())[1]
        attributesBeforeChange = self.getAttributes()[key]


        # Iterate on children
        labelsSet = set()
        
        for child in self.getChildren():
            childAttributes = child.getAttributes()
            if childAttributes[key] == NULL or childAttributes[key] == attributesBeforeChange:
                child.changeAttribute(attrs)
            
        labels = []
        for child in self.getChildren():
            childAttributes = child.getAttributes()
            labels.append(childAttributes[key])
        
        labelsSet = set(labels)
        

        # First case : no children (last segmentation level)
        if len(labelsSet)==0:
            prov = self.layer.dataProvider()
            caps = prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                prov.changeAttributeValues({self.feature.id() : attrs})
                self.changeAttrs(attrs)
        
        # Second case : exactly one label not null
        elif (len(labelsSet) == 1 and labels[0]!=NULL):
            prov = self.layer.dataProvider()
            caps = prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                prov.changeAttributeValues({self.feature.id() : attrs})
                self.changeAttrs(attrs)

        else:
            attrsNull = {}
            for k in attrs.keys():
                attrsNull[k]=None
            prov = self.layer.dataProvider()
            caps = prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                prov.changeAttributeValues({self.feature.id() : attrsNull})
                self.changeAttrs(attrsNull)

        return True, None

    
    def removeCurrentClass(self, attrs, classId):
        # Change attributes of the feature
        prov = self.layer.dataProvider()
        caps = prov.capabilities()
        if caps and QgsVectorDataProvider.ChangeAttributeValues:
            prov.changeAttributeValues({self.feature.id() : attrs})
            self.changeAttrs(attrs)
        
        # Iterate on children
        for child in self.getChildren():
            key = list(attrs.keys())[1]
            childAttributes = child.getAttributes()
            if str(childAttributes[key]) == classId:
                child.removeCurrentClass(attrs, classId)


    def removeAll(self, attrs):
        prov = self.layer.dataProvider()
        caps = prov.capabilities()
        if caps and QgsVectorDataProvider.ChangeAttributeValues:
            prov.changeAttributeValues({self.feature.id() : attrs})
            self.changeAttrs(attrs)
            for child in self.getChildren():
                child.removeAll(attrs)


    def getAttributes(self):
        return self.attrs


    def check(self, attrs, attrsNull):
        key = list(attrs.keys())[1]
        labels = []
        for child in self.getChildren():
            labels.append(child.getAttributes()[key])
        setLabels = set(labels)

        modif = False
        
        # first case:
        # at least two labels different and self.attributes is not null
        if len(setLabels) >= 2 and self.getAttributes()[key] != NULL:
            prov = self.layer.dataProvider()
            caps = prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                prov.changeAttributeValues({self.feature.id() : attrsNull})
                self.changeAttrs(attrsNull)
                modif = True
        
        # second case:
        # exactly one label and self.attributes different from the label
        elif len(setLabels) == 1 and self.getAttributes()[key] != labels[0]:
            prov = self.layer.dataProvider()
            caps = prov.capabilities()
            if caps and QgsVectorDataProvider.ChangeAttributeValues:
                if labels[0] == NULL:
                    prov.changeAttributeValues({self.feature.id() : attrsNull})
                    self.changeAttrs(attrsNull)
                else:
                    prov.changeAttributeValues({self.feature.id() : attrs})
                    self.changeAttrs(attrs)
                modif = True

        if modif and self.getParent() is not None:
            self.getParent().check(attrs, attrsNull)



class TnTFeaturesLevel:

    def __init__(self) -> None:
        self.features : List[TnTFeatures] = []
        self.index = QgsSpatialIndex()

    @staticmethod
    def createTnTFeaturesLevel(qgsVectorLayer:QgsVectorLayer):

        tntFeaturesLevel = TnTFeaturesLevel()
        for feature in qgsVectorLayer.getFeatures():
            tntFeaturesLevel.features.append(TnTFeatures(feature, qgsVectorLayer))
        
        tntFeaturesLevel.index.addFeatures(qgsVectorLayer.getFeatures())
        return tntFeaturesLevel


    def searchChildren(self, tntFeaturesLevel):
        """
        tntFeaturesLevel is more segmented than self
        """

        for feature in self.features:
            
            ids = tntFeaturesLevel.index.intersects(feature.feature.geometry().boundingBox())
            
            for id in ids:
                f = tntFeaturesLevel.features[id]
                if f.feature.geometry().within(feature.feature.geometry()):
                    feature.addChild(f)
                    f.setParent(feature)


    def getFeature(self, feature):
        for f in self.features:
            if f.feature == feature:
                return f
        return None






class TnTFeaturesManager:
    """Factory Class to manage Hierarchical Vector Layers with class `TnTFeatureLayers`

    """
    def __init__(self, layers) -> None:
        self.layers = layers
        self.tntFeaturesLevel:List[TnTFeaturesLevel] = []
        self.createTnTFeaturesLevel()
        
    def createTnTFeaturesLevel(self):
        progressMessageBar = iface.messageBar().createMessage("Loading...")
        progress = QProgressBar()
        progress.setMaximum(2*len(self.layers)-1)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
        compte = 0
        progress.setValue(compte)
        for layer in self.layers:
            self.tntFeaturesLevel.append(TnTFeaturesLevel.createTnTFeaturesLevel(layer))
            compte += 1
            progress.setValue(compte)

        for i in range(1, len(self.tntFeaturesLevel)):
            tntFeaturesLevel_i = self.tntFeaturesLevel[i]
            tntFeaturesLevel_i1 = self.tntFeaturesLevel[i-1]
            tntFeaturesLevel_i1.searchChildren(tntFeaturesLevel_i)
            compte += 1
            progress.setValue(compte)
        iface.messageBar().clearWidgets()
        

    def getFeature(self, feature, layer):
        for i, l in enumerate(self.layers):
            if l == layer:
                return self.tntFeaturesLevel[i].getFeature(feature)
        return None

    def getTnTFeaturesLevel(self, layer):
        for i, l in enumerate(self.layers):
            if l.sourceName() == layer.sourceName():
                return self.tntFeaturesLevel[i]
