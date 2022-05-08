#!/usr/bin/env python3

import time
import random
import sys
import json
import requests
import datetime

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

def doit(val: int, id: str, priority: str, met_url:str, headers: dict) -> None:
    """
    """
    if query_state()=="on":
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print("exiting")
            exit(0)

        # TODO: send fake tts per phase to met

        res = str(int(val)*2)

        print("res =", res)

        print("sending res to met")
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now,
                "val": val,
                "res": res,
                "id": id, "pr": priority}, headers=headers)


    return None


if __name__ == "__main__":

    print("call 'doit' or 'query_state' function")
