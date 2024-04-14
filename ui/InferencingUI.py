# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InferencingUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import json
import os
import re
import shutil
import subprocess
import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt


class Ui_InferencingPage(QtWidgets.QMainWindow):
    def setupUi(self):
        uic.loadUi('InferencingUI.ui', self)
        self.uploadPhonetFilesButton.clicked.connect(self.openFolderDialog)
        self.uploadFeatureChartButton.clicked.connect(self.openPhonological)
        self.runAlgoButton.clicked.connect(self.runAlgo)
        self.cancelButton.clicked.connect(self.handleCancel)
        self.saveParametersButton_2.clicked.connect(self.saveParams)
        self.loadParametersButton_2.clicked.connect(self.loadParams)
        self.enableRunButton(False)
        self.show()

    def loadParams(self):
        # Get the file path selected by the user

        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")

        # Check if a file was selected
        if file_path:
            # Read the parameters from the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Extract the parameters from each line and populate the UI fields
                if len(lines) >= 3:
                    model = lines[0].strip()
                    phon_file = lines[1].strip()
                    selected_feats = [line.strip() for line in lines[2:]]

                    # Check if the model file exists
                    if not os.path.exists(model):
                        self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 16px;")
                        self.phonetFilePathLabel.setText("Model file not found.")
                        return

                    # Check if the phonological file exists
                    if not os.path.exists(phon_file):
                        self.phonologicalChartLabel.setStyleSheet("color: red; font-size: 16px;")
                        self.phonologicalChartLabel.setText("Phonological file not found.")
                        return

                    # Set values in the UI
                    self.phonetFilePathLabel.setStyleSheet("color: black; font-size: 16px;")
                    self.phonetFilePathLabel.setText(model)
                    self.phonologicalChartLabel.setStyleSheet("color: black; font-size: 16px;")
                    self.phonologicalChartLabel.setText(phon_file)
                    dictionary_str, dict_keys = self.extract_dictionary_keys(phon_file)

                    if dictionary_str and dict_keys:
                        self.listOfPhonologicalFeatures.clear()
                        for key in dict_keys:
                            self.listOfPhonologicalFeatures.addItem(key)
                        self.listOfPhonologicalFeatures.show()
                        self.select_items(selected_feats)

                    # Enable the run button if necessary
                    if model and phon_file and selected_feats:
                        self.enableRunButton(True)
                else:
                    QMessageBox.warning(self, "Error", "Invalid parameter file format.")

    def saveParams(self):
        model = self.phonetFilePathLabel.text()
        phon_file = self.phonologicalChartLabel.text()
        selected_feat = [item.text() for item in self.listOfPhonologicalFeatures.selectedItems()]

        current_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        file_path = "saved_parameters_inference/parameters_" + current_time + ".txt"
        with open(file_path, 'w') as file:
            file.write(model + "\n")
            file.write(phon_file + "\n")
            for feat in selected_feat:
                file.write(feat + "\n")
        self.saveParamsLabel_3.setText(f"Parameters saved to {file_path}")

    def enableRunButton(self, enable):
        self.runAlgoButton.setEnabled(enable)

    def openFolderDialog(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        # Check if the 'MT' directory exists inside the selected directory
        mt_directory_path = os.path.join(folderpath, 'MT')
        # Check if the 'phonemes' directory exists inside the selected directory
        phonemes_directory_path = os.path.join(folderpath, 'phonemes')

        # Error handling
        if not os.path.isdir(mt_directory_path):
            self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 16px;")
            self.phonetFilePathLabel.setText("No MT folder in uploaded directory. Please upload again.")
            self.enableRunButton(False)
        elif not os.path.isdir(phonemes_directory_path):
            self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 14px;")
            self.phonetFilePathLabel.setText("No phonemes folder in uploaded directory. Please upload again.")
            self.enableRunButton(False)
        else:
            # Check for required files in 'MT' directory
            mt_files = os.listdir(mt_directory_path)
            mt_extensions = {os.path.splitext(file)[1] for file in mt_files}
            mt_extensions_required = {'.npy', '.h5', '.hdf5', '.json'}

            # Check for required extensions in 'MT' directory
            if not mt_extensions_required.issubset(mt_extensions):
                self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 16px;")
                self.phonetFilePathLabel.setText("Missing required files in MT folder. Please upload again.")
                self.enableRunButton(False)
                return

            # Check for std.npy and mu.npy files in 'MT' directory
            if 'std.npy' not in mt_files or 'mu.npy' not in mt_files:
                self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 16px;")
                self.phonetFilePathLabel.setText("Missing required files in MT folder. Please upload again.")
                self.enableRunButton(False)
                return

            # Check for required files in 'phonemes' directory
            phonemes_files = os.listdir(phonemes_directory_path)
            phonemes_extensions = {os.path.splitext(file)[1] for file in phonemes_files}
            phonemes_extensions_required = {'.npy', '.h5', '.hdf5', '.json'}

            # Check for required extensions in 'phonemes' directory
            if not phonemes_extensions_required.issubset(phonemes_extensions):
                self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 14px;")
                self.phonetFilePathLabel.setText("Missing required files in phonemes folder. Please upload again.")
                self.enableRunButton(False)
                return

            # Check for std.npy and mu.npy files in 'phonemes' directory
            if 'std.npy' not in phonemes_files or 'mu.npy' not in phonemes_files:
                self.phonetFilePathLabel.setStyleSheet("color: red; font-size: 14px;")
                self.phonetFilePathLabel.setText("Missing required files in phonemes folder. Please upload again.")
                self.enableRunButton(False)
                return

            # If all checks pass, set folder path
            self.phonetFilePathLabel.setStyleSheet("color: black; font-size: 16px;")
            self.phonetFilePathLabel.setText(folderpath)
            if self.phonologicalChartLabel.text() != "File must contain a valid dictionary. Please upload again.":
                self.enableRunButton(True)

    def openPhonological(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "*.py")
        try:
            dictionary_str, dict_keys = self.extract_dictionary_keys(fname[0])

            if dictionary_str and dict_keys:
                self.phonologicalChartLabel.setStyleSheet("color: black; font-size: 16px;")
                self.phonologicalChartLabel.setText(fname[0])
                self.listOfPhonologicalFeatures.clear()
                for key in dict_keys:
                    self.listOfPhonologicalFeatures.addItem(key)
                self.listOfPhonologicalFeatures.show()
                self.select_items(["sonorant", "continuant"])
                if "Please upload again" not in self.phonetFilePathLabel.text():
                    self.enableRunButton(True)
            # Error handling
            else:
                self.phonologicalChartLabel.setStyleSheet("color: red; font-size: 16px;")
                self.phonologicalChartLabel.setText("File must contain a valid dictionary. Please upload again.")
                self.listOfPhonologicalFeatures.clear()
                self.enableRunButton(False)
        # Error handling
        except Exception as e:
            self.phonologicalChartLabel.setStyleSheet("color: red; font-size: 16px;")
            self.phonologicalChartLabel.setText("File must contain a valid dictionary. Please upload again.")
            self.listOfPhonologicalFeatures.clear()
            self.enableRunButton(False)

    def select_items(self, items_to_select):
        for item_text in items_to_select:
            items = self.listOfPhonologicalFeatures.findItems(item_text, Qt.MatchExactly)
            if items:
                item = items[0]
                item.setSelected(True)

    def extract_dictionary_keys(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Use regex to find the dictionary definition
        pattern = r"\{([^}]*)\}"
        match = re.search(pattern, code)
        if match:
            dictionary_str = match.group(0)
            # Extract keys from the dictionary string
            keys = re.findall(r'\'([^\']*)\'', dictionary_str)
            return dictionary_str, keys
        else:
            return []


    def runAlgo(self):
        # Output directory
        directory_output = 'posterior_probs/'
        os.makedirs(directory_output, exist_ok=True)
        selected_phon_feat = [self.listOfPhonologicalFeatures.item(i).text()
                              for i in range(self.listOfPhonologicalFeatures.count())
                              if self.listOfPhonologicalFeatures.item(i).isSelected()]
        selected_phonological_feat_str = json.dumps(selected_phon_feat)

        # Get entire phonological.py file to pass as dict
        phonological_file_name = self.phonologicalChartLabel.text()
        directory = 'uploaded_files/'
        os.makedirs(directory, exist_ok=True)

        # Define the output file path in the output directory
        output_file_path = os.path.join(directory, os.path.basename(phonological_file_name))

        # Copy the uploaded file to the output directory
        try:
            shutil.copy(phonological_file_name, output_file_path)
        except Exception as e:
            print(f"Error saving file: {e}")

        # Rename the phonological file
        new_path = directory + "Phonological.py"
        shutil.move(output_file_path, new_path)

        phonological = self.phonologicalChartLabel.text()
        dict, _ = self.extract_dictionary_keys(phonological)

        # Define the command to run the other Python script
        command = ["python", "inferencing.py", self.phonetFilePathLabel.text(), self.phonologicalChartLabel.text(),
                   selected_phonological_feat_str, dict, 'uploaded_files/']

        # Show progress dialog indicating the algorithm is running
        progress_dialog = QProgressDialog("Running Algorithm...", None, 0, 0, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowTitle("Algorithm is running. This may take a few minutes.")
        progress_dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        progress_dialog.resize(400,50)

        progress_dialog.show()

        # Run the command
        subprocess.run(command)

        # Close the progress dialog after completion
        progress_dialog.close()

        # Show dialog box indicating completion
        QMessageBox.information(self, "Algorithm Completed", "The algorithm is done. Output is saved to the output/ folder.")

        self.close()

    def handleCancel(self):
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loadFilesPage = QtWidgets.QMainWindow()
    ui = Ui_InferencingPage()
    ui.setupUi()
    sys.exit(app.exec_())