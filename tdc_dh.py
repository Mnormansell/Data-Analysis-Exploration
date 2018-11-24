from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
import matplotlib.pyplot as plt


# damped harmonic motion a (e ^ (-y + i sqrt(w^2 - y^2)t ) + b ( e ^ (-y - isqrt(w^2 - y^2)t)
class Tdc_dh():
    def __init__(self, master):
        mainFrame = Frame(master)
        master.geometry('600x800')
        mainFrame.pack()

        instructions = Label(mainFrame, text='Visualization of damped harmonic motion')
        instructions.config(font=("Helvetica", 12))
        instructions.grid(row=0, columnspan=5)

        instructions_2 = Label(mainFrame,
                             text='Visualization equation y = a*e^(-c + i*sqrt(d^2 - c^2)) + b*e^(-c - i*sqrt(d^2-c^2))')
        instructions_2.config(font=("Helvetica", 12))
        instructions_2.grid(row=1, columnspan=5)

        # create sliders for the different coefficients
        self.labelA = Label(mainFrame, text='a')
        self.labelA.config(font=("Helvetica", 16))
        self.labelA.grid(row=2, column=0, pady=2)
        self.sliderA = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=-10, to=10,
                        tickinterval=2)
        self.sliderA.grid(row=2, column=1, padx=10, pady=2)

        self.labelB = Label(mainFrame, text='b')
        self.labelB.config(font=("Helvetica", 16))
        self.labelB.grid(row=3, column=0, pady=2)
        self.sliderB = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=-10, to=10,
                        tickinterval=2)
        self.sliderB.grid(row=3, column=1, padx=10, pady=2)

        self.labelC = Label(mainFrame, text='c')
        self.labelC.config(font=("Helvetica", 16))
        self.labelC.grid(row=4, column=0, pady=2)
        self.sliderC = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=-10, to=10,
                        tickinterval=2)
        self.sliderC.grid(row=4, column=1, padx=10, pady=2)

        #code based on https://stackoverflow.com/questions/47500266/python-tkinter-combobox
        self.selection = 1
        def on_select(event=None):
            if event:  # <-- this works only with bind because `command=` doesn't send event
                if event.widget.get() == 'Integer':
                    self.selection = 1
                elif event.widget.get() == 'Fraction':
                    self.selection = -1
            print(self.selection)

        self.comboC = ttk.Combobox(mainFrame, values=('Integer', 'Fraction'))
        self.comboC.set('Integer')
        self.comboC.grid(row=4, column=2, pady=2)
        self.comboC.bind('<<ComboboxSelected>>', on_select)


        self.labelD = Label(mainFrame, text='d')
        self.labelD.config(font=("Helvetica", 16))
        self.labelD.grid(row=5, column=0, pady=2)
        self.sliderD = Scale(mainFrame, orient=HORIZONTAL, length=300, width=20, from_=1, to=20,
                             tickinterval=2)
        self.sliderD.grid(row=5, column=1, padx=10, pady=2)

        def graph():
            while len(master.winfo_children()) > 2:
                master.winfo_children()[2].destroy()

            f = Figure(figsize=(4,4), dpi=100)
            ax = f.add_subplot(111)
            f.add_axes()

            conjugate_p = -(self.sliderC.get()**self.selection) + 1j * np.sqrt(self.sliderD.get()**2 - (self.sliderC.get()**self.selection)**2)
            conjugate_n = -(self.sliderC.get()**self.selection) - 1j * np.sqrt(self.sliderD.get() ** 2 - (self.sliderC.get()**self.selection) ** 2)
            x = np.arange(-10, 10, .01)

            y1 = self.sliderA.get()*np.e**(conjugate_p*x) + self.sliderB.get()*np.e**(conjugate_n*x)

            ax.plot(x, y1)
            ax.set_xlim([0,5])
            ax.set_ylim([-10, 10])
            ax.grid(True)

            #Title

            radical = r'\sqrt{' + str( self.sliderD.get()**2 - (self.sliderC.get()**self.selection)**2 ) + '}'
            exponent_a = r'-' + str(self.sliderC.get()) + ' + i' + radical
            if self.selection == -1:
                exponent_a = r'-\frac{1}{' + str(self.sliderC.get()) +'}' + ' + i' + radical
            exponent_b = r'-' + str(self.sliderC.get()) + ' - i' + radical
            if self.selection == -1:
                exponent_b = r'-\frac{1}{' + str(self.sliderC.get())+'}' + ' - i' + radical


            coeffA = str(self.sliderA.get())
            coeffB = str(self.sliderB.get())

            left =  coeffA + r'$e^{' + exponent_a + '}$'
            right =  coeffB + r'$e^{' + exponent_b + '}$'
            ax.set(title= left + ' + ' + right)


            canvas = FigureCanvasTkAgg(f, master=master)
            canvas.draw()
            canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=TRUE)

            toolbar = NavigationToolbar2Tk(canvas, master)
            toolbar.update()
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        update = Button(mainFrame, text='Update', command=graph)
        update.grid(rowspan=3, column=2, padx=10, pady=2)

        graph()


