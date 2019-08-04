'''
data processing
'''

from __future__ import division
import os
import glob
import nltk
from string import punctuation
import config


class LanguageProcessing:

    def __init__(self,):
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.words_list()
        self.input_filedata_reader()

    def __str__(self,):
        doc = '''
            The heart of the analysis will be figuring out whether a sentence is talking about a man, woman, both or neither
            Sets intersection is used {1,2,4,6}=q {3,1,4,2}=e q.instersection(e) ={1,2,4}
            step1: The basic idea is to read each file, split it into sentences, and then process each sentence.
                    The processing begins by splitting the sentence into words and removing punctuation.!"#$%&'()*+,-/:;<=>?@[\]^_{|}~.
                    
            '''
        return doc
        


    def words_list(self):
        self.male_words=set(['guy','spokesman','chairman',"men's",'men','him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers','dad',
                             'dads','dude','father','fathers','fiance','gentleman','gentlemen','god','grandfather','grandpa','grandson',
                             'groom','he','himself','husband','husbands','king','male','man','mr','nephew','nephews','priest','prince','son',
                             'sons','uncle','uncles','waiter','widower','widowers'])
        self.female_words=set(['heroine','spokeswoman','chairwoman',"women's",'actress','women',"she's",'her','aunt',
                               'aunts','bride','daughter','daughters','female','fiancee','girl','girlfriend','girlfriends',
                               'girls','goddess','granddaughter','grandma','grandmother','herself','ladies','lady','lady','mom','moms',
                               'mother','mothers','mrs','ms','niece','nieces','priestess','princess','queens','she','sister','sisters',
                               'waitress','widow','widows','wife','wives','woman'])

    def is_it_proper(self,word):
        self.proper_nouns={}
        
        if word[0]==word[0].isupper():
            case='upper'
        else:
            case='lower'
        word_lower=word.lower()
        try:
            self.proper_nouns[word_lower][case] = self.proper_nouns[word_lower].get(case,0)+1
        except Exception as e:
            #This is triggered when the word hasn't been seen yet
            self.proper_nouns[word_lower]= {case:1}
        

    def gender_the_sentence(self,sentence_words):
        '''
        Checking how many male words intersetcted with the pre default set and measuring the length
        '''
        mw_length=len(self.male_words.intersection(sentence_words))
        fw_length=len(self.female_words.intersection(sentence_words))

        if mw_length>0 and fw_length==0:
            gender='male'
        elif mw_length==0 and fw_length>0: 
            gender='female'
        elif mw_length>0 and fw_length>0:
            print(mw_length,"\t",fw_length)
            print(self.male_words.intersection(sentence_words),"\t",self.female_words.intersection(sentence_words))
            gender='both'
        else:
            gender='none'
        return gender

    def increment_gender(self,sentence_words,gender):
        '''
        sentence_words --> is set{}
        '''
        sexes=['male','female','none','both']
        self.sentence_counter={sex:0 for sex in sexes} #sentence_counter:  {'male': 0, 'female': 0, 'none': 0, 'both': 0}
        self.word_counter={sex:0 for sex in sexes} #word counter:  {'male': 0, 'female': 0, 'none': 0, 'both': 0}
        self.word_freq={sex:{} for sex in sexes} #word_frequency:  {'male': {}, 'female': {}, 'none': {}, 'both': {}}
        print("*"*50)
        print("gender: ",gender)
        print("sentence words: ",sentence_words)
        print("word countr------->:",self.word_counter)
        self.sentence_counter[gender]+=1   #sentence_counter:  {'male': 0, 'female': 0, 'none': 0, 'both': 0} increment
        self.word_counter[gender]+=len(sentence_words)
        for word in sentence_words:
            self.word_freq[gender][word] = self.word_freq[gender].get(word,0)+1
        print(self.word_counter)
        print("*"*50)


    def input_filedata_reader(self,):
        '''
        step1: read the data from text or doc
        step2: tokenizer will do list form and make sentence upto fullstop
        step3: on  every sapce it will split in a list
        step4: in each word we are striping the punctuations
        step5: Lower case each word in a list
        step6: Finding the number of the male and female words exist with the default set
        step7: 
        '''
        for root, dirs, files in os.walk(os.getcwd()):
            print(root)
            if "data.txt" in files:
                path = root+"\\"+"data.txt"
                #Open the file
                text=open(path,'r').read()
                #Split into sentences
                sentences= self.tokenizer.tokenize(text)
            
                for sentence in sentences:
                    sentence_words=sentence.split()
                    sentence_words=[w.strip(punctuation) for w in sentence_words 
                                        if len(w.strip(punctuation))>0]
                    [self.is_it_proper(word) for word in sentence_words[1:]]
                    sentence_words=set([w.lower() for w in sentence_words])
                    gender = self.gender_the_sentence(sentence_words)
                    self.increment_gender(sentence_words,gender)
                

if __name__ == "__main__":
    process = LanguageProcessing()
    print(process)
    
