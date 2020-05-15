#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO
import time
import os
import sys
from threading import Thread
import threading
import json
from select import select
import tkinter as tk
from tkinter import ttk

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buzzer = 5
relay = 6
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)
ekran = lcddriver.lcd()