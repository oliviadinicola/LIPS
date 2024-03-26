# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HnrKingstonUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import shutil

from PyQt5 import QtWidgets, uic, QtCore
import os
from PyQt5.QtWidgets import QFileDialog


class Ui_HnrKingstonPage(QtWidgets.QMainWindow):
    def setupUi(self):
        uic.loadUi('HnrKingstonUI.ui', self)
        self.show()
        self.lexicalTierComboBox.addItems(["1", "2"])
        self.labeledTierComboBox.addItems(["1", "2"])
        self.uploadSegmentFileButton.clicked.connect(self.openSegmentDialog)
        self.runAlgoButton.clicked.connect(self.runScript)

    def openSegmentDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        self.segmentFileLabel.setText(fname[0])

    def runScript(self):
        # Get input values
        f0 = float(self.f0MinimumInput.text())
        time_offset = float(self.timeOffsetInput.text())
        smooth_proportion = float(self.smoothProportionInput.text())
        output_file_name = str(self.outputFileNameInput.text())
        freq_left_range = float(self.leftRangeInput.text())
        freq_right_range = float(self.rightRangeInput.text())
        freq_low_pass_filter = float(self.lowPassFilterInput.text())
        lexical_tier = self.lexicalTierComboBox.currentText()
        labeled_tier = self.labeledTierComboBox.currentText()
        directory = 'uploaded_files/'
        segment_file_name = self.segmentFileLabel.text()

        try:
            shutil.copy(segment_file_name)
        except Exception as e:
            print(f"Error saving file: {e}")

        # Run Praat script with parameters
        #praat.run_file("lenition_2nd_1_KTOneBand.praat", directory, output_file_name, segment_file_name,
                      # labeled_tier, lexical_tier,
                      # freq_left_range, freq_right_range, freq_low_pass_filter,
                      # smooth_proportion, f0, time_offset)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loadFilesPage = QtWidgets.QMainWindow()
    ui = Ui_HnrKingstonPage()
    ui.setupUi()
    sys.exit(app.exec_())
