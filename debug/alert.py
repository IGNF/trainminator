from qgis.PyQt.QtWidgets import QMessageBox


def show_alert_box(title, message, icon=QMessageBox.Information):
    """
    Affiche une boîte d'alerte avec un titre, un message et une icône dans QGIS.

    Parameters
    ----------
    title : str
        Le titre de la boîte d'alerte.
    message : str
        Le message à afficher dans la boîte d'alerte.
    icon : QMessageBox.Icon, optionnel
        L'icône à afficher dans la boîte d'alerte. La valeur par défaut est QMessageBox.Information.
        D'autres options incluent QMessageBox.Warning, QMessageBox.Error, QMessageBox.Question.

    Returns
    -------
    None
    """
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
