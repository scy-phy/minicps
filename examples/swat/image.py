#!/usr/bin/python

import Tkinter as tk
from PIL import Image, ImageTk
import time
import sys

class Img:
    def __init__(self, filename, timer):
        self.__filename = filename
        self.__timer = timer * 1000
        self.__root = tk.Tk()
        self.__root.title(filename)

        # pick an image file you have .bmp  .jpg  .gif.  .png
        # load the file and covert it to a Tkinter image object
        self.__image = ImageTk.PhotoImage(Image.open(filename))

        # get the image size
        w = self.__image.width()
        h = self.__image.height()

        # position coordinates of root 'upper left corner'
        x = 0
        y = 0

        # make the root window the size of the image
        self.__root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # root has no image argument, so use a label as a panel
        self.__panel = tk.Label(self.__root, image=self.__image)
        self.__display = self.__image
        self.__panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.__root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        image = Img(sys.argv[1], int(sys.argv[2]))
