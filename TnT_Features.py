
from qgis.core  import (QgsVectorLayer, QgsSpatialIndex, QgsFeature, NULL, QgsVectorDataProvider)
from typing import List

class TnTFeatures:

    def __init__(self, feature:QgsFeature, layer:QgsVectorLayer) -> None:
        self.feature = feature
        self.layer = layer
        self.children = []
        self.parent = None
        

    def addChild(self, feature):
        if feature not in self.children:
            self.children.append(feature)

    def setParent(self, parent):
        self.parent = parent


    def changeAttribute(self, attrs):
        # Change attributes of the feature
        attributesBeforeChange = self.getAttributes()
        prov = self.layer.dataProvider()
        caps = prov.capabilities()
        if caps and QgsVectorDataProvider.ChangeAttributeValues:
            prov.changeAttributeValues({self.feature.id() : attrs})
        
        # Iterate on children
        key = list(attrs.keys())[1]
        for child in self.children:
            childAttributes = child.getAttributes()
            if childAttributes[key] == NULL or childAttributes[key] == attributesBeforeChange[key]:
                child.changeAttribute(attrs)

    
    def removeCurrentClass(self, attrs, classId):
        # Change attributes of the feature
        prov = self.layer.dataProvider()
        caps = prov.capabilities()
        if caps and QgsVectorDataProvider.ChangeAttributeValues:
            prov.changeAttributeValues({self.feature.id() : attrs})
        
        # Iterate on children
        key = list(attrs.keys())[1]
        for child in self.children:
            childAttributes = child.getAttributes()
            if childAttributes[key] == classId:
                child.removeCurrentClass(attrs, classId)


    def removeAll(self, attrs):
        prov = self.layer.dataProvider()
        caps = prov.capabilities()
        if caps and QgsVectorDataProvider.ChangeAttributeValues:
            prov.changeAttributeValues({self.feature.id() : attrs})
            for child in self.children:
                child.removeAll(attrs)


    def getAttributes(self):
        # return self.feature.attributes() doesn't work : it returns value at the beginning of the plugin...
        feature = self.layer.getFeature(self.feature.id())
        return feature.attributes()
            





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
                    f.setParent = feature


    def getFeature(self, feature):
        for f in self.features:
            if f.feature == feature:
                return f
        return None


        



class TnTFeaturesManager:

    def __init__(self, layers) -> None:
        self.layers = layers
        self.tntFeaturesLevel:List[TnTFeaturesLevel] = []
        self.createTnTFeaturesLevel()
        
    def createTnTFeaturesLevel(self):
        for layer in self.layers:
            self.tntFeaturesLevel.append(TnTFeaturesLevel.createTnTFeaturesLevel(layer))

        for i in range(1, len(self.tntFeaturesLevel)):
            tntFeaturesLevel_i = self.tntFeaturesLevel[i]
            tntFeaturesLevel_i1 = self.tntFeaturesLevel[i-1]
            tntFeaturesLevel_i1.searchChildren(tntFeaturesLevel_i)
        

    def getFeature(self, feature, layer):
        for i, l in enumerate(self.layers):
            if l == layer:
                return self.tntFeaturesLevel[i].getFeature(feature)
        return None

    def getTnTFeaturesLevel(self, layer):
        for i, l in enumerate(self.layers):
            if l.sourceName() == layer.sourceName():
                return self.tntFeaturesLevel[i]
