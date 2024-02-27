


def run_inferencing(EXP_NAME):
    import os,sys
    #sys.path.append('/home/sophiavellozzi/phonet/phonet')
    # os.chdir()



    # This is the first step in the inferencing process
    from codelibrary.step2_Phonological_revised import Phonological_revised
#    from codelibrary.Phonological_english_librispeech import Phonological
    # We just want the list_phonological
    phon_temp = Phonological_revised()
#    phon_temp = Phonological()
    list_phonological = phon_temp.list_phonological
    # print(list_phonological.keys())

    # quit()



    wav_lab_dir = 'DATA/FOR_INFERENCING/realigned_pd_hc_pataka/'
    feat_dir = 'TEMP_PROCESSING_DATA/posterior_probs/realigned_pd_hc_pataka/'
    files = os.listdir(wav_lab_dir)
    wavfiles = [i for i in files if '.wav' in i]

    from tqdm import tqdm
    import random
    random.seed(42)


    #wavfiles = random.sample(wavfiles, 100)

    # only care about continuant & sonorant
    from phonet import Phonet

    PH_PARAMS = {
        "phc": ["continuant", "sonorant"],
#	"phc": list(list_phonological.keys()),
        "EXP_NAME":  EXP_NAME
    }
    phon = Phonet(PH_PARAMS)

    for wavfile in tqdm(wavfiles):
        stem = wavfile[:-4]
        file_feat = os.path.join(feat_dir,stem + '.postprob')
        file_audio = os.path.join(wav_lab_dir,wavfile)
        phon.get_phon_wav(file_audio, file_feat, False)

# def predict_on_wavfile(wavfile):
#     # Use only CPU
#     import os
#     os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
#     # only care about continuant & sonorant
#     from phonet import Phonet
#     phon = Phonet(["continuant", "sonorant"])
#
#     file_feat = os.path.join(feat_dir, wavfile.replace(".wav", ".postprob"))
#     file_audio = os.path.join(wav_lab_dir, wavfile)
#     return phon.get_phon_wav(file_audio, file_feat, False)
#
# import multiprocessing as mp
# with mp.Pool(10) as pool:
#     responses = tqdm(pool.imap(predict_on_wavfile, wavfiles), total=20)
#     tuple(responses) # Executes the parallel process
#     print("Inferencing done!")
