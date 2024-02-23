# Filter in selected bands, estimate energy within each band, and calculate its rate of change.
# Copyright John Kingston 2020.

# Modified by Christian DiCanio 2020 to work with textgrid files of any name across a directory, to
# permit the script to work only on target segments (not all segments), and to include a number
# of additional intensity measures at several positions around the consonant target. Difference
# values are now included as well.
clearinfo

# Get the arguments passed from Python
form Band-pass filter and intensity tracking
    sentence directory
    sentence output_file_name
    sentence Segment_file_name
    positive Labeled_tier_number
    positive Lexical_tier_number
    real left_range_Band1
    real right_range_Band1
    positive Band1_low_pass
    real left_range_Band2
    real right_range_Band2
    positive Band2_low_pass
    real left_range_Band3
    real right_range_Band3
    positive Band3_low_pass
    real left_range_Band4
    real right_range_Band4
    positive Band4_low_pass
    real left_range_Band5
    real right_range_Band5
    positive Band5_low_pass
    real left_range_Band6
    real right_range_Band6
    positive Band6_low_pass
    real Smooth_proportion
    positive F0_minimum
    positive Offset
endform

#writeInfoLine: "F0 minimum duration ", f0_minimum

# calculate smoothing values in Hz

for j from 1 to 6
	smooth = round(right_range_Band'j' * 'smooth_proportion') 
	printline 'smooth'
	sm_'j' = smooth
endfor

# delete output file if it already exists

filedelete 'output_file_name$'

# make a header for the file
fileappend "'directory$''output_file_name$'" file'tab$'labelNumber'tab$'label'tab$'seg_bf'tab$'seg_aft'tab$'lex'tab$'seg_bf_dur'tab$'seg_bf_max_int'tab$'seg_aft_dur'tab$'seg_aft_max_int'tab$'seg_dur'tab$'seg_min_int'tab$'seg_mean_int'tab$'seg_mean_hnr'tab$'int_dif'tab$'dur_ratio'tab$'new_premin1'tab$'new_postmax1'tab$'t_new_premin1'tab$'t_new_postmax1'tab$'new_premin2'tab$'new_postmax2'tab$'t_new_premin2'tab$'t_new_postmax2'tab$'new_premin3'tab$'new_postmax3'tab$'t_new_premin3'tab$'t_new_postmax3'tab$'new_premin4'tab$'new_postmax4'tab$'t_new_premin4'tab$'t_new_postmax4'tab$'new_premin5'tab$'new_postmax5'tab$'t_new_premin5'tab$'t_new_postmax5'tab$'new_premin6'tab$'new_postmax6'tab$'t_new_premin6'tab$'t_new_postmax6'tab$''newline$'

# Make a list of file names and open wav files.
Create Strings as file list... list 'directory$'*.wav
number_files = Get number of strings
for ifile to number_files
	select Strings list
	current_file$ = Get string... ifile
	Read from file... 'directory$''current_file$'
	base_name$ = current_file$ - ".wav"
	sound0 = selected("Sound")
	
	select 'sound0'
	intensID = To Intensity: f0_minimum, 0, "no"

	select 'sound0'
	harmonicityID = To Harmonicity (cc): 0.01, 75, 0.1, 1.0
	

# Open the corresponding TextGrid file.
	Read from file... 'directory$''base_name$'.TextGrid
	textGridID = selected("TextGrid")
	num_labels = Get number of intervals... labeled_tier_number

# process each frequency band

	for j from 1 to 6
		select 'sound0'

# filter and get intensity differences
		Filter (pass Hann band)... left_range_Band'j' right_range_Band'j' sm_'j'
		To Intensity... 'f0_minimum' 0.001 yes
		Formula... (self[col+1]-self[col])/0.001

# dump results to a matrix and cast its contents to a Sound; then low pass filter to smooth.

		Down to Matrix
		To Sound (slice)... 1

		low_pass = band'j'_low_pass 
		roll_off = round('low_pass' * 0.1) 
		Filter (pass Hann band)... 0 'low_pass' 'roll_off'

# rename sound created by each band

		Rename... sound_'j'
	endfor

Read Strings from raw text file... 'directory$''segment_file_name$'
segments = selected("Strings")
lenseg = Get number of strings

