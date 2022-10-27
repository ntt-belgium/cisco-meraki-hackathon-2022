#!/usr/bin/env python 

# run: ./0_basic.py
# try with: curl http://127.0.0.1:5000/
import random
import time
import csv
import cv2
import glob
import os

from urllib.parse import parse_qs
from flask import Flask, make_response
from flask_cors import CORS
import threading


DATASET_DIR = "/Users/pmat/Projects/2022_Cisco_hackathon/Dataset"
DATA = "/Users/pmat/Projects/2022_Cisco_hackathon/fill_rate.csv"
PERSONS = "/Users/pmat/Projects/2022_Cisco_hackathon/persons.csv"
PAUSE = 400

g_value = 0
g_persons = 0

#############################
# Misc

def read_csv(filename):
   dres = {}
   try:
      with open(filename, newline='') as csvfile:
         inreader = csv.reader(csvfile, delimiter=';')
         for row in inreader:  
            dres[row[0]] = int(row[1])
   except Exception as e:
      print("exception: ", e)
   return dres

def msort(filename):
   print(filename)
   return filename

def get_lof(dirname):
   list_of_files = filter(os.path.isfile,
                        glob.glob(dirname + '/*') )
   list_of_files = sorted(list_of_files, key = msort)
   return list_of_files

#############################
# Thread

def worker():
   global g_value
   global g_persons
   first = True
   dfullness = read_csv(DATA)
   dpersons = read_csv(PERSONS)
   list_of_files = get_lof(DATASET_DIR)

#   while True:
   for filename in list_of_files:
      filename = filename.strip()
      _, ext = os.path.splitext(filename)

      if ext not in [".jpeg", ".jpg"]:
         continue

      img = cv2.imread(filename)
      cv2.imshow("Meraki MV Sens - Q2JV-4QEU-G7X6", img)

      if first:
         cv2.waitKey(0)
         first = False
      cv2.waitKey(PAUSE)   # wait in ms  
      g_value = dfullness.get(os.path.basename(filename), 0)
      g_persons = dpersons.get(os.path.basename(filename), 0)

#############################

app = Flask(__name__)
CORS(app)

@app.route('/')
def main_endpoint():
   return {
      "fullness": g_value,
      "n_persons": g_persons,
   }

def runapi():
   app.run()

if __name__ == '__main__':
   threading.Thread(target=runapi).start()
   worker()