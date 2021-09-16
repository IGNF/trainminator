# -*- coding: utf-8 -*-/
"""
/***************************************************************************
TnT_StatTools
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

from datetime import datetime

from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import ( QMainWindow, QVBoxLayout, QHBoxLayout,
                              QSizePolicy ,QGroupBox, QSpacerItem,
                              QPushButton, QWidget, QComboBox,
                              QLabel, QFileDialog )

from qgis.core import (QgsProject,QgsFeatureRequest,QgsExpression)

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')


def lineno():
    """Returns the current line number in Python source code"""
    return inspect.currentframe().f_back.f_lineno

def flocals():
    """Returns the local namespace seen by this frame"""
    return inspect.currentframe().f_back.f_locals

class TnTMplCanvas(FigureCanvasQTAgg):
    """
    Graph generation class.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(TnTMplCanvas, self).__init__(fig)

    def generateChartTimeStamp(self, typeChart):
        """
            :param typeChart:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTMplCanvas->generateChartTimeStamp(typeChart:{typeChart})")
        result = datetime.now().strftime('This '+typeChart+' was generated on %Y-%m-%d at %H:%M')
        return result

    def setTitle(self, title):
        """
            :param title:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTMplCanvas->setTitle(titleLable:{title})")
        self.axes.set_title(label=title,
                            fontdict={'fontsize':8,
                                      'fontweight':'bold'},
                            loc='center')

    def setFooter(self,typeChart):
        """
            :param typeChart:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTMplCanvas->setFooter(typeChart:{typeChart})")
        xlabel=self.generateChartTimeStamp(typeChart)
        self.axes.set_xlabel(xlabel,
                             fontdict={'fontsize':6,
                             'fontstyle':'oblique'})

    def drawBarChart(self, labels , sizes, colors):
        """
            :param  labels:
            :param sizes:
            :param  colors:
            :returns none:
        """
       # print(f"line:{self.lineno()}, TnTMplCanvas->drawBarChart()")

        self.axes.set_xticklabels(labels, fontsize=8, rotation=45)
        self.axes.bar(labels,
                      sizes,
                      color=colors,
                      align='center')
        for i in range(len(sizes)):
            self.axes.annotate(str(sizes[i])+"%",
                               xy=(labels[i],sizes[i]),
                               ha='center',
                               va='bottom',
                               rotation=30,
                               fontsize=6)

    def drawPieChart(self,  labels , sizes, colors, explode, nomenclatureName):
        """
            :param none:
            :param labels:
            :param sizes:
            :param colors:
            :param explode:
            :param nomenclatureName:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTMplCanvas->drawPieChart()")
        wedges,texts=self.axes.pie(sizes,
                                   explode=explode,
                                   labels=labels,
                                   colors=colors,
                                   shadow=True,
                                   startangle=157.5,
                                   textprops={'fontsize':8})

        self.axes.legend(wedges,
                         sizes,
                         title="Nomenclature: "+nomenclatureName+"\nOccupancy rate (%)",
                         title_fontsize=8,
                         loc='center left',
                         bbox_to_anchor=(1, 0, 0.5, 1),
                         fontsize=8)

