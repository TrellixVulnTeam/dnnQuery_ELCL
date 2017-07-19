'''
A simple script for logical form verification
'''
import re
import numpy as np
import editdistance as ed
#from data_utils import basic_tokenizer
# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile(b"([,!?\"')(])")   # get rid of '.':;
_DIGIT_RE = re.compile(br"\d")

def strSimilarity(word1, word2):
    ''' Measure the similarity based on Edit Distance
    ### Measure how similar word1 is with respect to word2
    '''
    diff = ed.eval(word1.lower(), word2.lower())   #search
    # lcs = LCS(word1, word2)   #search
    length = max(len(word1), len(word2))
    if diff >= length:
        similarity = 0.0
    else:
        similarity = 1.0 * (length-diff) / length
    return similarity

'''
input files
'''
subset = 'basketball'

truth_path = "../dataover/except_%s" % subset
output_path = "../evaluation/dataover/except_%s" % subset


# train_truth = truth_path + "/rand_train.lox"
# train_output = output_path + "/logicalTemp_train.out"
# dev_truth = truth_path + "/rand_dev.lox"
# dev_output = output_path + "/logicalTemp_dev.out"
test_truth = truth_path + "/%s_test.lox" % subset
test_output = output_path + "/%s_test.out" % subset

geo_truth = truth_path + "/%s_train.lox" % subset
geo_output = output_path + "/%s_train.out" % subset

# train_truth = truth_path + "/rand_train.lo"
# train_output = output_path + "/forms_train.lo"
# dev_truth = truth_path + "/rand_dev.lo"
# dev_output = output_path + "/forms_dev.lo"
# test_truth = truth_path + "/rand_test.lo"
# test_output = output_path + "/forms_test.lo"

correct = 0
truth = []
with open(test_truth) as infile:
    for line0 in infile:
        # wordsList = basic_tokenizer(line)
        line = line0.strip()
        '''1. Strip Parentheses'''
        wordsList = line.replace('( ', '')
        wordsList = wordsList.replace(' )', '')
        '''2. Strip value types'''
        # for i in range(len(wordsList)):
        #     wordsList[i] = _DIGIT_RE.sub(b"0", wordsList[i])
        # truth.append(' '.join(wordsList))
        truth.append(wordsList.lower())
index = 0
with open(test_output) as infile:
    for line0 in infile:
        line = line0.strip()
        length = len(truth[index])
        if line.lower()[:length] == truth[index]:
            correct += 1
        else:
            # compare line with all possible forms, and choose the most similar one
            print "wrong examples: %d" %(index + 1)
            print truth[index]
            print line.lower()
            # dists = np.ones(len(loTemp))
            # for j in range(len(loTemp)):
            #     dists[j] = strSimilarity(line, loTemp[j])
            # newline = loTemp[np.argmax(dists)]
            # if newline == truth[index]:
            #     correct += 1
            # else:
            #     print "wrong examples: %d" %(index + 1)
            #     print truth[index]
            #     print line.lower()
        index += 1
print "test accuracy: " + str(correct * 1.0 / len(truth))

correct = 0
truth = []
with open(geo_truth) as infile:
    for line in infile:
        # wordsList = basic_tokenizer(line)
        wordsList = line.strip()
        # for i in range(len(wordsList)):
        #     wordsList[i] = _DIGIT_RE.sub(b"0", wordsList[i])
        # truth.append(' '.join(wordsList))
        truth.append(wordsList.lower())
index = 0
with open(geo_output) as infile:
    for line0 in infile:
        line = line0.strip()
        length = len(truth[index])
        if line.lower()[:length] == truth[index]:
            correct += 1
        else:
            # compare line with all possible forms, and choose the most similar one
            print "wrong examples: %d" %(index + 1)
            print truth[index]
            print line.lower()
            # dists = np.ones(len(loTemp))
            # for j in range(len(loTemp)):
            #     dists[j] = strSimilarity(line, loTemp[j])
            # newline = loTemp[np.argmax(dists)]
            # if newline == truth[index]:
            #     correct += 1
            # else:
            #     print "wrong examples: %d" %(index + 1)
            #     print truth[index]
            #     print line.lower()
        index += 1
print "train accuracy: " + str(correct * 1.0 / len(truth))
