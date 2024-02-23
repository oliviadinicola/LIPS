import parselmouth.praat as praat
import os

# Define parameters
directory = "test_data/"
output_file_name = "output4.txt"
segment_file_name = "obstruents.txt"
labeled_tier_number = 2
lexical_tier_number = 1
band1_left_range = 0
band1_right_range = 400
band1_low_pass = 50
band2_left_range = 800
band2_right_range = 1500
band2_low_pass = 50
band3_left_range = 1200
band3_right_range = 2000
band3_low_pass = 50
band4_left_range = 2000
band4_right_range = 3500
band4_low_pass = 50
band5_left_range = 3500
band5_right_range = 5000
band5_low_pass = 50
band6_left_range = 5000
band6_right_range = 8000
band6_low_pass = 50
smooth_proportion = 0.10
f0_minimum = 100
offset = 0.050

path = os.path.join('/', directory, output_file_name)
if os.path.exists(path):
    os.remove(file_path)
# Run Praat script with parameters
praat.run_file("kingston_hnr.praat", directory, output_file_name, segment_file_name,
                 labeled_tier_number, lexical_tier_number,
                 band1_left_range, band1_right_range, band1_low_pass,
                 band2_left_range, band2_right_range, band2_low_pass,
                 band3_left_range, band3_right_range, band3_low_pass,
                 band4_left_range, band4_right_range, band4_low_pass,
                 band5_left_range, band5_right_range, band5_low_pass,
                 band6_left_range, band6_right_range, band6_low_pass,
                 smooth_proportion, f0_minimum, offset)