class TnTstatTools(QMainWindow):
    """
    Graph generation class.
    """
    def __init__(self, parent=None):
        super(TnTstatTools, self).__init__(parent)
        self.windowParent=parent
        self.centralwidget=None
        self.chart=None
        #Data 4 Chart
        self.labels=[]
        self.sizes=[]
        self.colors=[]
        self.explode=[]

        self.workGroupName='FINAL_DATA'
        self.workGroup=self.getRootGroup().findGroup(self.workGroupName)

        self.dictFinalLayers={}
        self.dictClasses={}

        self.setUpUi()
        self.init()

    def getRootGroup(self):
        """
            :param none:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->getRootGroup()")
        return self.windowParent.getRootGroup()

    def init(self):
        """
            :param none:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->init()")
        self.dumpIntoDict(self.windowParent.nomenclatureWidget.nomenclatureTree, self.dictClasses)
        self.getLayers()

        list_ComboBox=self.centralwidget.findChildren(QComboBox)
        defaultCharType=list_ComboBox[0].currentText()

        self.generateChart(defaultCharType)

    def setUpUi(self):
        """
            :param none:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->setUpUi()")
        self.resize(500, 750)
        self.centralwidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        QVBoxLayout(self.centralwidget)

        #Top group box
        top_GroupBox  = QGroupBox(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        top_GroupBox.setSizePolicy(sizePolicy)
        QHBoxLayout(top_GroupBox)

        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        graphType_QLabel = QLabel("Generate as:")
        graphType_QLabel.setSizePolicy(sizePolicy)
        top_GroupBox.layout().addWidget(graphType_QLabel)

        graphType_QComboBox = QComboBox(top_GroupBox)
        graphType_QComboBox.addItems( ('Bar chart','Pie chart') )
        graphType_QComboBox.setSizePolicy(sizePolicy)
        top_GroupBox.layout().addWidget(graphType_QComboBox)

        graphType_QComboBox.currentTextChanged.connect(self.generateChart)

        export_PushButton = QPushButton("Export As...", top_GroupBox)
        export_PushButton.setSizePolicy(sizePolicy)
        top_GroupBox.layout().addWidget(export_PushButton)

        export_PushButton.clicked.connect(self.exportAsImage)

        top_GroupBox_SpacerItem  = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_GroupBox.layout().addItem(top_GroupBox_SpacerItem)

        layer_ComboBoxLabel= QLabel(self)
        layer_ComboBoxLabel.setText("Final Selected Layer:")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        layer_ComboBoxLabel.setSizePolicy(sizePolicy)
        top_GroupBox.layout().addWidget(layer_ComboBoxLabel)

        layer_ComboBox= QComboBox(self)
        top_GroupBox.layout().addWidget(layer_ComboBox)
        self.centralwidget.layout().addWidget(top_GroupBox)
        #End group box

        #Principal group box
        principal_GroupBox   = QGroupBox(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        principal_GroupBox.setSizePolicy(sizePolicy)
        QHBoxLayout(principal_GroupBox)

        self.chart=TnTMplCanvas(self, width=4, height=5, dpi=100)
        self.chart.setSizePolicy(sizePolicy)
        principal_GroupBox.layout().addWidget(self.chart)

        self.centralwidget.layout().addWidget(principal_GroupBox)
        #Principal group box

        self.setCentralWidget(self.centralwidget)
        self.show()

    def getLayers(self):
        """
            :param none:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->getLayers()")
        group=QgsProject.instance().layerTreeRoot().findGroup(self.workGroupName)

        #Search comboBox widget (there is only one)
        list_ComboBox=self.centralwidget.findChildren(QComboBox)
        tLayers=group.findLayers()

        self.dictFinalLayers.clear()
        #list_ComboBox[0].clear()

        if len(tLayers)==0:
            self.dictFinalLayers["No layers"]=None
            list_ComboBox[1].addItem("No layers")
        else :
            for tLayer in tLayers:
                tLayerName=tLayer.name()
                self.dictFinalLayers[tLayerName]=tLayer
                list_ComboBox[1].addItem(tLayerName)

    def dumpIntoDict(self, treeWidget, dictClasses):
        """
            :param treeWidget:
            :param dictClasses:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->dumpIntoDict(treeWidget:{treeWidget},dictClasses:{dictClasses} )")
        nbColumns=treeWidget.headerItem().columnCount()
        items = treeWidget.findItems( "*", Qt.MatchWrap | Qt.MatchWildcard )
        for item in items :
            dictClasses[item.text(0)]=[]
            for i in range(nbColumns-1):
                dictClasses[item.text(0)].append(item.text(i+1))

    def generateDemoDataSet(self):
        """
            :param none:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->generateDemoDataSet()")
        labels=['class1', 'class2', 'Class3', 'EXPLODE']
        sizes=[35, 40, 20, 5]
        colors=['#3399FF', '#797979', '#00FF80','#FF5A00']
        explode =[0, 0, 0, 0.2]
        return labels, sizes, colors, explode

    def generateDataSet(self, vlayer, fieldName, dictItems):
        """
            :param vlayer:
            :param fieldName:
            :param dictItems:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->generateDataSet(vlayer:{vlayer},fieldName:{fieldName},dictItems:{dictItems})")
        Safety_orange='#FF5A00'
        totalLayerArea =vlayer.extent().area()
        labels=[]
        sizes=[]
        colors=[]
        explode=[]

        for key in dictItems :
            expr = QgsExpression( "\""+fieldName+"\"='"+key+"'" )
            selected_features = vlayer.getFeatures(QgsFeatureRequest(expr))
            area=0
            for feature in selected_features:
                area+=feature.geometry().area()
            if area!=0 :
                areaPercent=(area/totalLayerArea)*100
                if 0<areaPercent<1:
                    sizes.append(1)
                else:
                    sizes.append(round(areaPercent,1))

                labels.append(key)
                colors.append(dictItems[key][1])
                explode.append(0)

        # Finish with Not labeled data
        expr = QgsExpression( "\""+fieldName+"\"IS NULL" )
        selected_features = vlayer.getFeatures(QgsFeatureRequest(expr))
        area=0
        for feature in selected_features:
            area+=feature.geometry().area()
        if area!=0 :
            areaPercent=(area/totalLayerArea)*100
            if 0<areaPercent<1:
                sizes.append(1)
            else:
                sizes.append(round(areaPercent,1))

            labels.append('No label')
            colors.append(Safety_orange)
            explode.append(0.2)

        return labels, sizes, colors, explode

    def generateChart(self, chartType):
        """
            :param chartType:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->generateChart(chartType:{chartType})")

        list_ComboBox=self.centralwidget.findChildren(QComboBox)
        vlayer_name=list_ComboBox[1].currentText()
        vlayer=None
        try :
            vlayer=self.dictFinalLayers[vlayer_name]
        except KeyError:
            pass

        titleLable="Project: "+QgsProject.instance().baseName()
        nomenclatureName=self.windowParent.nomenclatureWidget.getCurrentNomenclatureName()

        self.chart.figure.clear()
        self.chart.axes = self.chart.figure.add_subplot(111)

        if vlayer :
            self.chart.setTitle(titleLable)
            self.labels, self.sizes, self.colors, self.explode=self.generateDataSet(vlayer.layer(),
                                                                                    "code",
                                                                                    self.dictClasses)
            titleLable="Project: "+QgsProject.instance().baseName()
            nomenclatureName=self.windowParent.nomenclatureWidget.getCurrentNomenclatureName()

        else :
            self.chart.setTitle('demo')
            self.labels, self.sizes, self.colors, self.explode= self.generateDemoDataSet()

        if chartType=="Bar chart":
            self.chart.drawBarChart(self.labels, self.sizes, self.colors)
        else :
            self.chart.drawPieChart(self.labels, self.sizes, self.colors, self.explode, nomenclatureName)

        self.chart.setFooter(chartType)
        self.chart.draw()

    def exportAsImage(self):
        """
        Executed when the user presses the "Export As" button.
            :param none:
            :returns none:
        """
        #print(f"line:{self.lineno()}, TnTstatTools->exportAsImage()")
        where=QgsProject.instance().absolutePath()
        filePath, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Image",
                                                  where,
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if filePath == "":
            return
        self.chart.figure.savefig(filePath)
