#glavni program
#upravljanje zaslonom i zvukom

import lcddriver
import RPi.GPIO as GPIO

import time
import thread

import os
import sys
import mysql
import tty
import termios
import logging


DEBUG=True
VERNOSE=True

GPIO.setmode(GPIO.BCM)

buzzer = 5
relay = 6
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)