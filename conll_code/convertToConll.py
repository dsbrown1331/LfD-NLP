"""
Created on Thu Apr 20 09:53:41 2017

@author: Taylor
"""
import re
import sys
import os

#get path to experiment files (user_0, user_1, etc)
path_to_source = sys.argv[1]
#get path to where we want to save .conllx file
path_to_save = sys.argv[2]
#open the conllx file
dest = open(path_to_save + '\data.conllx','w')
#go through every user folder, experiment folder, and .txt file that contains sentences
for user_folder in os.listdir(path_to_source):
    for experiment_folder in os.listdir(path_to_source + "/" + user_folder):
        for file in os.listdir(path_to_source + "/" + user_folder + "/" + experiment_folder):
            if file.endswith(".txt"):
                #open a single sentence file
                source = open(path_to_source + "/" + user_folder + "/" + experiment_folder + "/" + file, 'r')
                #read through the sentence in the file
                for line in source:
                    #keep track of words in the sentence
                    word_count = 1
                    #this splits the sentence so that punctuation is listed as a separate word
                    tokens = [t.strip() for t in re.findall(r"[\w']+|[.,!?;]", line)]
                    #look through every word
                    for word in tokens:
                        #write in conllx form to the conllx file
                        #take care of contractions
                        #add won't, can't
                        if(word == "won't"):
                            dest.write(str(word_count) + " will"  + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                            dest.write(str(word_count) + " not" + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                        elif(word[-3:] == "n't" and word != "can't"):
                            dest.write(str(word_count) + ' ' + word[:-3] + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                            dest.write(str(word_count) + ' ' + word[-3:] + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                        elif("'" in word):
                            place = word.find("'")
                            dest.write(str(word_count) + ' ' + word[:place] + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                            dest.write(str(word_count) + ' ' + word[place:] + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                        else:
                            dest.write(str(word_count) + ' ' + word + " _ _ _ _ _ _ _ _"+ '\n')
                            word_count = word_count + 1
                dest.write('\n')
                source.close()         
dest.close()
