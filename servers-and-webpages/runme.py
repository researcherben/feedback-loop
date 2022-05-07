#!/usr/bin/env python3

import time
import random
import sys
import json

"""
state machine using functions below for transitions between states
 and JSON file to track current state
"""

def start() -> str:
    """
    """
    state = query_state()
    if state=="on":
        return "already on"
    else:
        with open("state.json","w") as file_handle:
            json.dump({"state": "on", "valid states": ["on", "off"]}, file_handle)
    return "started"

def stop() -> str:
    """
    """
    state = query_state()
    if state=="off":
        return "already off"
    else:
        with open("state.json","w") as file_handle:
            json.dump({"state": "off", "valid states": ["on", "off"]}, file_handle)
    return "stopped"


def query_state() -> str:
    """
    """
    with open("state.json","r") as file_handle:
        data = json.load(file_handle)

    return data["state"]

def doit(val: int) -> int:
    """
    """
    if query_state()=="on":
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print("exiting")
            exit(0)

        return str(int(val)*2)
    else:
        return None

    return None


if __name__ == "__main__":

    print("call 'doit' or 'query_state' function")
