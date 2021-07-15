# -*- coding: utf-8 -*-

"""
/***************************************************************************
TraiNminaTor_dialog_base
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


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TraiNminatorDialogBase(object):
    
    print("passe constructeur Ui_TraiNminatorDialogBase (file:Ui_TraiNminator_Dialog_Base.py)")
    
    def setupUi(self, TraiNminatorDialogBase):
        TraiNminatorDialogBase.setObjectName("TraiNminatorDialogBase")
        TraiNminatorDialogBase.resize(400, 300)
        self.button_box = QtWidgets.QDialogButtonBox(TraiNminatorDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        self.retranslateUi(TraiNminatorDialogBase)
        self.button_box.accepted.connect(TraiNminatorDialogBase.accept)
        self.button_box.rejected.connect(TraiNminatorDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(TraiNminatorDialogBase)

    def retranslateUi(self, TraiNminatorDialogBase):
        _translate = QtCore.QCoreApplication.translate
        TraiNminatorDialogBase.setWindowTitle(_translate("TraiNminatorDialogBase", "TraiNminaTor"))
