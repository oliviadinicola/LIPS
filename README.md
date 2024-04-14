# Lenition Integrated Python System (LIPS)

## Description
LIPS is a unified Python-based graphical user interface (GUI) to streamline the measurement of lenition, a linguistic phenomenon involving the weakening of a consonant production. Traditionally, various lenition algorithms like Harmonic-to-Noise Ratio (HNR) are applied separately to audio data using various Praat and Python scripts, resulting in a tedious, inefficient, and irreproducible process. Our solution integrates these algorithms seamlessly within a single GUI, eliminating the need for researchers to have technical command-line expertise. This user-friendly interface empowers researchers to effortlessly run multiple algorithms, offering a more efficient alternative to the current approach.

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

add: they must upload phon file outside of ui folder -- must be same name just edit it
