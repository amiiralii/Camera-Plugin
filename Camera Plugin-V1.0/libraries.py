import sys
import cv2
import os
import qimage2ndarray
import pathlib
from copy import deepcopy
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from DigiCam.Camera import Camera
from os.path import join, sep
import datetime
CAMERA_CONTROL_CMD_PATH = join('C:' + sep, 'Program Files (x86)', 'digiCamControl', 'CameraControlCmd.exe')
import time
import matplotlib.pyplot as plt
import random
import matplotlib
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from qtrangeslider import QLabeledRangeSlider
from qtrangeslider.qtcompat import QtWidgets as QtW
# All the libraries used in the app