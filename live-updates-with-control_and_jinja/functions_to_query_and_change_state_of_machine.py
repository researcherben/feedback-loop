#!/usr/bin/env python3

import time
import random
import sys
import json
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

def write_json_to_log_file(json_to_log, log_filename:str) -> None:
    try:
        with open(log_filename, "a") as file_handle:
            file_handle.write(str(json_to_log)+"\n")
    except FileNotFoundError:
        with open(log_filename, "w") as file_handle:
            file_handle.write(str(json_to_log)+"\n")
    return

def poweron_machine(name_of_requestor: str,
                 log_filename: str, state_json_file:str) -> str:
    """ """
    state = query_state(state_json_file)
    print("according to 'query and change.py', state =",state)

    if "power-on" in state:
        msg_to_return="INVALID CONTROL SIGNAL RECEIVED: power was already on"
    else:
        with open(state_json_file, "w") as file_handle:
            json.dump({"state": "power-on, booting"}, file_handle)
        msg_to_return="starting boot"

    # log this event
    print("logging power on request to", send_logs_to_url)

    json_to_log={
            "%Y-%m-%d %H:%M:%S": current_time(),
            "command received by ": name_of_requestor,
            "command": "poweron_machine",
            "command result": msg_to_return
        }
    write_json_to_log_file(json_to_log, log_filename)

    return msg_to_return


def poweroff_machine(name_of_requestor: str,
        log_filename: str, state_json_file:str) -> str:
    """ """
    state = query_state(state_json_file)

    if state == "power-off":
        msg_to_return= "INVALID CONTROL SIGNAL RECEIVED: power was already off"
    else:
        with open(state_json_file, "w") as file_handle:
            json.dump({"state": "power-on, shutting-down"}, file_handle)
        msg_to_return= "initiating power-off"

    # log this event
    json_to_log={
            "%Y-%m-%d %H:%M:%S": current_time(),
            "command received by ": name_of_requestor,
            "command": "poweron_machine",
            "command result": msg_to_return
        }
    write_json_to_log_file(json_to_log, log_filename)

    return msg_to_return

def current_time() -> str:
    """
    what time is it currently?
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def query_state(state_json_file:str) -> str:
    """
    what is the state?
    """
    try:
        with open(state_json_file, "r") as file_handle:
            data = json.load(file_handle)
    except FileNotFoundError:
        data = {"state": "power-off"}
        with open(state_json_file, "w") as file_handle:
            json.dump(data, file_handle)

    return data["state"]


def doit(name:str,val: int, id: str,
         priority: str, log_filename: str, state_json_file:str) -> None:
    """ """
    if query_state(state_json_file) == "power-on, idle":
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print("exiting")
            exit(0)

        # TODO: send fake tts per phase to met

        res = str(int(val) * 2)

        print("res =", res)

        print("sending res to met")

        json_to_log={
                "%Y-%m-%d %H:%M:%S": current_time(),
                "who": name,
                "val": val,
                "res": res,
                "id": id,
                "pr": priority,
            }
        write_json_to_log_file(json_to_log, log_filename)

    else:
        msg_to_return= "INVALID CONTROL SIGNAL RECEIVED: not idle"

    return None


if __name__ == "__main__":

    print("call 'doit' or 'poweron_machine' or 'poweroff_machine'")
