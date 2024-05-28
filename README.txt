TrainMinator est un outil de labellisation développé en interne à l'IGN/DSI/(SDM et SIMV) par Yann Le Borgne, Célestin Huet et Apolline De Wit. Ces dévelopements ont été aidé par Lucas Martelet, Maxime Dardy, Samy Khelifi, Pascal Voitot et Nicolas Gonthier. 

Trainminator nécessite en entrée un projet QGis avec des contraintes spécifiques : images issues de la BDOrtho IGN accompagné des MNS ainsi que d'une segmentation hiérarchique. 
Celle-ci est réalisé à l'aide de Pyram, qui sert à faire la segmentation multi-échelle, est ouvert (https://github.com/IGNF/pyram_legacy?tab=readme-ov-file).

La documentation utilisateur est disponible dans le fichier TraiNminaTor Bidate Documentation.pdf et une très brève documentation développeur est disponible dans le fichier Documentation_developpeur.pdf.

----------------------

Plugin Builder Results

Your plugin TraiNminaTor2 was created in:
    C:/Users/YLe-Borgne/DEV/PROJECT-X/traiminator2\trainminator2

Your QGIS plugin directory is located at:
    C:/Users/YLe-Borgne/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

What's Next:

  * Copy the entire directory containing your new plugin to the QGIS plugin
    directory

  * Compile the resources file using pyrcc5

  * Run the tests (``make test``)

  * Test the plugin by enabling it in the QGIS plugin manager

  * Customize it by editing the implementation file: ``trainminator2.py``

  * Create your own custom icon, replacing the default icon.png

  * Modify your user interface by opening TraiNminaTor2_dialog_base.ui in Qt Designer

  * You can use the Makefile to compile your Ui and resource files when
    you make changes. This requires GNU make (gmake)

For more information, see the PyQGIS Developer Cookbook at:
http://www.qgis.org/pyqgis-cookbook/index.html

(C) 2011-2018 GeoApt LLC - geoapt.com