# Get values near each labeled interval (within offsets)
for k to num_labels
	select 'textGridID'
	label$ = Get label of interval... labeled_tier_number k
	intvl_start = Get starting point... labeled_tier_number k
	intvl_end = Get end point... labeled_tier_number k
		for m to lenseg
			select 'segments'
				text$ [m] = Get string... m
				if label$ = text$ [m]
				select 'textGridID'
				segbf$ = do$ ("Get label of interval...", labeled_tier_number, (k-1))
				segbf_start = do ("Get starting point...", labeled_tier_number, (k-1))
				segbf_end = do ("Get end point...", labeled_tier_number, (k-1))
				segbf_dur = (segbf_end - segbf_start)*1000
				

				segaft$ = do$ ("Get label of interval...", labeled_tier_number, (k+1))
				segaft_start = do ("Get starting point...", labeled_tier_number, (k+1))
				segaft_end = do ("Get end point...", labeled_tier_number, (k+1))
				segaft_dur = (segaft_end - segaft_start)*1000

				lex_num = do ("Get interval at time...", lexical_tier_number, intvl_start)
				lex$ = do$ ("Get label of interval...", lexical_tier_number, lex_num)

				tmin = Get starting point... labeled_tier_number k
				tmax = Get end point... labeled_tier_number k
				dur = (intvl_end - intvl_start)*1000
				dur_ratio = dur/(segbf_dur + dur + segaft_dur)

				precons = tmin - 'offset'
				precons_1 = tmin + 'offset'
				cons = tmax - tmin
				postcons = tmax - 'offset'
				postcons_1 = tmax + 'offset'				


select 'intensID'

segbf_max_int = Get maximum... 'segbf_start' 'segbf_end' Parabolic
segaft_max_int = Get maximum... 'segaft_start' 'segaft_end' Parabolic
seg_min_int = Get minimum... 'tmin' 'tmax' Parabolic
seg_mean_int = Get mean... 'tmin' 'tmax' dB
int_dif = segbf_max_int - seg_min_int

select 'harmonicityID'
seg_mean_hnr = Get mean... 'tmin' 'tmax' 

# select the twice-filtered sound and get minimum and maximum within labeled interval +/- offsets

		for n from 1 to 6
			select Sound sound_'n'
			#intensID = To Intensity: f0_minimum, 0, "no"
			#select 'intensID'
			new_premin = Get minimum... 'precons' 'precons_1' Parabolic
			new_postmax = Get maximum... 'postcons' 'postcons_1' Parabolic
			#premin = Get minimum... 'precons' 'tmin' Parabolic
			#premax = Get maximum... 'precons' 'tmin' Parabolic
			#postmin = Get minimum... 'tmax' 'postcons' Parabolic
			#postmax = Get maximum... 'tmax' 'postcons' Parabolic
			#consmin = Get minimum... 'tmin' 'tmax' Parabolic
			#consmax = Get maximum... 'tmin' 'tmax' Parabolic
			#bigmin = Get minimum... 'precons' 'postcons' Parabolic
			#bigmax = Get maximum... 'precons' 'postcons' Parabolic

			#delta_i_bf = premax - consmin
			#delta_i_aft = postmax - consmin
			#delta_i = bigmax - consmin

			t_new_premin = Get time of minimum... 'precons' 'precons_1' Parabolic
			t_new_postmax = Get time of maximum... 'postcons' 'postcons_1' Parabolic
			#pre_t_min = Get time of minimum... 'precons' 'tmin' Parabolic
			#pre_t_max = Get time of maximum... 'precons' 'tmin' Parabolic
			#post_t_min = Get time of minimum... 'tmax' 'postcons' Parabolic
			#post_t_max = Get time of maximum... 'tmax' 'postcons' Parabolic
			#cons_t_min = Get time of minimum... 'tmin' 'tmax' Parabolic
			#cons_t_max = Get time of maximum... 'tmin' 'tmax' Parabolic
			#big_t_min = Get time of minimum... 'precons' 'postcons' Parabolic
			#big_t_max = Get time of maximum... 'precons' 'postcons' Parabolic
		

# write the values and the corresponding times to a text file
				
			if n = 1 
				fileappend "'directory$''output_file_name$'" 'current_file$''tab$''k''tab$''label$''tab$''segbf$''tab$''segaft$''tab$''lex$''tab$''segbf_dur''tab$''segbf_max_int''tab$''segaft_dur''tab$''segaft_max_int''tab$''dur''tab$''seg_min_int''tab$''seg_mean_int''tab$''seg_mean_hnr''tab$''int_dif''tab$''dur_ratio''tab$''new_premin:3''tab$''new_postmax:3''tab$''t_new_premin''tab$''t_new_postmax''tab$'
			else
				fileappend "'directory$''output_file_name$'" 'new_premin:3''tab$''new_postmax:3''tab$''t_new_premin''tab$''t_new_postmax''tab$'
			endif	
		#select Sound sound_'n'
		#Remove
		endfor
		
		fileappend "'directory$''output_file_name$'" 'newline$'
		
		else
		#do nothing
		endif
	endfor
endfor

# clear the decks completely before getting the next file

	select all
	minus Strings list
	Remove
endfor
select all
Remove