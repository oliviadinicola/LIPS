# Adapted from Dr. Tang's step8_parse_posterior_prob_textgrid.py in Dropbox

from __future__ import division

def run_parse_post_prob_textgrid(EXP_NAME):

    import codecs
    import os, re, sys
    import tgt, operator
    # import parselmouth
    # from parselmouth.praat import call
    import os.path
    from tqdm import tqdm

    # This is the second step in the inferencing process
    from codelibrary.step2_Phonological_revised import Phonological_revised
    # For alcohol corpus since has different phonemes--otherwise use commented out statement above
#    from codelibrary.Phonological_alcohol_english_tang import Phonological
    # We just want the list_phonological
    phon_temp = Phonological_revised()

    # For alcohol corpus since has different phonemes--otherwise use phon_temp commented out above
#    phon_temp = Phonological()
    list_phonological = phon_temp.list_phonological


    phone_classes = ['continuant', 'sonorant']
   # phone_classes = list(list_phonological.keys())

    printheaders = ['textgrid.file',
                    'spkr.id',
                    # 'prepost',
                    # 'sgdu',
                    'utt.idx.in.tg',
                    'word.idx.in.tg',
                    'word.ortho',
                    'word.ipa',
                    'word.start.in.tg',
                    'word.end.in.tg',
                    'word.dur',
                    'phone.idx.in.wd',
                    'phone.ipa',
                    'phone.dur',
                    'postprobframe.idx.in.phone',
                    'postprobframe.start.in.tg',
                    'postprobframe.end.in.tg',
                    'phoneme.postprob',
		    #'voice.actual', 'voice.postprob', 'voice.dev',
		    #'anterior.actual', 'anterior.postprob', 'anterior.dev',
		    #'back.actual', 'back.postprob', 'back.dev',
		    #'consonantal.actual', 'consonantal.postprob', 'consonantal.dev',
		    'continuant.actual', 'continuant.postprob',  'continuant.dev',
		    #'coronal.actual', 'coronal.postprob', 'coronal.dev',
                    #'close.actual', 'close.postprob', 'close.dev',
		    #'diphthong.actual', 'diphthong.postprob', 'diphthong.dev',
		    #'dorsal.actual', 'dorsal.postprob', 'dorsal.dev',
                    #'dental.actual', 'dental.postprob', 'dental.dev',
		   ## 'high.actual', 'high.postprob', 'high.dev',
                    #'front.actual', 'front.postprob', 'front.dev',
                    #'flap.actual', 'flap.postprob', 'flap.dev',
		    #'labial.actual', 'labial.postprob', 'labial.dev',
		    #'lateral.actual', 'lateral.postprob', 'lateral.dev',
		   ## 'low.actual', 'low.postprob', 'low.dev',
		    #'nasal.actual', 'nasal.postprob', 'nasal.dev',
                    #'open.actual', 'open.postprob', 'open.dev',
		    #'pause.actual', 'pause.postprob', 'pause.dev',
		   ## 'rhotic.actual', 'rhotic.postprob', 'rhotic.dev',
		    #'round.actual', 'round.postprob', 'round.dev',
		    'sonorant.actual', 'sonorant.postprob','sonorant.dev']
		    #'stress.actual', 'stress.postprob', 'stress.dev',
		    #'strident.actual', 'strident.postprob','strident.dev',
		    #'syllabic.actual', 'syllabic.postprob','syllabic.dev',
		   ## 'tense.actual', 'tense.postprob','tense.dev'.
                    #'trill.actual', 'trill.postprob', 'trill.dev']

    phone_class_dict = {}
    for phonclass, phonelist in list_phonological.items():
        # print (phonclass,phonelist)
        for phone in phonelist:
            if phone not in phone_class_dict:
                phone_class_dict[phone] = [phonclass]
            else:
                phone_class_dict[phone] += [phonclass]
    # print (phone_class_dict)
    # quit()

    # Checks for nonwords like laughing, coughs, clicks, breaths
    nonwords = ['NONSPNLAUGHTER', 'NONSPNTHROAT', 'NONSPNCOUGH', 'NONSPNCLICK', 'UNKSPN', 'NONSPNBREATH', 'NONSPNLIPSMACK']
    nonwords = [i.lower() for i in nonwords]


    def read_textgrid(tginpath, include_empty_intervals_para):
        try:
            tg = tgt.read_textgrid(tginpath, include_empty_intervals=include_empty_intervals_para)
        except:
            print('Error reading textgrid file: ' + tginpath)
            print('Please ensure that the textgrid file is encoded in UTF-8.')
            quit()
        return tg


    # directory of textgrids
    # tgt_dir = '/home/sophiavellozzi/PyCharmProjects/PhonetNew/phonet/TestExpt/textgrids'
    tgt_dir = 'DATA/FOR_INFERENCING/realigned_pd_hc_pataka'

    # directory of my postprob files (from inferences)
    feat_dir = 'TEMP_PROCESSING_DATA/posterior_probs/realigned_pd_hc_pataka'

    # output file
    outpath_fname_path = f"TRAINED_RESULTS_AND_TSV/{EXP_NAME}/parse_post_probs_textgrids_realigned_pd_hc_pataka.tsv"

    # Check to make sure output doesn't already exist and if it does, removes it
    if os.path.isfile(outpath_fname_path):
        os.remove(outpath_fname_path)

    # Returns list of textgrids
    tgtsfiles = os.listdir(tgt_dir)
    tgtsfiles = [i for i in tgtsfiles if '.TextGrid' in i]

    # Returns list of post_probs
    probsfiles = os.listdir(feat_dir)

    for tgtsfile in tqdm(tgtsfiles):
        tginpath = os.path.join(tgt_dir, tgtsfile)

        # Takes off last 9 letters from back of textgrids -> .TextGrid ; So stem is everything but .TextGrid; Did this so that it's easier to do delimiting in next steps w/ .split('_')
        stem = tgtsfile[:-9]

        # Splits name of textgrids using '_' as the delimiter
        stem_bits = stem.split('_')

        print (stem_bits)

        # the index 1 split from doing stem.split is the speaker (id) -- skip beginning: arm_speakrid_uttid
        #spkr_id = stem_bits[1]

	# For PD corpus  -- see above for original
        spkr_id = stem_bits[0]

        #	prepost = stem_bits[2]
        #	sgdu = stem_bits[3]

        # think the index of utterance id is 2
        #utt_idx_in_tg = stem_bits[2]
	
	# see above for original
        utt_idx_in_tg = stem_bits[1]

        # stem = textgrid file name without the .TextGrid
        postprobfile = stem + '.postprob'
        if postprobfile not in probsfiles:
            continue

        # Joins paths of postprob (files from inference) & filename.postprob (concatenates w/ '/')
        postprobfile_path = os.path.join(feat_dir, postprobfile)

        # open file and read each line
        with open(postprobfile_path, 'r') as f:
            postproblines = f.readlines()
        postproblines = [i.rstrip() for i in postproblines]
        headerline = postproblines[0]

        # Take header off in postprob files
        postproblines.pop(0)

        # uses commas as delimiter for header identification in postprob files
        headers = headerline.split(',')

        # These get rid of '' and 'time' in header, leaving only 'phoneme' & phon classes
        headers.pop(0)
        headers.pop(0)
        # print (headers)
        postprob_parsed_tups = []  # Get next lines
        for postprobline in postproblines:
            postprobvalues = postprobline.split(',')
            postprobvalues.pop(0)
            start_time = float(postprobvalues[0])  # start time gets from first index
            end_time = float(start_time + 0.01)
            postprobvalues.pop(0)  # then remove it; now only left with phonemes/phon classes just like w/ headers
            if len(postprobvalues) != len(headers):
                print('weird')
                quit()
            postprob_dict = {headers[postprob_nr]: postprobvalue for postprob_nr, postprobvalue in
                             enumerate(postprobvalues)}

            postprob_parsed_tups.append((start_time, end_time, postprob_dict))

        cur_tg = read_textgrid(tginpath, include_empty_intervals_para=True)
        word_tier = cur_tg.get_tier_by_name(u'words')  # item[1] in textgrid
        phone_tier = cur_tg.get_tier_by_name(u'phones')  # item[2] in textgrid

        for word_nr, word_int in enumerate(word_tier):

            # if word_nr > 100:
            #	   break
            word_ortho = word_int.text
            if word_ortho in nonwords:
                continue

            # we skip empty word labels
            if len(word_ortho.strip()) == 0:
                continue

            word_start_time = word_int.start_time
            word_end_time = word_int.end_time
            word_mid_time = (word_end_time + word_start_time) / 2
            word_dur = word_end_time - word_start_time

            phones_in_word = phone_tier.get_annotations_between_timepoints(word_start_time, word_end_time)
            word_ipa = ' '.join([i.text for i in phones_in_word if i.text != ''])

            for phone_nr, phone_int in enumerate(phones_in_word):
                phone_start_time = phone_int.start_time
                phone_end_time = phone_int.end_time
                phone_label = phone_int.text
                phone_mid_time = (phone_end_time + phone_start_time) / 2
                phone_dur = phone_end_time - phone_start_time

                # grab all frames within start_time and end_time

                postprob_cur = [(postprob_start_time, postprob_end_time, postprob_dict) for
                                postprob_start_time, postprob_end_time, postprob_dict in postprob_parsed_tups if
                                postprob_start_time >= phone_start_time and postprob_end_time <= phone_end_time]

                for postprob_cur_nr, postprob_cur_frame in enumerate(postprob_cur):

                    postprob_start_time = postprob_cur_frame[0]
                    postprob_end_time = postprob_cur_frame[1]
                    postprob_dict = postprob_cur_frame[2]

                    comp_storage_cur = {'textgrid.file': tgtsfile,

                                        'postprobframe.idx.in.phone': postprob_cur_nr,
                                        'postprobframe.start.in.tg': postprob_start_time,
                                        'postprobframe.end.in.tg': postprob_end_time,

                                        'phone.ipa': phone_label,
                                        'phone.idx.in.wd': phone_nr,
                                        'phone.dur': phone_dur,
                                        'word.idx.in.tg': word_nr,
                                        # 'word.idx.in.utt':word_in_utt_nr,
                                        'word.ortho': word_ortho,
                                        'word.ipa': word_ipa,
                                        'word.start.in.tg': word_start_time,
                                        'word.end.in.tg': word_end_time,
                                        'word.dur': word_dur,
                                        'utt.idx.in.tg': utt_idx_in_tg,
                                        'spkr.id': spkr_id,
                                        # 'prepost':prepost,
                                        # 'sgdu':sgdu,
                                        # 'gender':gender,
                                        # 'bg.noise':bgnoise_txt,
                                        # 'cross.talk':crosstalk_txt,
                                        # 'word.pre.silsp':word_pre_silsp,
                                        # 'word.fol.silsp':word_fol_silsp
                                        }
                    for postprob_header, postprob_value in postprob_dict.items():
                        comp_storage_cur[postprob_header + '.postprob'] = postprob_value
                    # phone_classes

                    if phone_label not in phone_class_dict:
                        print('missing phone_label:' + phone_label)
                        print('for:' + word_ortho)
                        quit()
                    # print (phone_label)
                    actual_phon_class_dict = {
                        phone_class + '.actual': (1 if phone_class in phone_class_dict[phone_label] else 0) for phone_class
                        in phone_classes}
                    # print (actual_phon_class_dict)

                    # compute deviation
                    devi_phon_class_dict = {}
                    for phone_class in phone_classes:
                        actual_val = actual_phon_class_dict[phone_class + '.actual']
                        print (postprob_dict)
                        postprob_val = float(postprob_dict[phone_class])
                        # print (actual_val,postprob_val)
                        deviation_val = actual_val - postprob_val
                        # print (deviation_val)
                        # print (phone_class + '.dev')
                        devi_phon_class_dict[phone_class + '.dev'] = deviation_val

                    for actual_header, actual_value in actual_phon_class_dict.items():
                        comp_storage_cur[actual_header] = actual_value
                    for dev_header, dev_value in devi_phon_class_dict.items():
                        comp_storage_cur[dev_header] = dev_value

                    if not os.path.isfile(outpath_fname_path):
                        # printheaders = sorted(list(comp_storage_cur.keys()))
                        if len(set(printheaders) - set(comp_storage_cur.keys())) != 0:
                            print('missing headers')
                            print(set(printheaders) - set(comp_storage_cur.keys()))
                            quit()
                        if len(set(comp_storage_cur.keys()) - set(printheaders)) != 0:
                            print('missing headers')
                            print(set(comp_storage_cur.keys()) - set(printheaders))
                            quit()

                        foutput = codecs.open(outpath_fname_path, 'a', 'utf-8')
                        foutput.write('\t'.join(printheaders) + '\n')
                        print(printheaders)
                    # quit()

                    # print_lines = []
                    content_list = [str(comp_storage_cur[header]) for header in printheaders]
                    # print (content_list)
                    foutput = codecs.open(outpath_fname_path, 'a', 'utf-8')
                    foutput.write('\t'.join(content_list) + '\n')
                # for output_store_word in comp_storage_cur:
                # 	content_list = [output_store_word[header] for header in printheaders]
                # 	# content_list = content_list
                # 	#print
                # 	print_lines.append('\t'.join(content_list))
                # headers = ['wav.file'] + headers
                # print_lines = ['\t'.join(printheaders)] + print_lines
