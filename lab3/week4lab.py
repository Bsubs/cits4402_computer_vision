# Joo Kai Tay, 22489437, Week 4, lab03

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage import io, color
import scipy

# Creating a root window with the name of the current lab
root=tk.Tk()
root.title('CITS4402 Week 4 Lab')
root.geometry('1400x900')

def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

# Loop used to run the application. Waits for an event to occur and process the event
root.mainloop()