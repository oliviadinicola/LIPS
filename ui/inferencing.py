# STEP 7
from __future__ import division

import codecs
import json
import os, sys, re
import tgt, operator
import os.path
import datetime
from tqdm import tqdm
# This is the first step in the inferencing process

# We just want the list_phonological
EXP_NAME = sys.argv[1]
phon_temp = sys.argv[2]
#    phon_temp = Phonological()
list_phonological_str = sys.argv[4]
list_phonological = eval(list_phonological_str)

# print(list_phonological.keys())

# quit()

wav_lab_dir = sys.argv[5]
tgt_dir = sys.argv[5]
feat_dir = sys.argv[5]
phc = json.loads(sys.argv[3])

files = os.listdir(wav_lab_dir)
wavfiles = [i for i in files if '.wav' in i]

from tqdm import tqdm
import random
random.seed(42)

#wavfiles = random.sample(wavfiles, 100)

# only care about continuant & sonorant
from phonet import Phonet

PH_PARAMS = {
    "phc": phc,
#	"phc": list(list_phonological.keys()),
    "EXP_NAME":  EXP_NAME
}
phon = Phonet(PH_PARAMS)

for wavfile in tqdm(wavfiles):
    stem = wavfile[:-4]
    file_feat = os.path.join(feat_dir,stem + '.postprob')
    file_audio = os.path.join(wav_lab_dir,wavfile)
    phon.get_phon_wav(file_audio, file_feat, False)

# STEP 8

phone_classes = phc
# phone_classes = list(list_phonological.keys())

printheaders = ['textgrid.file',
                # 'prepost',
                # 'sgdu',
                'word.idx.in.tg',
                'word.ortho',
                'word.ipa',
                'word.start.in.tg',
                'word.end.in.tg',
                'phone.idx.in.wd',
                'phone.ipa',
                'phone.start.in.tg',
                'phone.end.in.tg',
                'postprobframe.idx.in.phone',
                'postprobframe.start.in.tg',
                'postprobframe.end.in.tg',
                'phoneme.postprob']

for feat in phc:
    printheaders.append(feat + ".actual")
    printheaders.append(feat + ".postprob")

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
nonwords = ['NONSPNLAUGHTER', 'NONSPNTHROAT', 'NONSPNCOUGH', 'NONSPNCLICK', 'UNKSPN', 'NONSPNBREATH',
            'NONSPNLIPSMACK']
nonwords = [i.lower() for i in nonwords]

def read_textgrid(tginpath, include_empty_intervals_para):
    try:
        tg = tgt.read_textgrid(tginpath, include_empty_intervals=include_empty_intervals_para)
    except:
        print('Error reading textgrid file: ' + tginpath)
        print('Please ensure that the textgrid file is encoded in UTF-8.')
        quit()
    return tg


# Generate a unique filename based on the current date and time
current_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
# output file
outpath_fname_path = f"output/parse_post_probs_textgrids_{current_time}.tsv"

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

    print(stem_bits)

    # the index 1 split from doing stem.split is the speaker (id) -- skip beginning: arm_speakrid_uttid
    # spkr_id = stem_bits[1]

    # For PD corpus  -- see above for original
    #spkr_id = stem_bits[0]

    #	prepost = stem_bits[2]
    #	sgdu = stem_bits[3]

    # think the index of utterance id is 2
    # utt_idx_in_tg = stem_bits[2]

    # see above for original
    #utt_idx_in_tg = stem_bits[1]

    # stem = textgrid file name without the .TextGrid
    postprobfile = stem + '.postprob'
    if postprobfile not in probsfiles:
        continue

    # Joins paths of postprob (files from inference) & filename.postprob (concatenates w/ '/')
    postprobfile_path = os.path.join(feat_dir, postprobfile)

    # open file and read each line
    with open(postprobfile_path, 'r', encoding='utf-8') as f:
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
        #word_dur = word_end_time - word_start_time

        phones_in_word = phone_tier.get_annotations_between_timepoints(word_start_time, word_end_time)
        word_ipa = ' '.join([i.text for i in phones_in_word if i.text != ''])

        for phone_nr, phone_int in enumerate(phones_in_word):
            phone_start_time = phone_int.start_time
            phone_end_time = phone_int.end_time
            phone_label = phone_int.text
            phone_mid_time = (phone_end_time + phone_start_time) / 2
            #phone_dur = phone_end_time - phone_start_time

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
                                    'word.idx.in.tg': word_nr,
                                    # 'word.idx.in.utt':word_in_utt_nr,
                                    'word.ortho': word_ortho,
                                    'word.ipa': word_ipa,
                                    'word.start.in.tg': word_start_time,
                                    'word.end.in.tg': word_end_time,
                                    'phone.start.in.tg': phone_start_time,
                                    'phone.end.in.tg': phone_end_time,
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
                    phone_class + '.actual': (1 if phone_class in phone_class_dict[phone_label] else 0) for
                    phone_class
                    in phone_classes}
                # print (actual_phon_class_dict)

                '''
                # compute deviation
                devi_phon_class_dict = {}
                for phone_class in phone_classes:
                    actual_val = actual_phon_class_dict[phone_class + '.actual']
                    print(postprob_dict)
                    postprob_val = float(postprob_dict[phone_class])
                    # print (actual_val,postprob_val)
                    deviation_val = actual_val - postprob_val
                    # print (deviation_val)
                    # print (phone_class + '.dev')
                    devi_phon_class_dict[phone_class + '.dev'] = deviation_val
		'''

                for actual_header, actual_value in actual_phon_class_dict.items():
                    comp_storage_cur[actual_header] = actual_value
                #for dev_header, dev_value in devi_phon_class_dict.items():
                 #   comp_storage_cur[dev_header] = dev_value

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

