import parselmouth.praat as praat
import os

# Define parameters
directory = "test_data/"
output_file_name = "output2.txt"
segment_file_name = "obstruents.txt"
labeled_tier_number = 2
lexical_tier_number = 1
band1_left_range = 0
band1_right_range = 400
band1_low_pass = 50
smooth_proportion = 0.10
f0_minimum = 100
offset = 0.050

path = os.path.join('/', directory, output_file_name)
if os.path.exists(path):
    os.remove(file_path)

# Run Praat script with parameters
praat.run_file("lenition_2nd_1_KTOneBand.praat", directory, output_file_name, segment_file_name,
                 labeled_tier_number, lexical_tier_number,
                 band1_left_range, band1_right_range, band1_low_pass,
                 smooth_proportion, f0_minimum, offset)
