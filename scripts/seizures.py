from operator import index
from tkinter.tix import Tree
import numpy as np
import pandas as pd 
import os
from pytools import average 
import scipy
from scipy.fft import fft, fftfreq
from scipy import signal

from preprocess import ExtractBrainStateEF1ALPHA
from scripts.filter import Filter
from power import PowerSpectrum, average_power_df
from ef1_alpha_properties import recordings_1_channel, recordings_2_channels, channels_dict, genotypes

