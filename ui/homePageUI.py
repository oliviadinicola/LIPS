# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homePageUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import shutil

from PyQt5 import QtWidgets, uic, Qt
import os
from PyQt5.QtCore import Qt

from ui.HnrKingstonUI import Ui_HnrKingstonPage
from ui.InferencingUI import Ui_InferencingPage
from ui.loadFilesUI import Ui_loadFilesPage


class Ui_loadHomePage(QtWidgets.QMainWindow):
    def setupUi(self):
        uic.loadUi('homePageUI.ui', self)
        self.show()
        self.loadFilesButton.clicked.connect(self.openLoadFilesWindow)
        self.openHNRPageButton.clicked.connect(self.openHnrKingstonWindow)
        self.openInferencingPageButton.clicked.connect(self.openInferencingWindow)
        self.errorMessageLabelHNR.setStyleSheet("color: red; font-size: 14px;")
        self.errorMessageLabelInferencing.setStyleSheet("color: red; font-size: 14px;")
        self.clearFilesButton.clicked.connect(self.clearFiles)

        if os.path.exists("uploaded_files/"):
            shutil.rmtree("uploaded_files/")

    def clearFiles(self):
        self.listOfFiles.clear()
        if os.path.exists("uploaded_files/"):
            shutil.rmtree("uploaded_files/")


    def openLoadFilesWindow(self):
        self.errorMessageLabelHNR.setText("")
        self.errorMessageLabelInferencing.setText("")
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_loadFilesPage()
        self.ui.setupUi()
        self.ui.filesSelected.connect(self.displaySelectedFiles)

    def openHnrKingstonWindow(self):
        if self.listOfFiles.count() >= 2:
            self.errorMessageLabelHNR.setText("")
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_HnrKingstonPage()
            self.ui.setupUi()
        else:
            self.errorMessageLabelHNR.setText("Please upload files before running algorithm!")

    def openInferencingWindow(self):
        if self.listOfFiles.count() >= 2:
            self.errorMessageLabelInferencing.setText("")
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_InferencingPage()
            self.ui.setupUi()
        else:
            self.errorMessageLabelInferencing.setText("Please upload files before running algorithm!")


    def displaySelectedFiles(self, files):
        self.output_directory = "uploaded_files"  # Define the output directory

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)

        for file_path in files:
            # Define the output file path in the output directory
            output_file_path = os.path.join(self.output_directory, os.path.basename(file_path))

            # Copy the uploaded file to the output directory
            try:
                shutil.copy(file_path, output_file_path)
            except Exception as e:
                print(f"Error saving file: {e}")

        for file_path in files:
            if not self.item_exists(file_path):
                self.listOfFiles.addItem(file_path)

    def item_exists(self, item_text):
        items = self.listOfFiles.findItems(item_text, Qt.MatchExactly)
        return bool(items)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HomePage = QtWidgets.QMainWindow()
    ui = Ui_loadHomePage()
    ui.setupUi()
    sys.exit(app.exec_())
