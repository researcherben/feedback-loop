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

upper_input_filename = 'from_middle_to_bottom'
upper_output_filename = 'from_bottom_to_middle'
result_filename = 'result.dat'
log = 'bottom.log'

if os.path.exists(result_filename):
    os.remove(result_filename)

done = False
while not done:
    if os.path.exists(upper_input_filename):
        with open(upper_input_filename) as fil:
            wordtime = fil.read()
        print("bottom, from middle: " + wordtime)
        # now that the word has been read in, delete the file
        os.remove(upper_input_filename)
        # write the enhanced word to output
        what_to_write = wordtime + random.choice(['x', 'y', 'z'])
        with open(result_filename,'a') as fil:
            fil.write(what_to_write + "\n")
        print("bottom, result:" + what_to_write)

        coin_flip = random.choice(['heads', 'tails'])
        while os.path.exists(upper_output_filename):
            time.sleep(0.1)
        with open(upper_output_filename, 'w') as fil:
            fil.write(coin_flip)

        with open(log,'a') as fil:
            fil.write(str(datetime.datetime.now()) + " | " + what_to_write + "-->" + coin_flip + "\n")

        if wordtime=="end":
            done=True
    else:
        time.sleep(0.1)
