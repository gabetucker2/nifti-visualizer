from asyncio.windows_events import NULL
import os
import tkinter as tk
import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines

class voxel():
    x = 0
    y = 0
    z = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "x={0}, y={1}, z={2}".format(self.x, self.y, self.z)

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

INNAME = input("enter the file name of your input ('-1' selects first option) (must be in the INPUT folder): ")
if INNAME == '-1':
    INNAME = os.listdir(INFOLDERPATH)[0]
INPATH = os.path.join(INFOLDERPATH, INNAME)
perSecond = 5
hertz = 1 / perSecond

#set up panels
print("setting up fMRI data")
NIfTI = nb.load(INPATH)
fData = NIfTI.get_fdata()

root = tk.Tk()
root.geometry("200x250+1000+200")
root.title("Focus Voxel")

loop = True

def exitProgram():
    global loop
    loop = False
    root.destroy()

maxX = fData.shape[0] - 1
labelX = tk.Label(root, text = "x (lateral/medial)")
labelX.pack()
sliderX = tk.Scale(root, from_ = 0, to = maxX, orient = tk.HORIZONTAL)
sliderX.pack()
maxY = fData.shape[1] - 1
labelY = tk.Label(root, text = "y (anterior/posterior)")
labelY.pack()
sliderY = tk.Scale(root, from_ = 0, to = maxY, orient = tk.HORIZONTAL)
sliderY.pack()
maxZ = fData.shape[2] - 1
labelZ = tk.Label(root, text = "z (inferior/superior)")
labelZ.pack()
sliderZ = tk.Scale(root, from_ = 0, to = maxZ, orient = tk.HORIZONTAL)
sliderZ.pack()
exit = tk.Button(root, text = "Exit", command = exitProgram)
exit.pack()

plt.ion()

oldVoxel = voxel(-1, -1, -1)

artists = []

xSqueeze = 0.75
ySqueeze = 0.5

#repeatedly slice
while loop:
    newVoxel = voxel(sliderX.get(), sliderY.get(), sliderZ.get())
    if str(newVoxel) != str(oldVoxel):
        print("slicing volumes")
        print(str(newVoxel))
        for d in range(3):
            fig = plt.figure(d+1, figsize = (4, 4))
            xCoord = -1
            yCoord = -1
            if d == 0:
                thisSlice = fData[newVoxel.x, :, :, 0]
                plt.title("Saggital (x)")
                xCoord = ((newVoxel.y / maxY) * xSqueeze) + ((1 - xSqueeze) * 0.5)
                yCoord = ((newVoxel.z / maxZ) * ySqueeze) + ((1 - ySqueeze) * 0.5)
            elif d == 1:
                thisSlice = fData[:, newVoxel.y, :, 0]
                plt.title("Coronal (y)")
                xCoord = ((newVoxel.x / maxX) * xSqueeze) + ((1 - xSqueeze) * 0.5)
                yCoord = ((newVoxel.z / maxZ) * ySqueeze) + ((1 - ySqueeze) * 0.5)
            elif d == 2:
                thisSlice = fData[:, :, newVoxel.z, 0]
                plt.title("Transverse (z)")
                xCoord = ((newVoxel.x / maxX) * xSqueeze) + ((1 - xSqueeze) * 0.5)
                yCoord = ((newVoxel.y / maxY) * ySqueeze) + ((1 - ySqueeze) * 0.5)
            if len(artists) == 6:
                for _i in range(2):
                    artists[0].remove()
                    artists.pop(0)
            artists.append(fig.add_artist(lines.Line2D([0, 1], [yCoord, yCoord])))
            artists.append(fig.add_artist(lines.Line2D([xCoord, xCoord], [0, 1])))
            plt.axis('off')
            plt.imshow(thisSlice.T, cmap = 'inferno', origin = 'lower')
    plt.pause(hertz)
    oldVoxel = newVoxel

#end
print()
print("-------------")
print("PROGRAM TERMINATE")
print()
