import pickle
import os
import datetime
     
directory = 'logs/'

def log(msg):
    if not os.path.exists(directory):
        os.makedirs(directory)
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    loc = directory + today + '.log'
    with open(loc, 'a') as file:
        print(msg)
        nowd = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(nowd + '-' + msg + '\n')