#!/usr/bin/env python3

import time
import random
import sys
import json
import requests
import datetime

"""
state machine as JSON using functions below to trigger transitions between states


+--------------+    +------------------------------------+
| power-is-off |    | power-is-on                        |
+--------^-+---+    |                                    |
         | |        |      +------------+                |
         | +--------+------> booting-up |                |
         |          |      +----+-------+                |
         |          |           |                        |
         |          | +----+----v--------+               |
         |          | |    | system-idle <----------+    |
         |          | | +--+----+----^---+          |    |
         |          | | |       |    |              |    |
         |          | | |  +----v----+----------+   |    |
         |          | | |  | system-running-app |   |    |
         |          | | |  +--------------------+   |    |
         |          | | |                           |    |
         |          | | |  +------------------------+--+ |
         |          | | +--> system-running-diagnostic | |
         |          | |    +---------------------------+ |
         |          | |                                  |
         |          | +-----+                            |
         |          |       |                            |
         |          |      +v---------------------+      |
         +----------+------+ system-shutting-down |      |
                    |      +----------------------+      |
                    +------+----------------------+------+

The possible states are
power-off
power-on, booting
power-on, idle
power-on, running-app
power-on, running-diagnostic
power-on, shutting-down

"""


def poweron_machine(name_of_requestor: str,
                 send_logs_to_url: str, headers: dict, json_file:str) -> str:
    """ """
    state = query_state(json_file)
    print("according to 'query and change.py', state =",state)

    if "power-on" in state:
        msg_to_return="INVALID CONTROL SIGNAL RECEIVED: power was already on"
    else:
        with open(json_file, "w") as file_handle:
            json.dump({"state": "power-on, booting"}, file_handle)
        msg_to_return="starting boot"

    # log this event
    print("logging power on request to", send_logs_to_url)
    r = requests.post(
        send_logs_to_url,
        json={
            "%Y-%m-%d %H:%M:%S": current_time(),
            "command received by ": name_of_requestor,
            "command": "poweron_machine",
            "command result": msg_to_return
        },
        headers=headers,
    )
    print("done with log; returning control")
    return msg_to_return


def poweroff_machine(name_of_requestor: str,
        send_logs_to_url: str, headers: dict, json_file:str) -> str:
    """ """
    state = query_state(json_file)

    if state == "power-off":
        msg_to_return= "INVALID CONTROL SIGNAL RECEIVED: power was already off"
    else:
        with open(json_file, "w") as file_handle:
            json.dump({"state": "power-on, shutting-down"}, file_handle)
        msg_to_return= "initiating power-off"

    # log this event
    r = requests.post(
        send_logs_to_url,
        json={
            "%Y-%m-%d %H:%M:%S": current_time(),
            "command received by ": name_of_requestor,
            "command": "poweron_machine",
            "command result": msg_to_return
        },
        headers=headers,
    )
    return msg_to_return

def current_time() -> str:
    """
    what time is it currently?
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def query_state(json_file:str) -> str:
    """
    what is the state?
    """
    try:
        with open(json_file, "r") as file_handle:
            data = json.load(file_handle)
    except FileNotFoundError:
        data = {"state": "power-off"}
        with open(json_file, "w") as file_handle:
            json.dump(data, file_handle)

    return data["state"]


def doit(name:str,val: int, id: str,
         priority: str, send_logs_to_url: str, headers: dict, json_file:str) -> None:
    """ """
    if query_state(json_file) == "power-on, idle":
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print("exiting")
            exit(0)

        # TODO: send fake tts per phase to met

        res = str(int(val) * 2)

        print("res =", res)

        print("sending res to met")

        r = requests.post(
            send_logs_to_url,
            json={
                "%Y-%m-%d %H:%M:%S": current_time(),
                "who": name,
                "val": val,
                "res": res,
                "id": id,
                "pr": priority,
            },
            headers=headers,
        )
    else:
        msg_to_return= "INVALID CONTROL SIGNAL RECEIVED: not idle"

    return None


if __name__ == "__main__":

    print("call 'doit' or 'poweron_machine' or 'poweroff_machine'")
