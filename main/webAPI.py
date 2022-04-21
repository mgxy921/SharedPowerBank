import os
import sys
import threading
import Woshi
from flask import Flask
import flaskTest


class webAPI(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print('webAPI')
        flaskTest.flaskRUN(host='127.0.0.1', port=5000)
