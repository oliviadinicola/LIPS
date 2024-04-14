
# This is an example using Gujarati feature set. Please edit this file (self.list_phonological) with the
# feature set corresponding to your trained Phonet model.

import numpy as np
import pandas as pd

class Phonological_revised:

    # ~ represents nasalization
    # 'h' next to consonant represents aspiration
    # '.' on a vowel represents breathiness
    # 'ː' represents longer vowel length
    # 'ɱ' represents the generic nasal sound (anusvara) in guj

    def __init__(self):

        self.list_phonological = {'syllabic': ["aː", "aː~", "a", "e", "e.", "ə", "ə.", "ə~", "ɛ", "ɛ.", "ɛ~", "i", "i.", "iː", "iː~", "o", "o.", "o~", "ɔ",
                                               "ɔ.", "u", "u.", "u~", "uː", "uː~", "əʋ", "əj"],
                                  'long': ["aː", "aː~", "iː", "iː~", "uː", "uː~"],
                                  'voice': ["aː", "aː~", "a", "e", "e.", "ə", "ə.", "ə~", "ɛ", "ɛ.", "ɛ~", "i", "i.", "iː", "iː~", "o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~", "əʋ", "əj", "bh", "dh", "ɖh", "ɡh", "b", "d", "ɖ", "g", "ɾ", "j", "s", "m", "l", "ɭ", "ŋ", "ɲ", "ɳ", "n", "ʋ", "ɱ"],
                                  'spread_glottis': ["e.", "ə.", "ɛ.", "i.", "o.", "ɔ.", "u.", "bh", "dh", "ɡh", "ph", "th", "ʈh", "kh", "h", "ɖh", "ʤh", "ʧh"],
                                  'sonorant': ["m", "n", "ŋ", "ɳ", "ɲ", "aː", "aː~", "a", "e", "e.", "ə", "ə.", "ə~", "ɛ", "ɛ.", "ɛ~", "i", "i.", "iː", "iː~", "o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~", "əʋ", "əj", "l", "ɭ", "ɾ", "ʋ", "j", "ɱ"],
                                  'continuant': ["aː", "aː~", "a", "e", "e.", "ə", "ə.", "ə~", "ɛ", "ɛ.", "ɛ~", "i", "i.", "iː", "iː~", "o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~", "əʋ", "əj", "j", "l", "ɭ", "s", "h", "ɾ", "ʂ", "ʋ", "ɱ"],
                                  'consonantal': ["k", "kh", "g", "ɡh", "ʧ", "ʧh", "ʤ", "ʤh", "ʈ", "ʈh", "ɖ", "ɖh", "ɳ", "n", "ɲ", "ŋ", "t", "th", "d", "dh", "p", "ph", "b", "bh", "m", "j", "ɾ", "l", "ʋ", "ʃ", "ʂ", "s", "h", "ɭ", "ɱ"],
                                  'delayed_release': ["h", "ʧ", "ʧh", "ʤ", "ʤh", "ʃ", "s", "ʂ"],
                                  'nasal': ["m", "n", "ɲ", "ŋ", "ɳ", "ɱ", "aː~", "ə~", "ɛ~", "iː~", "o~", "u~", "uː~"],
                                  'labial': ["m", "p", "ph", "b", "bh", "ʋ", "ɱ", "o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~"],
                                  'labiodental': ["ʋ", "ɱ"],
                                  'round': ["o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~"],
                                  'approximant': ["aː", "aː~", "a", "e", "e.", "ə", "ə.", "ə~", "ɛ", "ɛ.", "ɛ~", "i", "i.", "iː", "iː~", "o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~", "əʋ", "əj", "l", "ɭ", "ɾ", "j", "ʋ"],
                                  'lateral': ["l", "ɭ"],
                                  'coronal': ["l", "s", "n", "ɲ", "ɾ", "t", "th", "ʈ", "ʈh", "ɳ", "ɭ", "d", "dh", "ɖ", "ɖh", "ʂ", "ʃ", "ʧ", "ʧh", "ʤ", "ʤh"],
                                  'anterior': ["l", "ɾ", "n", "t", "th", "s", "d", "dh"],
                                  'distributed': ["ɲ", "ʃ", "ʤ", "ʤh", "ʧ", "ʧh"],
                                  'strident': ["s", "ʂ", "ʃ", "ʤ", "ʤh", "ʧ", "ʧh"],
                                  'dorsal': ["aː", "aː~", "a", "e", "e.", "ə", "ə.", "ə~", "ɛ", "ɛ.", "ɛ~", "i", "i.", "iː", "iː~", "o", "o.", "o~", "ɔ", "ɔ.", "u", "u.", "u~", "uː", "uː~", "əʋ", "əj", "k", "kh", "j", "ŋ", "ɲ", "ɳ", "g", "gh"],
                                  'high': ["i", "i.", "iː", "iː~", "u", "u.", "u~", "uː", "uː~", "ɲ", "ŋ", "k", "kh", "g", "gh", "j"],
                                  'low': ["aː", "aː~", "a"],
                                  'front': ["i", "i.", "iː", "iː~", "e", "e.", "ɛ", "ɛ.", "ɛ~", "ɲ", "j"],
                                  'back': ["u", "u.", "u~", "uː", "uː~", "o", "o.", "o~", "ɔ", "ɔ."],
                                  'tense': ["o", "o.", "o~", "e", "e.", "u", "u.", "u~", "uː", "uː~", "i", "i.", "iː", "iː~", "j"],
                                  'tap': ["ɾ"],
                                  'pause': ["sil", "spn", "<p:>", u"sil", u"sp", u'']}
        
    def get_list_phonological(self):
        return self.list_phonological

    def get_list_phonological_keys(self):
        keys=self.list_phonological.keys()
        return list(keys)

    def get_d1(self):
        keys=self.get_list_phonological_keys()
        dict_1={"xmin":[],"xmax":[],"phoneme":[],"phoneme_code":[]}
        for k in keys:
            dict_1[k]=[]
        return dict_1

    def get_d2(self):
        keys=self.get_list_phonological_keys()
        dict_2={"n_frame":[],"phoneme":[],"phoneme_code":[]}
        for k in keys:
            dict_2[k]=[]
        return dict_2

    def get_list_phonemes(self):
        keys=self.get_list_phonological_keys()
        phon=[]
        for k in keys:
            phon.append(self.list_phonological[k])
        phon=np.hstack(phon)

        return np.unique(phon)


def main():
    phon=Phonological_revised()
    keys=phon.get_list_phonological_keys()
    print(keys)
    d1=phon.get_d1()
    print(d1)
    d2=phon.get_d2()
    print(d2)
    ph=phon.get_list_phonemes()
    print(ph)

if __name__=="__main__":
    main()


