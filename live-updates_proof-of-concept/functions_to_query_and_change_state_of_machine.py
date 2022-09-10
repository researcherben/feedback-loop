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


def poweron_machine(name_of_requestor: str, met_url: str, headers: dict) -> str:
    """ """
    state = query_state()

    if "power-on" in state:
        msg_to_return="INVALID CONTROL SIGNAL RECEIVED: power was already on"
    else:
        with open("machine_state.json", "w") as file_handle:
            json.dump({"state": "power-on, booting"}, file_handle)
        msg_to_return="starting boot"

    # log this event
    r = requests.post(
        met_url,
        json={
            "%Y-%m-%d %H:%M:%S": current_time(),
            "command received by ": name_of_requestor,
            "command": "poweron_machine",
            "command result": msg_to_return
        },
        headers=headers,
    )
    return msg_to_return


def poweroff_machine(name_of_requestor: str, met_url: str, headers: dict) -> str:
    """ """
    state = query_state()

    if state == "power-off":
        msg_to_return= "INVALID CONTROL SIGNAL RECEIVED: power was already off"
    else:
        with open("machine_state.json", "w") as file_handle:
            json.dump({"state": "power-on, shutting-down"}, file_handle)
        msg_to_return= "initiating power-off"

    # log this event
    r = requests.post(
        met_url,
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

def query_state() -> str:
    """ """
    with open("machine_state.json", "r") as file_handle:
        data = json.load(file_handle)

    return data["state"]


def doit(val: int, id: str, priority: str, met_url: str, headers: dict) -> None:
    """ """
    if query_state() == "power-on, idle":
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
            met_url,
            json={
                "%Y-%m-%d %H:%M:%S": current_time(),
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
