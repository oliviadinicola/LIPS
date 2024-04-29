# Lenition Integrated Python System (LIPS)

## Description
LIPS is a unified Python-based graphical user interface (GUI) to streamline the measurement of lenition, a linguistic phenomenon involving the weakening of a consonant production. Traditionally, various lenition algorithms like Harmonic-to-Noise Ratio (HNR) are applied separately to audio data using various Praat and Python scripts, resulting in a tedious, inefficient, and irreproducible process. Our solution integrates lenition algorithms seamlessly within a single GUI, eliminating the need for researchers to have technical command-line expertise. This user-friendly interface empowers researchers to effortlessly run Kingston/HNR metrics and the inferencing algorithm on audio & TextGrid data, offering a more efficient alternative to the current approach.

### About the Algorithms
#### Kingston/HNR
This algorithm is adapted from [Christian DiCanio's lenition algorithm](https://www.acsu.buffalo.edu/~cdicanio/scripts/Kingston_lenition_2.praat). It calculates HNR, a measure that quantifies the level of additional noise present in the vocal signal. Essentially, the more lenited a segment, the more vowel-like it is, meaning a higher HNR. It also calculates measures used by John Kingston in his [paper](http://www.lingref.com/cpp/lasp/3/paper1711.pdf): intensity difference, mean intensity, and relative duration. The algorithm used in this toolkit can be found at `ui/lenition_2nd_1_KTOneBand.praat`.

#### Inferencing
This algorithm is used for the inferencing process after training a [Phonet](https://github.com/jcvasquezc/phonet) model. You will use the output Phonet model and corresponding phonological feature file as input to this algorithm (more information below). The algorithm used in this tookit can be found at `ui/inferencing.py`.

## Installation
Either clone the [git](https://git-scm.com/) repository:

`git clone https://github.com/oliviadinicola/LIPS.git`

Or [download a zip archive](https://github.com/oliviadinicola/LIPS/archive/refs/heads/main.zip).

### Requirements
See `requirements.txt` for the full list of requirements. The best way to install these requirements is using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing) and a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (like [venv](https://docs.python.org/3/library/venv.html)).

*Make sure to substitute <name_of_vev> with an actual name of your environment.*

    python3 -m venv <name_of_venv>
    source <name_of_venv>/bin/activate
    pip install -r requirements.txt

## Project Structure & Software Implementation
All source code can be found in the `ui/` folder. The GUI is run using Python scripts with Python 3.8.3.

Run `python homePageUI.py` from the command line to start the GUI!

*Please note: if you are wanting to run the inferencing algorithm, make sure you name your phonological features file `step2_Phonological_revised.py` as seen in the example file provided in `LIPS/`. We recommend you edit or make a copy of this existing file to suit your phonological features.*

### `ui/` Folder Structure
* `output/`: where the results from the Kingston/HNR and inferencing algorithm will be saved to
* `saved_parameters_hnr/`: where any parameters are saved from the user clicking the "Save Parameters" button on the Kingston/HNR algorithm page. We provide you with a `default.txt` file with some example parameters you can use
* `saved_parameters_inference/`: where any parameters are saved from the user clicking the "Save Parameters" button on the Inferencing algorithm page
* `homePageUI.ui`: contains the UI design for the home page
* `homePageUI.py`: contains the Python code for the home page features
* `loadFilesUI.ui`: contains the UI design for the load files page
* `loadFilesUI.py`: contains the Python code for the load files page
* `HnrKingstonUI.ui`: contains the UI design for the HNR/Kingston algorithm page
* `HnrKingstonUI.py`: contains the Python code for the HNR/Kingston algorithm page
* `InferencingUI.ui`: contains the UI design for the inferencing algorithm page
* `InferencingUI.py`: contains the Python code for the inferencing algorithm page

### `test_data/` Folder
This folder contains sample test data for you to experiment with. However, you can use your own data as well that is saved in any location on your computer as long as the audio files have a `.wav` extension and textgrids have a `.TextGrid` extension. All textgrids must have only 2 tiers: a 'lexical' (word) tier and a 'labeled' (phone) tier.

This folder also contains an example segment file that is used in the Kingston/HNR algorithm: `segment_example.txt`. Ensure that the segment file you upload for this algorithm has each segment on a new line as demonstrated in this example file.

### `example_gujarati_model/` Folder
This contains an example model trained through Phonet on the Gujarati language to use for the inferencing algorithm. You can use any Phonet model that you have previously trained. However, as seen with this example model, ensure the directory contains both an `MT/` directory and `phonemes/` directory.

## LIPS Interface
**homePageUI:**
![image](https://github.com/oliviadinicola/LIPS/assets/67873975/440fc9be-332a-4546-9c33-0e0f95a453ba)

**loadFilesUI:**
![image](https://github.com/oliviadinicola/LIPS/assets/67873975/c83a04b4-4ff3-4984-9e46-063c9635c2ce)

**HnrKingstonUI:**
![image](https://github.com/oliviadinicola/LIPS/assets/67873975/2c003032-1d84-4aba-9532-acf1211cf3bd)

**InferencingUI:**
![image](https://github.com/oliviadinicola/LIPS/assets/67873975/1c9f78b7-f448-4adb-823c-2afe5491e392)

*For more detailed information, you can view our full [documentation.](https://docs.google.com/document/d/1cFr7PB7lrnbY9Zepxrv1xTbbsnFbnMIAqTUB4PqhXvY/edit?usp=sharing)*
