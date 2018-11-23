from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
from tkinter import Widget

class ZTest:
    alpha = 'default'
    mu = 'default'
    test = 'default'
    sigma = 'default'
    mean = 'default'
    n = 'default'
    hasGraphed = 0

    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.pack()
        master.geometry('650x400')

        # Status
        self.status = Label(master, text="No Errors", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        # Instructions
        self.instructions = Label(mainFrame,
                                  text='Z Test: Either manually input required statistics or import data from a .csv file (data column must be titled "Data")',
                                  bg='purple').grid(row=0, columnspan=3)

        # alpha
        alphaInput = StringVar()

        def alphaRetrieve():
            stringAlpha = alphaInput.get()
            try:
                self.alpha = float(stringAlpha)
                if self.alpha > 0 and self.alpha < 1:
                    self.alphaValue.configure(text='\u03B1 = ' + str(self.alpha))
                    self.alphaValue.update()
                else:
                    self.status.configure(text='Please input a confidence level between 0 and 1')
                    self.status.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.alphaLabel = Label(mainFrame, text='\u03B1').grid(row=1, column=0, pady=2)
        self.alphaEntry = Entry(mainFrame, textvariable=alphaInput).grid(row=1, column=1, padx=10, pady=2)
        self.alphaButton = Button(mainFrame, text='Input', command=alphaRetrieve).grid(row=1, column=2, pady=2)
        self.alphaValue = Label(mainFrame, text=' ')
        self.alphaValue.grid(row=1, column=3, pady=2)

        # mu
        muInput = StringVar()

        def muRetrieve():
            stringMu = muInput.get()
            try:
                self.mu = float(stringMu)
                self.muValue.configure(text=u'\u03bc = ' + str(self.mu))
                self.muValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.muLabel = Label(mainFrame, text=u'\u03bc = ').grid(row=2, column=0, pady=2)
        self.muEntry = Entry(mainFrame, textvariable=muInput).grid(row=2, column=1, padx=10, pady=2)
        self.muButton = Button(mainFrame, text='Input', command=muRetrieve).grid(row=2, column=2, pady=2)
        self.muValue = Label(mainFrame, text=' ')
        self.muValue.grid(row=2, column=3, pady=2)

        # Hypothesis Testing
        def less():
            self.test = -1  # arbitrary
            self.hypothesis.configure(text='H: \u03bc < \u03bc\u2090')
            self.hypothesis.update()

        self.lessThan = Button(mainFrame, text='H: \u03bc < \u03bc\u2090', command=less).grid(row=3, column=0, pady=2)

        def greater():
            self.test = 1  # arbitrary
            self.hypothesis.configure(text='H: \u03bc > \u03bc\u2090')
            self.hypothesis.update()

        self.lessThan = Button(mainFrame, text='H: \u03bc > \u03bc\u2090', command=greater).grid(row=3, column=1,
                                                                                                 pady=2)

        def neq():
            self.test = 0  # arbitrary
            self.hypothesis.configure(text='H: \u03bc \u2260 \u03bc\u2090')
            self.hypothesis.update()

        self.lessThan = Button(mainFrame, text='H: \u03bc \u2260 \u03bc\u2090', command=neq).grid(row=3, column=2,
                                                                                                  pady=2)
        self.hypothesis = Label(mainFrame, text=' ')
        self.hypothesis.grid(row=3, column=3, pady=2)
        # Sigma
        sigmaInput = StringVar()

        def sigmaRetrieve():
            sigmaString = sigmaInput.get()
            try:
                self.sigma = float(sigmaString)
                self.sigmaValue.configure(text='\u03C3 = ' + str(self.sigma))
                self.sigmaValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.sigmaLabel = Label(mainFrame, text='\u03C3').grid(row=4, column=0, pady=2)
        self.sigmaEntry = Entry(mainFrame, textvariable=sigmaInput).grid(row=4, column=1, padx=10, pady=2)
        self.sigmaButton = Button(mainFrame, text='Input', command=sigmaRetrieve).grid(row=4, column=2, pady=2)
        self.sigmaValue = Label(mainFrame, text=' ')
        self.sigmaValue.grid(row=4, column=3, pady=2)

        # Sample Mean
        meanInput = StringVar()

        def meanRetrieve():
            meanString = meanInput.get()
            try:
                self.mean = float(meanString)
                self.meanValue.configure(text='x = ' + str(self.mean))
                self.meanValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.meanLabel = Label(mainFrame, text='Sample Mean').grid(row=5, column=0, pady=2)
        self.meanEntry = Entry(mainFrame, textvariable=meanInput).grid(row=5, column=1, padx=10, pady=2)
        self.meanButton = Button(mainFrame, text='Input', command=meanRetrieve).grid(row=5, column=2, pady=2)
        self.meanValue = Label(mainFrame, text=' ')
        self.meanValue.grid(row=5, column=3, pady=2)

        # Sample Size
        nInput = StringVar()

        def nRetrieve():
            nString = nInput.get()
            try:
                self.n = float(nString)
                self.nValue.configure(text='n = ' + str(self.n))
                self.nValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.nLabel = Label(mainFrame, text='Sample Size').grid(row=6, column=0, pady=2)
        self.nEntry = Entry(mainFrame, textvariable=nInput).grid(row=6, column=1, padx=10, pady=2)
        self.nButton = Button(mainFrame, text='Input', command=nRetrieve).grid(row=6, column=2, pady=2)
        self.nValue = Label(mainFrame, text=' ')
        self.nValue.grid(row=6, column=3, pady=2)

        # Data Location
        locationInput = StringVar()

        def locationRetrieve():
            location = locationInput.get()
            data = self.dataBreakdown(location)  # calls function
            if data == 'good':
                self.meanValue.configure(text='x = ' + str(self.mean))
                self.meanValue.update()
                self.nValue.configure(text='n = ' + str(self.n))
                self.meanValue.update()

        self.locationLabel = Label(mainFrame, text='Data Input (Optional)').grid(row=7, column=0, pady=2)
        self.locationEntry = Entry(mainFrame, textvariable=locationInput).grid(row=7, column=1, padx=10, pady=2)
        self.locationButton = Button(mainFrame, text='Input', command=locationRetrieve).grid(row=7, column=2, pady=2)
        # Calculate Button
        self.calculateButton = Button(mainFrame, text='Calculate', command=self.calculate).grid(row=8, columnspan=3,pady=2)

        self.hasGraphed = 0


    def dataBreakdown(self, location):  # ADD THIS, THEN DO GRAPHING, THEN GOOD
        try:
            with open(location, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                count = 0  # to count total data\
                position = -1
                dataList = []
                for row in reader:
                    if count == 0:  # first line, find what position the data is at
                        for i in range(0, len(row)):
                            if row[i] == 'data' or row[i] == 'Data':
                                position = i  # sets the position
                        count += 1
                    else:
                        if position == -1:  # if position was not found, break
                            self.status.configure(text='Invalid data set. Please title column "Data"')
                            self.status.update()
                            return
                        else:
                            dataList.append(row[position])
                            count += 1
                try:
                    self.n = 0
                    total = 0
                    for item in dataList:
                        total += float(item)
                        self.n += 1
                    self.mean = total / self.n
                    file.close()
                    return 'good'  # return if it be good
                except:
                    self.status.configure(text='Data Issue: Check that all data are floats')
                    self.status.update()
                    return
        except FileNotFoundError as fnf_error:
            self.status.configure(text=fnf_error)
            self.status.update()
            return

    def calculate(self):
        if self.alpha == 'default':
            self.status.configure(text='Please input a \u03B1')
            self.status.update()
        elif self.mu == 'default':
            self.status.configure(text='Please input a \u03bc')
            self.status.update()
        elif self.test == 'default':
            self.status.configure(text='Please choose an alternative hypthesis')
            self.status.update()
        elif self.sigma == 'default':
            self.status.configure(text='Please input a \u03C3')
            self.status.update()
        elif self.mean == 'default':
            self.status.configure(text='Please input a Sample Mean or input data')
            self.status.update()
        elif self.n == 'default':
            self.status.configure(text='Please input a Sample Size or input data')
            self.status.update()
        else:
            zScore = (self.mean - self.mu) / (self.sigma / np.sqrt(self.n))
            pValue = 0
            if self.test == -1:  # less than
                pValue = norm.cdf(zScore)
            elif self.test == 0:  # not equal
                pValue = 2 * (1 - norm.cdf(abs(zScore)))
            elif self.test == 1:
                pValue = 1 - norm.cdf(zScore)
            if pValue < self.alpha:
                self.status.configure(text='z = ' + str(zScore) + ', p = ' + str(pValue) + ', Reject H\u2092')
                self.status.update()
            if pValue >= self.alpha:
                self.status.configure(text='z = ' + str(zScore) + ', p = ' + str(pValue) + ', Fail to reject H\u2092')
                self.status.update()
            parent = self.status.winfo_parent()
            parentName = Widget.nametowidget(self.status, parent)
            self.graph(parentName)


    def graph(self, master):
        if self.hasGraphed == 1:
            master.winfo_children()[len(master.winfo_children()) - 1].destroy()
            master.winfo_children()[len(master.winfo_children()) - 1].destroy()
        master.geometry('670x750')
        self.hasGraphed = 1

        f = Figure(figsize=(4, 4), dpi=100)
        ax = f.add_subplot(111)
        f.add_axes()

        sigmaWeighted = self.sigma / np.sqrt(self.n) # Weight sigma, like sample mean distributions

        left = self.mu - (4 * sigmaWeighted)
        right = self.mu + (4 * sigmaWeighted)

        if self.mean > right:
            right = self.mean + 1
        if self.mean < left:
            left = self.mean - 1

        step = .01 # need to add part to shift relative to self.mean

        if sigmaWeighted > 100:
            step = sigmaWeighted/100

        x = np.arange(left, right, step)

        y1 = (1 / (sigmaWeighted * (np.sqrt(2 * np.pi)))) * np.e ** (-((x - self.mu) ** 2) / (2 * sigmaWeighted ** 2)) # Normal Dist
        y2 =  50 * (x - self.mean) #Essentially a straight line at the sample mean

        ax.plot(x, y1,label='N(\u03bc,\u03C3)',color='blue')
        ax.plot(x, y2, label='Sample Mean', color='orange' )

        if self.test == -1:  # visualize score needed, based of z = x - u / (o / sqrt(n))
            y3 = 50*(x - ((norm.ppf(self.alpha)*sigmaWeighted) + self.mu))
            ax.plot(x, y3, label='Critical Value', color='red')
            ax.fill_between(x, y3, y1, where=y3 <= y1, color='red')
        elif self.test == 0:  # not equal
            y3 = 50 * (x - ((norm.ppf(self.alpha/2) * sigmaWeighted) + self.mu))
            y4 = -50 * (x - ((norm.ppf(1 - (self.alpha/2)) * sigmaWeighted) + self.mu))
            ax.plot(x, y3, label='Critical Value Left', color='red')
            ax.fill_between(x, y3, y1, where=y3 <= y1, color='red')
            ax.plot(x, y4, label='Critical Value Right', color='red')
            ax.fill_between(x, y4, y1, where=y1 >= y4, color='red')
        elif self.test == 1:
            y3 = -50 * (x - ((norm.ppf(1-self.alpha) * sigmaWeighted) + self.mu))
            ax.plot(x, y3, label='Critical Value')
            ax.fill_between(x, y3, y1, where=y1 >= y3, color='red')

        ax.legend(loc='upper right')

        # Change y scale based upon sigma(seems to bea  good indicator of the spread of the data)
        if self.sigma < 10:
            ax.set_ylim([0, 1])
        elif self.sigma < 50:
            ax.set_ylim([0,.6])
        elif self.sigma < 100:
            ax.set_ylim([0, .4])
        else:
            ax.set_ylim([0, .2])

        canvas = FigureCanvasTkAgg(f, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        toolbar = NavigationToolbar2Tk(canvas, master)
        toolbar.update()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=TRUE)
