import sys
from PyQt5 import QtWidgets, uic

from MainWindow import Ui_ListeBiere
from dialog import Ui_Dialog
import csv

class MainWindow(QtWidgets.QMainWindow, Ui_ListeBiere):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.liredonnees("sauvegarde.csv")

        self.dialog = QtWidgets.QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)

        self.dialog.ui.non.clicked.connect(self.non)
        self.dialog.ui.oui.clicked.connect(self.oui)

        #Clic sur bouton créer
        self.pushButton.clicked.connect(self.creer)
        #clic sur ligne tableau
        self.tableWidget.clicked.connect(self.clicligne)
        #double clic sur ligne tableau
        self.tableWidget.doubleClicked.connect(self.doubleclicligne)

    #sauvegarde des données en CSV
    def sauvecsv(self, fichiercsv):
        """Lit le QTableWidget et enregistre son contenu dans un fichier csv
        """
        with open(fichiercsv, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for row in range(0, self.tableWidget.rowCount()):
                ligne = []
                for col in range(0, self.tableWidget.columnCount()):
                    valeurcase = self.tableWidget.item(row, col).text().strip()
                    ligne.append(valeurcase)
                csvwriter.writerow(ligne)

    def liredonnees(self, fichiercsv):
        with open(fichiercsv, "r") as fileInput:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(3)
            for rowdata in csv.reader(fileInput, delimiter=';'):
                row =  self.tableWidget.rowCount()

                self.tableWidget.insertRow(row)
                self.tableWidget.setColumnCount(len(rowdata))
                for column, data in enumerate(rowdata):
                    item = QtWidgets.QTableWidgetItem(data)
                    self.tableWidget.setItem(row, column, item)

    #ouverture de la boite de dialogue
    def doubleclicligne(self):
         self.dialog.exec_()

    #si non
    def non(self):
         self.dialog.hide()

    #si oui suppression ligne
    def oui(self):
        index = self.tableWidget.currentIndex()
        self.tableWidget.removeRow(index.row())
        self.pushButton.setText("Créer")
        self.nom.setText("")
        self.variete.setText("")
        self.degre.setText("")
        self.dialog.hide()
        self.sauvecsv("sauvegarde.csv")

    #Creer nouvelle entrée dans le tableau ou modifier une entrée
    def creer(self):
        if self.nom.text() != "" and self.variete.text() != "" and self.degre.text() != "" and self.check_string_to_float(self.degre.text()):
            if self.pushButton.text() == "Créer":
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(self.nom.text()))
                self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(self.variete.text()))
                self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(self.degre.text()))

            else:
                index = self.tableWidget.currentIndex()
                item = self.tableWidget.item(index.row(), 0)
                item.setText(self.nom.text())
                item = self.tableWidget.item(index.row(), 1)
                item.setText(self.variete.text())
                item = self.tableWidget.item(index.row(), 2)
                item.setText(self.degre.text())
                self.pushButton.setText("Créer")

            self.nom.setText("")
            self.variete.setText("")
            self.degre.setText("")
            self.sauvecsv("sauvegarde.csv")

    #ligne a modifier dans formulaire
    def clicligne(self):
        self.pushButton.setText("Modifier")

        index = self.tableWidget.currentIndex()

        NewIndex = self.tableWidget.model().index(index.row(), 0)
        self.nom.setText(self.tableWidget.model().data(NewIndex))

        NewIndex = self.tableWidget.model().index(index.row(), 1)
        self.variete.setText(self.tableWidget.model().data(NewIndex))

        NewIndex = self.tableWidget.model().index(index.row(), 2)
        self.degre.setText(self.tableWidget.model().data(NewIndex))

    #Vérifier si valeur est en float
    def check_string_to_float(self, s):
        try:
            float(s)
            return True
        except:
            return False

#Lancement application
app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
