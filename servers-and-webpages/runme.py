#!/usr/bin/env python3

import time
import datetime
import json
import random
import requests

"""
"""

origin_hostName = "localhost"
origin_serverPort = 1044
origin_url = 'http://'+origin_hostName+':'+str(origin_serverPort)

met_hostName = "localhost"
met_serverPort = 1033
met_url = 'http://'+met_hostName+':'+str(met_serverPort)

headers = {"charset": "utf-8", "Content-Type": "application/json"}


if __name__ == "__main__":

    r = requests.post(origin_url, json={"hello":"world"}, headers=headers)
    #print(r.text)
    #print(r.json())

    while(True):
        # get next data
        data = r.json()
        print("got",data)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("now=",now)

        r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now}, headers=headers)

        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("exiting")
            exit(0)

        data["a number"] = data["a number"]*2
        print("res_dict=",data)

        r = requests.post(origin_url, json=data, headers=headers)

        print("\n")
