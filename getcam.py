#!/usr/bin/env python 

import os
from numpy import str0
import requests as rq
from datetime import datetime, timedelta, timezone
import time


START_TS = datetime.now(tz=timezone.utc) - timedelta(days=2)
INCR_MINUTES = 5 

SERIAL_CAM = "Q2JV-4QEU-G7X6"
OUTPUT_DIR = "./Dataset"

def get_images(sdate:str):
    print("sdate: ", sdate)
    url = f"https://n308.meraki.com/api/v1/devices/{SERIAL_CAM}/camera/generateSnapshot"
    headers = {
        "X-Cisco-Meraki-API-Key" : "d0703acbdfaebdee766ffa43f1f9e877a3579e2a",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    rep = rq.post(url, headers=headers, json={"timestamp": sdate, "fullframe": False})
    if rep.status_code >= 300:
        return None
        
    try:
        #print(str(rep.json()["url"]))
        time.sleep(1) # wait for the image to be ready 
        rep_jpg = rq.get(str(rep.json()["url"]))
        result = rep_jpg.content
        #print(result)
    except: 
        result = None
    
    return result


def main():
    os.system(f"mkdir -p {OUTPUT_DIR}")

    current_time = START_TS
    while current_time < datetime.now(tz=timezone.utc):
        isodate = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"{isodate}: ", end='')
        current_time += timedelta(minutes=INCR_MINUTES)

        image_content = get_images(isodate)
        if image_content:
            filename = f"{SERIAL_CAM}_" + isodate
            print(filename)
            fd = open(f"{OUTPUT_DIR}/{filename}.jpg", "wb")
            fd.write(image_content)
            fd.close()
        else:
            print(" not exist")

if __name__ == "__main__":
    main()




