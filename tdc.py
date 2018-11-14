from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
import matplotlib.pyplot as plt


# two dimensional cartesian : parabola
class Tdc():
    def __init__(self, master):
        mainFrame = Frame(master)
        master.geometry('600x800')
        mainFrame.pack()

        instructions = Label(mainFrame, text='Visualization of the Quadratic Equation - Use the sliders to manipulate ax\u00B2 + bx + c')
        instructions.config(font=("Helvetica", 12))
        instructions.grid(row=0, columnspan=5)

        # create sliders for the different coefficients
        self.labelA = Label(mainFrame, text='a')
        self.labelA.config(font=("Helvetica", 16))
        self.labelA.grid(row=1, column=0, pady=2)
        self.sliderA = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=-10, to=10,
                        tickinterval=2)
        self.sliderA.grid(row=1, column=1, padx=10, pady=2)

        self.labelB = Label(mainFrame, text='b')
        self.labelB.config(font=("Helvetica", 16))
        self.labelB.grid(row=2, column=0, pady=2)
        self.sliderB = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=-10, to=10,
                        tickinterval=2)
        self.sliderB.grid(row=2, column=1, padx=10, pady=2)

        self.labelC = Label(mainFrame, text='c')
        self.labelC.config(font=("Helvetica", 16))
        self.labelC.grid(row=3, column=0, pady=2)
        self.sliderC = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=-10, to=10,
                        tickinterval=2)
        self.sliderC.grid(row=3, column=1, padx=10, pady=2)

        def graph():
            if len(master.winfo_children()) > 2:
                master.winfo_children()[2].destroy()
                master.winfo_children()[2].destroy()
            f = Figure(figsize=(4,4), dpi=100)
            ax = f.add_subplot(111)
            f.add_axes()

            x = np.arange(-10, 10, .01)
            ax.plot(x, (self.sliderA.get()) * x ** 2 + (self.sliderB.get()) * x + (self.sliderC.get()))
            ax.set(title=str(self.sliderA.get())+'x\u00B2 + ' + str(self.sliderB.get()) + 'x +' + str(self.sliderC.get()),
                   xlabel='x',ylabel='y')
            if self.sliderA.get() > 0:
                ax.set_ylim([-10,40])
            elif self.sliderA.get() == 0:
                ax.set_ylim([-20, 20])
            else:
                ax.set_ylim([-40, 10])

            canvas = FigureCanvasTkAgg(f, master=master)
            canvas.draw()
            canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=TRUE)

            toolbar = NavigationToolbar2Tk(canvas, master)
            toolbar.update()
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        update = Button(mainFrame, text='Update', command=graph)
        update.grid(rowspan=3, column=2, padx=10, pady=2)

        graph()


