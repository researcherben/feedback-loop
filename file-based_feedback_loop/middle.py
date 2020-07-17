#!/usr/bin/env python3

import json
import random
import os
import time
import datetime

parameter_file = 'parameters.json'
with open(parameter_file, 'r') as fil:
    param = json.load(fil)

#print(param)

upper_input_filename = 'from_top_to_middle'
upper_output_filename = 'from_middle_to_top'
lower_input_filename = 'from_bottom_to_middle'
lower_output_filename = 'from_middle_to_bottom'
log = 'middle.log'

done = False
while not done:
    if os.path.exists(upper_input_filename):
        with open(upper_input_filename) as fil:
            word = fil.read()
        print("middle, from top: " + word)
        # now that the word has been read in, delete the file
        os.remove(upper_input_filename)

        if word=="end":
            what_to_write = word
        else:
            what_to_write = word + str(random.randint(0,10))

        # write the enhanced word to output
        while os.path.exists(lower_output_filename):
            time.sleep(0.1)
        with open(lower_output_filename,'w') as fil:
            fil.write(what_to_write)
        with open(log,'a') as fil:
            fil.write(str(datetime.datetime.now()) + " | " + word + "\n")
        if word=="end":
            done=True
    elif os.path.exists(lower_input_filename):
        with open(lower_input_filename,'r') as fil:
            coin_result = fil.read()
        print("middle, from bottom: " + coin_result)
        os.remove(lower_input_filename)
        # wait until top has removed file before proceeding
        while os.path.exists(upper_output_filename):
            time.sleep(0.1)
        with open(upper_output_filename,'w') as fil:
            if "head" in coin_result:
                fil.write('yes, head')
            else:
                fil.write('no, tail')
