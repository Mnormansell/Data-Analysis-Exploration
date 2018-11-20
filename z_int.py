from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
import matplotlib.pyplot as plt

class ZInt:
    alpha = 'default'
    mu = 'default'
    sigma = 'default'
    mean = 'default'
    n = 'default'

    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.pack()
        master.geometry('600x400')

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

        # Sigma
        sigmaInput = StringVar()

        def sigmaRetrieve():
            sigmaString = sigmaInput.get()
            try:
                self.sigma = float(sigmaString)
                sigmaValue = Label(mainFrame, text='\u03C3 = ' + str(self.sigma)).grid(row=3, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.sigmaLabel = Label(mainFrame, text='\u03C3').grid(row=3, column=0, pady=2)
        self.sigmaEntry = Entry(mainFrame, textvariable=sigmaInput).grid(row=3, column=1, padx=10, pady=2)
        self.sigmaButton = Button(mainFrame, text='Input', command=sigmaRetrieve).grid(row=3, column=2, pady=2)

        # Sample Mean
        meanInput = StringVar()

        def sigmaRetrieve():
            sigmaString = sigmaInput.get()
            try:
                self.sigma = float(sigmaString)
                self.sigmaValue.configure(text='\u03C3 = ' + str(self.sigma))
                self.sigmaValue.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.sigmaLabel = Label(mainFrame, text='\u03C3').grid(row=3, column=0, pady=2)
        self.sigmaEntry = Entry(mainFrame, textvariable=sigmaInput).grid(row=3, column=1, padx=10, pady=2)
        self.sigmaButton = Button(mainFrame, text='Input', command=sigmaRetrieve).grid(row=3, column=2, pady=2)
        self.sigmaValue = Label(mainFrame, text=' ')
        self.sigmaValue.grid(row=3, column=3, pady=2)

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

        self.meanLabel = Label(mainFrame, text='Sample Mean').grid(row=4, column=0, pady=2)
        self.meanEntry = Entry(mainFrame, textvariable=meanInput).grid(row=4, column=1, padx=10, pady=2)
        self.meanButton = Button(mainFrame, text='Input', command=meanRetrieve).grid(row=4, column=2, pady=2)
        self.meanValue = Label(mainFrame, text=' ')
        self.meanValue.grid(row=4, column=3, pady=2)

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

        self.nLabel = Label(mainFrame, text='Sample Size').grid(row=5, column=0, pady=2)
        self.nEntry = Entry(mainFrame, textvariable=nInput).grid(row=5, column=1, padx=10, pady=2)
        self.nButton = Button(mainFrame, text='Input', command=nRetrieve).grid(row=5, column=2, pady=2)
        self.nValue = Label(mainFrame, text=' ')
        self.nValue.grid(row=5, column=3, pady=2)
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
        self.locationLabel = Label(mainFrame, text='Data Input (Optional)').grid(row=6, column=0, pady=2)
        self.locationEntry = Entry(mainFrame, textvariable=locationInput).grid(row=6, column=1, padx=10, pady=2)
        self.locationButton = Button(mainFrame, text='Input', command=locationRetrieve).grid(row=6, column=2, pady=2)
        # Calculate Button
        self.calculateButton = Button(mainFrame, text='Calculate', command=self.calculate).grid(row=7, columnspan=3,
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
            zCrit = norm.ppf(1 - (self.alpha / 2))
            marginOfError = zCrit * self.sigma / np.sqrt(self.n)
            if self.mu < (self.mean + marginOfError) and self.mu > (self.mean - marginOfError):
                self.status.configure(text='C.I: (' + str(self.mean - marginOfError) + ', ' + str(
                    self.mean + marginOfError) + '), M.O.E = ' + str(
                    marginOfError) + ', \u03bc is in the Confidence Interval')
                self.status.update()
            else:
                self.status.configure(text='C.I: (' + str(self.mean - marginOfError) + ', ' + str(
                    self.mean + marginOfError) + '), M.O.E = ' + str(
                    marginOfError) + ', \u03bc is not in the Confidence Interval')
                self.status.update()