# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HnrKingstonUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import shutil
import datetime

from PyQt5 import QtWidgets, uic, QtCore
import os

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QMessageBox
import parselmouth


class Ui_HnrKingstonPage(QtWidgets.QMainWindow):
    def setupUi(self):
        uic.loadUi('HnrKingstonUI.ui', self)
        self.show()
        self.lexicalTierComboBox.addItems(["1", "2"])
        self.labeledTierComboBox.addItems(["1", "2"])
        self.uploadSegmentFileButton.clicked.connect(self.openSegmentDialog)
        self.runAlgoButton.clicked.connect(self.runScript)
        self.cancelButton.clicked.connect(self.handleCancel)
        self.saveParametersButton.clicked.connect(self.saveParams)
        self.select_option("2")

    def saveParams(self):
        f0min = self.f0MinimumInput.text()
        timeOffset = self.timeOffsetInput.text()
        smoothProp = self.smoothProportionInput.text()
        outputFileName = self.outputFileNameInput.text()
        segmentFileName = self.segmentFileLabel.text()
        leftRange = self.leftRangeInput.text()
        rightRange = self.rightRangeInput.text()
        lowPassFilter = self.lowPassFilterInput.text()
        lexicalTier = self.lexicalTierComboBox.currentText()
        labeledTier = self.labeledTierComboBox.currentText()

        current_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        file_path = "saved_parameters_hnr/parameters_" + current_time + ".txt"
        with open(file_path, 'w') as file:
            file.write(f0min + "\n")
            file.write(timeOffset + "\n")
            file.write(smoothProp + "\n")
            file.write(outputFileName + "\n")
            file.write(segmentFileName + "\n")
            file.write(leftRange + "\n")
            file.write(rightRange + "\n")
            file.write(lowPassFilter+ "\n")
            file.write(lexicalTier + "\n")
            file.write(labeledTier + "\n")
        self.saveParamsLabel.setText(f"Parameters saved to {file_path}")


    def validateInputs(self):
        invalid_inputs = []

        validators = {
            self.f0MinimumInput: (QDoubleValidator(0, 500, 1000), "Integer/Decimal between 0 and 500"),
            self.timeOffsetInput: (QDoubleValidator(0, 1000, 1000), "Integer/Decimal between 0 and 1000"),
            self.smoothProportionInput: (QDoubleValidator(0, 1, 1000), "Integer/Decimal between 0 and 1"),
            self.outputFileNameInput: (QRegExpValidator(QRegExp("[^./\\:*?\"<>|]+")), "Valid file name"),
            self.leftRangeInput: (QDoubleValidator(0, 8000, 1000),"Integer/Decimal between 0 and 8000"),
            self.rightRangeInput: (QDoubleValidator(0, 8000, 1000),"Integer/Decimal between 0 and 8000"),
            self.lowPassFilterInput: (QDoubleValidator(0, 8000, 1000),"Integer/Decimal between 0 and 8000")
        }
        # Store references to input widgets in a list
        input_widgets = [self.f0MinimumInput, self.timeOffsetInput, self.smoothProportionInput, self.outputFileNameInput, self.leftRangeInput, self.rightRangeInput, self.lowPassFilterInput]


        for input_widget, (validator, valid_range) in validators.items():
            state, _, _ = validator.validate(input_widget.text(), 0)

            if state != validator.Acceptable:
                invalid_inputs.append(f"{input_widget.objectName()} ({valid_range})")

        if self.segmentFileLabel.text() == '':
            QMessageBox.warning(self, "Validation Result",
                                f"Please upload a segment file")
            return False

        lexicalTierValue = self.lexicalTierComboBox.currentText()
        labeledTierValue = self.labeledTierComboBox.currentText()

        if lexicalTierValue == labeledTierValue:
            QMessageBox.warning(self, "Validation Result", "Lexical and Labeled Tiers cannot have the same value")
            return False

        if invalid_inputs:
            QMessageBox.warning(self, "Validation Result",
                                f"Please enter valid inputs for: {', '.join(invalid_inputs)}.")
            return False
        else:
            return True

    def select_option(self, option_text):
        index = self.labeledTierComboBox.findText(option_text)
        if index != -1:
            self.labeledTierComboBox.setCurrentIndex(index)

    def openSegmentDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        self.segmentFileLabel.setText(fname[0])

    def handleCancel(self):
        self.close()

    def runScript(self):
        if self.validateInputs() == True:

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

            # self.output_directory = "uploaded_files"  # Define the output directory

            # Create the output directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)

            # Define the output file path in the output directory
            output_file_path = os.path.join(directory, os.path.basename(segment_file_name))

            # Copy the uploaded file to the output directory
            try:
                shutil.copy(segment_file_name, output_file_path)
            except Exception as e:
                print(f"Error saving file: {e}")

            # Generate a unique filename based on the current date and time
            current_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            output_file_name = f"{output_file_name}_{current_time}.txt"

            # Run Praat script with parameters
            parselmouth.praat.run_file("lenition_2nd_1_KTOneBand.praat", directory, output_file_name,
                                       os.path.basename(segment_file_name),
                                       labeled_tier, lexical_tier,
                                       freq_left_range, freq_right_range, freq_low_pass_filter,
                                       smooth_proportion, f0, time_offset)
            self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loadFilesPage = QtWidgets.QMainWindow()
    ui = Ui_HnrKingstonPage()
    ui.setupUi()
    sys.exit(app.exec_())
