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

        return val*2
    else:
        return None

    return None

def run(origin_url:str, met_url: str) -> None:
    while True:

        r = requests.post(origin_url, json={"hello":"world"}, headers=headers)
        data = r.json()
        print("got",data)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("now=",now)

        r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now}, headers=headers)

        if "msg" in data.keys():
            print("msg = ",str(data["msg"]))
        else:
            res = runme.doit(data["jb"]['val'])
            if res:
                r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now, "res": res}, headers=headers)


        data["a number"] = data["a number"]*2
        print("res_dict=",data)

        r = requests.post(origin_url, json=data, headers=headers)
    return

if __name__ == "__main__":

    print("call 'doit' or 'query_state' function")
