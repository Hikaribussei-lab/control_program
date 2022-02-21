from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
ui_path = "mercury_ui_files"
dlg1 = uic.loadUi(f"{ui_path}/page1.ui")
dlg2 = uic.loadUi(f"{ui_path}/page2.ui")


def changeView():  # dlg1 -> dlg2に遷移させる
    dlg1.hide()    # dlg1 を hide
    dlg2.show()    # dlg2 を show


dlg1.pushButton.clicked.connect(changeView)

if __name__ == "__main__":
    dlg1.show()
    app.exec()