#python 3.2
import sys
import math
import codecs

class hidden_markov_model:
    '''
    '''

    def __init__(self, count_file_name):
        self.words = {}
        self.ngrams = { 1: {}, 2:{}, 3:{} }
        self.word_counts = {}

        with codecs.open(count_file_name, encoding = 'utf-8') as count_file:
            for l in count_file:
                fields = list( l.strip().split() )
                count = int( fields[0] )
                key = tuple( fields[2:] )
                if fields[1] == "WORDTAG":
                    # key is a 2-tuple ( TAG, WORD )
                    self.words[key] = count
                    self.word_counts.setdefault( key[1], 0 )
                    self.word_counts[ key[1] ] += count
                else:           #N-gram
                    # key is a 1-,2-,3-,...n- tuple
                    N = int( fields[1].split('-')[0] )
                    self.ngrams[N][key] = count

    def vocab(self):
        '''
        Returns
        -------
        vocabulary:      A list of vocabulary(tags) in the HMM.
        '''
        vocabulary = []
        for one_key in self.ngrams[1].keys():
            vocabulary.append( one_key[0] )
        return vocabulary

    def word_count(self, word):
        return self.word_counts.get(word, 0.0)

    def trigram_prob(self, trigram):
        '''
        Parameters
        ----------
        trigram:        A trigram in the HMM vocabulary.

        Returns
        -------
        q( trigram[2] | trigram[0], trigram[1] ) if non-zero, zero otherwise
        '''
        bigram = trigram[:-1]
        return self.ngrams[3].get(trigram, 0.0) / self.ngrams[2][bigram]

    def emission_prob(self, word, tag):
        '''
        Parameters
        ----------
        word:       A word in the hmm.
        tag:        A valid tag in the vocabulary.

        Returns
        e:          e(x|y) = The prob of x = word, conditioned on y = tag.
        '''
        if tag in ['*', 'STOP']:
            return 0.0
        new_word = self.replace_word(word)
        key = (tag, new_word)
        print(word, new_word, tag)
        e = self.words.get(key, 0.0) / self.ngrams[1][(tag,)]
        return e

    def replace_word(self, word):
        '''
        Replaces RARE words in the training set with a common _RARE_ symbol.
        Allows categorizing of unseen words in a future test set.
        '''

        if self.word_counts.get(word, 0) < 5:
            return "_RARE_"
        else:
            return word

    def replace_sentence(self, sentence):
        '''
        '''
        new_sentence = []
        for pair in sentence:
            w, t = pair.split()
            new_sentence.append(self.replace_word(w) + " " + t)
        return new_sentence

def read_sentences(handle):
    sentence = []
    for l in handle:
        if l.strip():
            sentence.append( l.strip() )
        else:
            yield sentence
            sentence = []
'''
def argmax(ls):
"Take a list of pairs (item, score), return the argmax."
    return max(ls, key = lambda x: x[1])

def unigram(hmm, sentence):
    "Implement PA1.1."
    # Define terms to be like notes
    n = len(sentence)

    K = hmm.tags()

    def e(x, u): return hmm.emission_prob(x, u)

    # Compute y* = argmax_y e(x | y) for all x.
    return [argmax([(y, e(x, y)) for y in K])[0] for x in sentence]
'''
def baseline_unigram(hmm, sentence):
    '''
    '''
    tagged_sent = []
    T = hmm.vocab()
    for w in sentence:
        e_max = 0
        for t in T:
            e = hmm.emission_prob(w,t)
            if e >= e_max:
                e_max = e
                tag = t
        tagged_sent.append( (w,tag) )
    return tagged_sent

if __name__ == "__main__":
    train_file = sys.argv[1]
    hmm = hidden_markov_model(train_file)
    print( hmm.ngrams )
    print( hmm.vocab() )
    print( hmm.word_count("the") )
    for t in hmm.ngrams[3]:
        print( t, hmm.trigram_prob( t ) )
    print( hmm.emission_prob("the", 'O' ) )
    print( hmm.emission_prob("the", 'I-GENE' ) )
    print( hmm.emission_prob("ryan", 'I-GENE' ) )
    print( hmm.emission_prob("ryan", 'O' ) )

    test_file = sys.argv[2]
    with codecs.open(test_file, encoding='utf-8') as tf, \
                codecs.open("gene2_dev.p1.out","w") as out:
        for sentence in read_sentences(tf):
            tagged_sent = baseline_unigram(hmm, sentence)
            print( tagged_sent )
            for pair in tagged_sent:
                out.write( pair[0] + " " + pair[1] + "\n" )
            out.write("\n")

        
