# Lenition Integrated Python System (LIPS)

## Description
LIPS is a unified Python-based graphical user interface (GUI) to streamline the measurement of lenition, a linguistic phenomenon involving the weakening of a consonant production. Traditionally, various lenition algorithms like Harmonic-to-Noise Ratio (HNR) are applied separately to audio data using various Praat and Python scripts, resulting in a tedious, inefficient, and irreproducible process. Our solution integrates these algorithms seamlessly within a single GUI, eliminating the need for researchers to have technical command-line expertise. This user-friendly interface empowers researchers to effortlessly run Kingston/HNR metrics and the inferencing algorithm on data, offering a more efficient alternative to the current approach.

## About the Algorithms


## Installation
Either clone the [git](https://git-scm.com/) repository:

`git clone https://github.com/oliviadinicola/LIPS.git`

Or download a zip archive.

### Requirements
See `requirements.txt` for the full list of requirements. The best way to install these requirements is using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing) and a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (like [venv](https://docs.python.org/3/library/venv.html)).

*Make sure to substitute <name_of_vev> with an actual name of your environment.*

    python3 -m venv <name_of_venv>
    source <name_of_venv>/bin/activate
    pip install -r requirements.txt`

## Project Structure & Software Implementation
All source code can be found in the `ui/` folder. The GUI is run using Python scripts with Python 3.8.3.

Download [Pycharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows) and open the location of this cloned repository in it. From here, you can run the `ui/homePageUI.py` file to start the GUI!

*Please note: if you are wanting to run the inferencing algorithm, make sure you name your phonological features file `step2_Phonological_revised.py` as seen in the example file provided in `LIPS/`. We recommend you edit or make a copy of this existing file to suit your phonological features.*

### `ui/` Folder Structure
* `output/`: where the results from the Kingston/HNR and inferencing algorithm will be saved to
* `saved_parameters_hnr/`: where any parameters are saved from the user clicked the "Save Parameters" button on the Kingston/HNR algorithm page
* `saved_parameters_inference/`: where any parameters are saved from the user clicked the "Save Parameters" button on the Inferencing algorithm page

### `test_data/` Folder
This folder contains sample test data for you to experiment with. However, you can use your own data as well that is saved in any location on your computer.

### `example_gujarati_model/` Folder
This contains an example model trained through Phonet on the Gujarati language to use for the inferencing algorithm. You can use any Phonet model that you have previously trained. However, as seen with this example model, ensure the directory contains both an `MT/` directory and `phonemes/` directory.
