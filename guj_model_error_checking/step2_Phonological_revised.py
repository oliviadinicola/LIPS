
# Gujarati feature set

import numpy as np
import pandas as pd

class Phonological_revised:

    # ~ represents nasalization
    # 'h' next to consonant represents aspiration
    # '.' on a vowel represents breathiness
    # 'ː' represents longer vowel length
    # 'ɱ' represents the generic nasal sound (anusvara) in guj

    def __init__(self):

        self.list_phonological = "syllabic"
        
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


