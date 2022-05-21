#!/usr/bin/env python3

import json
import random
import os
import time
import datetime

parameter_file = "parameters.json"
with open(parameter_file, "r") as fil:
    param = json.load(fil)

# print(param)

vocab = ["a", "b", "c", "d"]

log = "top.log"
lower_output_filename = "from_top_to_middle"
lower_input_filename = "from_middle_to_top"


def write_value(val, filename, log_file):
    # if the output file exists, wait for it to be removed
    while os.path.exists(
        filename
    ):  # https://linuxize.com/post/python-check-if-file-exists/
        time.sleep(0.1)
    # at this point the output file does not exist, so we can write value without overwriting
    with open(filename, "w") as fil:
        fil.write(val)
    with open(log_file, "a") as fil:
        fil.write(str(datetime.datetime.now()) + " | " + val + "\n")
    return


for indx in range(param["num words from top"]):
    val = random.choice(vocab)
    print("top: " + val)
    write_value(val, lower_output_filename, log)

    # wait for result from middle
    while not os.path.exists(lower_input_filename):
        time.sleep(0.1)
    with open(lower_input_filename, "r") as fil:
        status = fil.read()
    print(status)
    os.remove(lower_input_filename)

# after finishing the list of values, write "end" to indicate termination
write_value("end", lower_output_filename, log)
