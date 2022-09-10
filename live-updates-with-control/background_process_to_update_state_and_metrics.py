#!/usr/bin/env python3

import time
import random
import sys
import json
import requests
import datetime
import os

"""
The possible states are
power-off
power-on, booting
power-on, idle
power-on, running-app
power-on, running-diagnostic
power-on, shutting-down

"""

if __name__ == "__main__":

    while True:
        time.sleep(1)

        # load current state
        try:
            with open("machine_state.json", "r") as file_handle:
                data = json.load(file_handle)
        except FileNotFoundError:
            data = {"state": "power-off"}
            with open("machine_state.json", "w") as file_handle:
                json.dump(data, file_handle)


        if ("idle" in data["state"]) or ("running" in data["state"]):
            with open("met.json", "w") as file_handle:
                json.dump({"key1": random.randint(3, 9),
                           "key2": random.randint(13, 19)}, file_handle)

        if "booting" in data["state"]:
            time.sleep(5)
            with open("machine_state.json", "w") as file_handle:
                json.dump({"state": "power-on, idle"}, file_handle)

        elif "shutting-down" in data["state"]:
            time.sleep(5)
            with open("machine_state.json", "w") as file_handle:
                json.dump({"state": "power-off"}, file_handle)
            # because the machine is turned off, there are no metrics being generated
            if os.path.exists("met.json"):
                os.remove("met.json")


# EOF
