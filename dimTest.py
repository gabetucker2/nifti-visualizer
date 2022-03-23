import os
from tkinter import *
import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt

#start
print()
print("PROGRAM START")
print("-------------")
print()

#init variables
print("initializing variables")
WD = os.path.dirname(os.path.realpath(__file__))
INFOLDERNAME = "INPUT"
INFOLDERPATH = os.path.join(WD, INFOLDERNAME)

#asking question
print(" - this is a test run to ensure your data is correctly set up")
print(" - time view is mostly unnoticeable due to lack of preprocessing")

INNAME = input("enter the file name of your input ('-1' selects first option) (must be in the INPUT folder): ")
if INNAME == '-1':
    INNAME = os.listdir(INFOLDERPATH)[0]
INPATH = os.path.join(INFOLDERPATH, INNAME)

c = input("enter the dimension you would like to view ('x', 'y', 'z', or 't'): ")
n = -1
valid = True

if   c == 'x':
    n = 0
elif c == 'y':
    n = 1
elif c == 'z':
    n = 2
elif c == 't':
    n = 3
else:
    print(" - invalid input, halting")
    valid = False

if valid:
    _m = input("enter your total view time: ")

    #set up fMRI data
    print("setting up fMRI data")
    NIfTI = nb.load(INPATH)
    fData = NIfTI.get_fdata()
    
    fig = plt.figure(figsize = (8, 8))
    
    m = float(_m) / fData.shape[n]

    #create a slice each second
    print("slicing volumes")
    for d in range(fData.shape[n]):
        print(" - slicing volume ", d + 1)
        slice
        if   n == 0:
            slice = fData[d, :, :, 0]
        elif n == 1:
            slice = fData[:, d, :, 0]
        elif n == 2:
            slice = fData[:, :, d, 0]
        else:
            slice = fData[fData.shape[0] / 2, :, :, d]
        fig.clear()
        plt.imshow(slice.T, cmap = 'inferno', origin = 'lower')
        plt.draw()
        plt.pause(m)

#end
print()
print("-------------")
print("PROGRAM TERMINATE")
print()
