import Tkinter as tk
import time
import sys

from PIL import Image, ImageTk


class ImageContainer(object):

    def __init__(self, filename, refresh_period):
        """
        :refresh_period: in msec
        """

        self.__filename = filename
        self.__refresh_period = refresh_period

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
        self.__label = tk.Label(self.__root, image=self.__image)
        self.__label.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.__root.after(self.__refresh_period, self.update_image)
        self.__root.mainloop()

    def update_image(self):
        """
        It recall itself after self.__refresh_period
        """

        try:
            self.__image = ImageTk.PhotoImage(Image.open(self.__filename))
            self.__label.config(image=self.__image)
            self.__label.after(self.__refresh_period, self.update_image)
        except:
            self.__label.after(self.__refresh_period, self.update_image)


if __name__ == '__main__':
    """Require two args:

    :filename: path to the image to contain
    :refresh_period: in ms
    """

    if len(sys.argv) == 3:
        filename = sys.argv[1]
        refresh_period = sys.argv[2]  # ms

        SLEEP = 8
        time.sleep(SLEEP)

        image_container = ImageContainer(filename, refresh_period)
    else:
        print "Pass the path to the image and the refresh-period"
        sys.exit(1)
