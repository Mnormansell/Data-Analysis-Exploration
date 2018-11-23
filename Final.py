from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
import matplotlib.pyplot as plt

# import classes
from z_test import ZTest
from z_int import ZInt
from one_t_test import OneTTest
from two_t_test import TwoTTest
from t_int import TInt
from two_t_int import TwoTInt

from tdc import Tdc
from tdc_t import Tdc_t
from tdc_h import Tdc_h
from td_polar import limacons

main = Tk()
main.geometry("1024x500")
main.wm_title("Tk and MatLibPlot Project")


# needed functions
def zTest():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    ZTest(main)


def zInt():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    ZInt(main)


def oneSampTTest():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    OneTTest(main)


def twoSampTTest():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    TwoTTest(main)

def tInt():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    TInt(main)

def twoTInt():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    TwoTInt(main)


def tdc():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    Tdc(main)

def tdc_t():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    Tdc_t(main)

def tdc_h():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    Tdc_h(main)

def lima():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    limacons(main)

# will need classes for buttons
def createMenus():
    menu = Menu(main)
    main.config(menu=menu)
    # Stats Menu
    statsMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Statistics', menu=statsMenu)
    statsMenu.add_command(label='Z-Test', command=zTest)
    statsMenu.add_command(label='Z-Interval', command=zInt)
    statsMenu.add_separator()
    statsMenu.add_command(label='One Sample T-Test', command=oneSampTTest)
    statsMenu.add_command(label='One Sample T-Interval', command=tInt)
    statsMenu.add_command(label='Two Sample T-Test', command=twoSampTTest)
    statsMenu.add_command(label='Two Sample T-Interval', command=twoTInt)
    # Graphing Menu
    graphMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label='2D Graphing', menu=graphMenu)
    tdcMenu = Menu(menu, tearoff=0)
    graphMenu.add_cascade(label='2D Cartesian', menu = tdcMenu)
    tdcMenu.add_command(label='Quadratics', command=tdc)
    tdcMenu.add_command(label='Cubics', command=tdc_t)
    tdcMenu.add_command(label='Simple Harmonic Motion', command=tdc_h)
    graphMenu.add_separator() #seperator
    tdpMenu = Menu(menu, tearoff=0)
    graphMenu.add_cascade(label='2D Polar', menu=tdpMenu)
    tdpMenu.add_command(label='Limacons', command=lima)


    # graphMenu.add_command(label='2D Graphing', command=twoDimensional)
    # graphMenu.add_command(label='3D Graphing', command=threeDimensional)
    # graphMenu.add_separator()
    # graphMenu.add_command(label='Scatterplot', command=scatterplot)
    # graphMenu.add_command(label='Histogram', command=histogram)
    # graphMenu.add_command(label='Line Graph', command=lineGraphing)
    # graphMenu.add_command(label='Pie Graph', command=pieCharts)


# Perhaps Another menu

createMenus()
mainFrame = Frame(main)
mainFrame.pack()

introduction = Label(mainFrame, text="This personal project combines Tkinter and Matplotlib to create a streamlined math tool;", bd=1)
introduction.config(font=("Courier", 14))
introduction.pack(side=TOP, fill=X, expand=1)
introduction_2 = Label(mainFrame, text="Use the statistics menu or experiment with graphing examples", bd=1)
introduction_2.config(font=("Courier", 14))
introduction_2.pack(side=TOP, fill=X, expand=1)
# Embedding Original Graph, code from MATLIB Original Sight
fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(-3, 3, .01)
fig.add_subplot(133).plot(t, (1 / (np.sqrt(2 * np.pi))) * np.e ** (-(t ** 2) / 2))
fig.add_subplot(131).plot(t, t + np.sin(t) ** 2)
fig.add_subplot(132).plot(t, t ** 2 + np.sin(t) - 2 * t)
# figure out o get a random plot
canvas = FigureCanvasTkAgg(fig, master=mainFrame)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

# Don't update toolbar yet, that's for second part
# toolbar = NavigationToolbar2Tk(canvas, main)
# toolbar.update()



# savefig('../figures/grid_ex.png',dpi=48)

# Need first screen to just be a basic explanation of everything
# For statistics, give graph (ex show normal dist and the z-distribution stuffs, learn how to show area)
# Have option to find data from CSV file, which they can input, but they still need to input test statistic and whatever
# For other stuff figure that shit out

main.mainloop()
