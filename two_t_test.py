from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
import matplotlib.pyplot as plt

## Make sure you add sub scripts to titles, shift everything down (not on same row), glitch with a few inputs
class TwoTTest:
    alpha = 'none'
    mu_one = 'none'
    mu_two = 'none'
    test_one = 'none'
    test_two = 'none'
    mean_one = 'none'
    mean_two = 'none'
    stdDev_one = 'none'
    stdDev_two = 'none'
    n_one = 'none'
    n_two = 'none'
    df_one = 'none'
    df_two = 'none'

    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.pack()
        master.geometry('700x500')

        # Status
        self.status = Label(master, text="No Errors", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        # Instructions
        self.instructions = Label(mainFrame,
                                  text='One Sample T Test: Either manually input required statistics or import data from a .csv file (data column must be titled "Data")',
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
                self.mu_one = float(stringMu)
                self.muValue.configure(text=u'\u03bc\u2081 = ' + str(self.mu_one))
                self.muValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.muLabel = Label(mainFrame, text=u'\u03bc\u2081 = ').grid(row=2, column=0, pady=2)
        self.muEntry = Entry(mainFrame, textvariable=muInput).grid(row=2, column=1, padx=10, pady=2)
        self.muButton = Button(mainFrame, text='Input', command=muRetrieve).grid(row=2, column=2, pady=2)
        self.muValue = Label(mainFrame, text=' ')
        self.muValue.grid(row=2, column=3, pady=2)

        muInput_two = StringVar()

        def muRetrieve_two():
            stringMu_two = muInput_two.get()
            try:
                self.mu_two = float(stringMu_two)
                self.muValue_two.configure(text='\u03bc\u2082 = ' + str(self.mu_two))
                self.muValue_two.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.muLabel_two = Label(mainFrame, text=u'\u03bc\u2082 = ').grid(row=3, column=0, pady=2)
        self.muEntry_two = Entry(mainFrame, textvariable=muInput_two).grid(row=3, column=1, padx=10, pady=2)
        self.muButton_two = Button(mainFrame, text='Input', command=muRetrieve_two).grid(row=3, column=2, pady=2)
        self.muValue_two = Label(mainFrame, text =' ')
        self.muValue_two.grid(row=3, column=3, pady=2)

        # Hypothesis Testing
        def less():
            self.test = -1  # arbitrary
            self.hypothesis.configure(text='H: \u03bc\u2081 - \u03bc\u2082 < 0')

        self.lessThan = Button(mainFrame, text='H: \u03bc\u2081 - \u03bc\u2082 < 0', command=less).grid(row=4, column=0,
                                                                                                        pady=2)

        def greater():
            self.test = 1  # arbitrary
            self.hypothesis.configure(text='H: \u03bc\u2081 - \u03bc\u2082 > 0')
            self.hypothesis.update()

        self.lessThan = Button(mainFrame, text='H: \u03bc\u2081 - \u03bc\u2082 > 0', command=greater).grid(row=4,
                                                                                                           column=1,
                                                                                                           pady=2)

        def neq():
            self.test = 0  # arbitrary
            self.hypothesis.configure(text='H: \u03bc\u2081 \u2260 \u03bc\u2082 < 0')
            self.hypothesis.update()

        self.lessThan = Button(mainFrame, text='H: \u03bc\u2081 \u2260 \u03bc\u2082 < 0', command=neq).grid(row=4,
                                                                                                            column=2,
                                                                                                            pady=2)
        self.hypothesis = Label(mainFrame, text=' ')
        self.hypothesis.grid(row=4, column=3, pady=2)
        # Sample Mean
        meanInput = StringVar()

        def meanRetrieve():
            meanString = meanInput.get()
            try:
                self.mean_one = float(meanString)
                self.meanValue.configure(text='x\u2081 = ' + str(self.mean_one))
                self.meanValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.meanLabel = Label(mainFrame, text='Sample Mean One').grid(row=5, column=0, pady=2)
        self.meanEntry = Entry(mainFrame, textvariable=meanInput).grid(row=5, column=1, padx=10, pady=2)
        self.meanButton = Button(mainFrame, text='Input', command=meanRetrieve).grid(row=5, column=2, pady=2)
        self.meanValue = Label(mainFrame, text=' ')
        self.meanValue.grid(row=5, column=3, pady=2)

        meanInput_two = StringVar()

        def meanRetrieve_two():
            meanString_two = meanInput_two.get()
            try:
                self.mean_two = float(meanString_two)
                self.meanValue_two.configure(text='x\u2082 = ' + str(self.mean_two))
                self.meanValue_two.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.meanLabel_two = Label(mainFrame, text='Sample Mean Two').grid(row=6, column=0, pady=2)
        self.meanEntry_two = Entry(mainFrame, textvariable=meanInput_two).grid(row=6, column=1, padx=10, pady=2)
        self.meanButton_two = Button(mainFrame, text='Input', command=meanRetrieve_two).grid(row=6, column=2, pady=2)
        self.meanValue_two = Label(mainFrame, text=' ')
        self.meanValue_two.grid(row=6, column=3, pady=2)

        # Sample Standard Deviation
        stdInput = StringVar()

        def stdRetrieve():
            stdString = stdInput.get()
            try:
                self.stdDev_one = float(stdString)
                self.stdValue.configure(text='s\u2081 = ' + str(self.stdDev_one))
                self.stdValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.stdLabel = Label(mainFrame, text='Sample Std. Dev One').grid(row=7, column=0, pady=2)
        self.stdEntry = Entry(mainFrame, textvariable=stdInput).grid(row=7, column=1, padx=10, pady=2)
        self.stdButton = Button(mainFrame, text='Input', command=stdRetrieve).grid(row=7, column=2, pady=2)
        self.stdValue = Label(mainFrame, text=' ')
        self.stdValue.grid(row=7, column=3, pady=2)

        stdInput_two = StringVar()

        def stdRetrieve_two():
            stdString_two = stdInput.get()
            try:
                self.stdDev_two = float(stdString_two)
                self.stdValue_two.configure(text='s\u2082 = ' + str(self.stdDev_two))
                self.stdValue_two.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.stdLabel_two = Label(mainFrame, text='Sample Std. Dev Two').grid(row=8, column=0, pady=2)
        self.stdEntry_two = Entry(mainFrame, textvariable=stdInput_two).grid(row=8, column=1, padx=10, pady=2)
        self.stdButton_two = Button(mainFrame, text='Input', command=stdRetrieve_two).grid(row=8, column=2, pady=2)
        self.stdValue_two = Label(mainFrame, text=' ')
        self.stdValue_two.grid(row=8, column=3, pady=2)

        # Sample Size
        nInput = StringVar()

        def nRetrieve():
            nString = nInput.get()
            try:
                self.n_one = float(nString)
                self.df_one = self.n_one - 1
                self.nValue.configure(text='n\u2081 = ' + str(self.n_one))
                self.nValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.nLabel = Label(mainFrame, text='Sample Size One').grid(row=9, column=0, pady=2)
        self.nEntry = Entry(mainFrame, textvariable=nInput).grid(row=9, column=1, padx=10, pady=2)
        self.nButton = Button(mainFrame, text='Input', command=nRetrieve).grid(row=9, column=2, pady=2)
        self.nValue = Label(mainFrame, text=' ')
        self.nValue.grid(row=9, column=3, pady=2)

        nInput_two = StringVar()

        def nRetrieve_two():
            nString_two = nInput_two.get()
            try:
                self.n_two = float(nString_two)
                self.df_two = self.n_two - 1
                self.nValue_two.configure(text='n\u2082 = ' + str(self.n_two))
                self.nValue_two.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.nLabel_two = Label(mainFrame, text='Sample Size Two').grid(row=10, column=0, pady=2)
        self.nEntry_two = Entry(mainFrame, textvariable=nInput_two).grid(row=10, column=1, padx=10, pady=2)
        self.nButton_two = Button(mainFrame, text='Input', command=nRetrieve_two).grid(row=10, column=2, pady=2)
        self.nValue_two = Label(mainFrame, text=' ')
        self.nValue_two.grid(row=10, column=3, pady=2)

        # Data Location
        locationInput = StringVar()

        def locationRetrieve():
            location = locationInput.get()
            data = self.dataBreakdown(location)  # calls function
            if data == 'good':
                self.meanValue.configure(text='x\u2081 = ' + str(self.mean_one))
                self.meanValue.update()
                self.meanValue_two.configure(text='x\u2082 = ' + str(self.mean_two))
                self.meanValue_two.update()
                self.stdValue.configure(text='s\u2081 = ' + str(self.stdDev_one))
                self.stdValue.update()
                self.stdValue_two.configure(text='s\u2082 = ' + str(self.stdDev_two))
                self.stdValue_two.update()
                self.nValue.configure(text='n\u2081 = ' + str(self.n_one))
                self.nValue.update()
                self.nValue_two.configure(text='n\u2082 = ' + str(self.n_two))
                self.nValue_two.update()


        self.locationLabel = Label(mainFrame, text='Data Input (Optional)').grid(row=11, column=0, pady=2)
        self.locationEntry = Entry(mainFrame, textvariable=locationInput).grid(row=11, column=1, padx=10, pady=2)
        self.locationButton = Button(mainFrame, text='Input', command=locationRetrieve).grid(row=11, column=2, pady=2)
        # Calculate Button
        self.calculateButton = Button(mainFrame, text='Calculate', command=self.calculate).grid(row=12, columnspan=3,
                                                                                                pady=2)

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
                            if row[i] == 'data' or 'Data':
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
                # try:
                self.n = 0
                total = 0
                partialSum = 0
                for item in dataList:
                    total += float(item)
                    self.n += 1
                self.mean = total / self.n
                self.df = self.n - 1
                for item in dataList:
                    partialSum += (float(item) - self.mean) ** 2
                self.stdDev = np.sqrt(partialSum / (self.n - 1))
                return 'good'  # return if it be good
                # except:
                #     self.status.configure(text='Data Issue: Check that all data are floats')
                #     self.status.update()
                #     return
        except FileNotFoundError as fnf_error:
            self.status.configure(text=fnf_error)
            self.status.update()
            return

    def calculate(self):
        if self.alpha == 'default':
            self.status.configure(text='Please input an \u03B1')
            self.status.update()
        elif self.mu == 'default':
            self.status.configure(text='Please input a \u03bc')
            self.status.update()
        elif self.test == 'default':
            self.status.configure(text='Please choose and alternative hypthesis')
            self.status.update()
        elif self.stdDev == 'default':
            self.status.configure(text='Please input a sample standard deviation')
            self.status.update()
        elif self.mean == 'default':
            self.status.configure(text='Please input a Sample Mean or input data')
            self.status.update()
        elif self.n == 'default':
            self.status.configure(text='Please input a Sample Size or input data')
            self.status.update()
        else:
            tScore = (self.mean - self.mu) / (self.stdDev / np.sqrt(self.n))
            pValue = 0
            if self.test == -1:  # less than
                pValue = sci.t.cdf(tScore, self.df)
            elif self.test == 0:  # not equal
                pValue = 2 * (1 - sci.t.cdf(abs(tScore), self.df))
            elif self.test == 1:
                pValue = 1 - sci.t.cdf(tScore, self.df)
            if pValue < self.alpha:
                self.status.configure(text='t = ' + str(tScore) + ', p = ' + str(pValue) + ', Reject H\u2092')
                self.status.update()
            if pValue >= self.alpha:
                self.status.configure(text='t = ' + str(tScore) + ', p = ' + str(pValue) + ', Fail to reject H\u2092')
                self.status.update()
