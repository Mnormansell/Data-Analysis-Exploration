from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
import scipy.stats as sci
import csv
import matplotlib.pyplot as plt

#Need Alpha, U, Sigma, Mean, Or Data location z = x - u / o
#Errors, after inputting data, you can't overwrite things
#When you click a button it just creates another, need to delete everyhing
class ZTest:
    alpha = 'default'
    mu = 'default'
    test = 'default'
    sigma = 'default'
    mean = 'default'
    n = 'default'
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.pack()
        main.geometry('600x400')

        #Status
        self.status = Label(master, text="No Errors", bd=1,relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        #Instructions
        self.instructions = Label(mainFrame,text='Z Test: Either manually input required statistics or import data from a .csv file (data column must be titled "Data")',bg='purple').grid(row=0,columnspan=3)

        #alpha
        alphaInput = StringVar()
        def alphaRetrieve():
            stringAlpha = alphaInput.get()
            try:
                self.alpha = float(stringAlpha)
                if self.alpha > 0 and self.alpha < 1:
                    alphaValue = Label(mainFrame, text='\u03B1 = ' + str(self.alpha)).grid(row=1, column=3, pady=2)
                else:
                    self.status.configure(text='Please input a confidence level between 0 and 1')
                    self.status.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.alphaLabel = Label(mainFrame, text='\u03B1').grid(row=1, column=0, pady=2)
        self.alphaEntry = Entry(mainFrame,textvariable=alphaInput).grid(row=1, column=1, padx=10, pady=2)
        self.alphaButton = Button(mainFrame, text='Input', command=alphaRetrieve).grid(row=1, column=2, pady=2)

        #mu
        muInput = StringVar()
        def muRetrieve():
            stringMu = muInput.get()
            try:
                self.mu = float(stringMu)
                muValue = Label(mainFrame, text=u'\u03bc = '+str(self.mu)).grid(row=2, column=3, pady=2 )
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.muLabel = Label(mainFrame, text=u'\u03bc = ').grid(row=2, column=0, pady=2)
        self.muEntry = Entry(mainFrame, textvariable=muInput).grid(row=2, column=1, padx=10, pady=2)
        self.muButton = Button(mainFrame, text='Input', command=muRetrieve).grid(row=2, column=2, pady=2)

        #Hypothesis Testing
        def less():
            self.test = -1 #arbitrary
            hypothesis = Label(mainFrame, text='H: \u03bc < \u03bc\u2090').grid(row=3, column=3, pady=2)
        self.lessThan = Button(mainFrame, text = 'H: \u03bc < \u03bc\u2090', command=less).grid(row=3, column=0, pady=2)
        def greater():
            self.test = 1 #arbitrary
            hypothesis = Label(mainFrame, text='H: \u03bc > \u03bc\u2090').grid(row=3, column=3, pady=2)
        self.lessThan = Button(mainFrame, text = 'H: \u03bc > \u03bc\u2090', command=greater).grid(row=3, column=1, pady=2)
        def neq():
            self.test = 0 #arbitrary
            self.hypothesis = Label(mainFrame, text='H: \u03bc \u2260 \u03bc\u2090').grid(row=3, column=3, pady=2)
        self.lessThan = Button(mainFrame, text = 'H: \u03bc \u2260 \u03bc\u2090', command=neq).grid(row=3, column=2, pady=2)

        #Sigma
        sigmaInput = StringVar()
        def sigmaRetrieve():
            sigmaString = sigmaInput.get()
            try:
                self.sigma = float(sigmaString)
                sigmaValue = Label(mainFrame, text='\u03C3 = ' + str(self.sigma)).grid(row=4, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.sigmaLabel = Label(mainFrame, text='\u03C3').grid(row=4, column=0, pady=2)
        self.sigmaEntry = Entry(mainFrame, textvariable=sigmaInput).grid(row=4, column=1, padx=10, pady=2)
        self.sigmaButton = Button(mainFrame, text='Input', command=sigmaRetrieve).grid(row=4, column=2, pady=2)

        #Sample Mean
        meanInput = StringVar()
        def meanRetrieve():
            meanString = meanInput.get()
            try:
                self.mean = float(meanString)
                meanValue = Label(mainFrame, text='x = '+str(self.mean)).grid(row=5, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.meanLabel = Label(mainFrame, text='Sample Mean').grid(row=5, column=0, pady=2)
        self.meanEntry = Entry(mainFrame, textvariable=meanInput).grid(row=5, column=1, padx=10, pady=2)
        self.meanButton = Button(mainFrame, text='Input', command=meanRetrieve).grid(row=5, column=2, pady=2)

        # Sample Size
        nInput = StringVar()
        def nRetrieve():
            nString = nInput.get()
            try:
                self.n = float(nString)
                nValue = Label(mainFrame, text='n = ' + str(self.n)).grid(row=6, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.nLabel = Label(mainFrame, text='Sample Size').grid(row=6, column=0, pady=2)
        self.nEntry = Entry(mainFrame, textvariable=nInput).grid(row=6, column=1, padx=10, pady=2)
        self.nButton = Button(mainFrame, text='Input', command=nRetrieve).grid(row=6, column=2, pady=2)
        # Data Location
        locationInput = StringVar()
        def locationRetrieve():
            location = locationInput.get()
            data = self.dataBreakdown(location) #calls function
            if data == 'good':
                meanValue = Label(mainFrame, text='x = ' + str(self.mean)).grid(row=5, column=3, pady=2)
                nValue = Label(mainFrame, text='n = ' + str(self.n)).grid(row=6, column=3, pady=2)
        self.locationLabel = Label(mainFrame, text='Data Input (Optional)').grid(row=7, column=0, pady=2)
        self.locationEntry = Entry(mainFrame, textvariable=locationInput).grid(row=7, column=1, padx=10, pady=2)
        self.locationButton = Button(mainFrame, text='Input', command=locationRetrieve).grid(row=7, column=2, pady=2)
        #Calculate Button
        self.calculateButton = Button(mainFrame, text='Calculate',command=self.calculate).grid(row=8,columnspan=3,pady=2)

    def dataBreakdown(self, location): #ADD THIS, THEN DO GRAPHING, THEN GOOD
        try:
            with open(location, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                count = 0 #to count total data\
                position = -1
                dataList = []
                for row in reader:
                    if count == 0: #first line, find what position the data is at
                        for i in range(0, len(row)):
                            if row[i] == 'data' or 'Data':
                                position = i #sets the position
                        count += 1
                    else:
                        if position == -1: #if position was not found, break
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
                    self.mean = total/self.n
                    return 'good' #return if it be good
                except:
                    self.status.configure(text='Data Issue: Check that all data are floats')
                    self.status.update()
                    return
        except FileNotFoundError as fnf_error:
            self.status.configure(text=fnf_error+'failed here')
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
            self.status.configure(text='Please choose and alternative hypthesis')
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
            zScore = (self.mean - self.mu)/(self.sigma/np.sqrt(self.n))
            pValue = 0
            if self.test == -1: #less than
                pValue = norm.cdf(zScore)
            elif self.test == 0: #not equal
                pValue = 2 * (1 - norm.cdf(abs(zScore)))
            elif self.test == 1:
                pValue = 1 - norm.cdf(zScore)
            if pValue < self.alpha:
                self.status.configure(text='z = ' + str(zScore) + ', p = ' + str(pValue) + ', Reject H\u2092')
                self.status.update()
            if pValue >= self.alpha:
                self.status.configure(text='z = ' + str(zScore) + ', p = ' + str(pValue) + ', Fail to reject H\u2092')
                self.status.update()

class oneTTest:
    alpha = 'default'
    mu = 'default'
    test = 'default'
    mean = 'default'
    stdDev = 'default'
    n = 'default'
    df = 'default'
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.pack()
        main.geometry('700x400')

        #Status
        self.status = Label(master, text="No Errors", bd=1,relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        #Instructions
        self.instructions = Label(mainFrame,text='One Sample T Test: Either manually input required statistics or import data from a .csv file (data column must be titled "Data")',bg='purple').grid(row=0,columnspan=3)

        #alpha
        alphaInput = StringVar()
        def alphaRetrieve():
            stringAlpha = alphaInput.get()
            try:
                self.alpha = float(stringAlpha)
                if self.alpha > 0 and self.alpha < 1:
                    alphaValue = Label(mainFrame, text='\u03B1 = ' + str(self.alpha)).grid(row=1, column=3, pady=2)
                else:
                    self.status.configure(text='Please input a confidence level between 0 and 1')
                    self.status.update()
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.alphaLabel = Label(mainFrame, text='\u03B1').grid(row=1, column=0, pady=2)
        self.alphaEntry = Entry(mainFrame,textvariable=alphaInput).grid(row=1, column=1, padx=10, pady=2)
        self.alphaButton = Button(mainFrame, text='Input', command=alphaRetrieve).grid(row=1, column=2, pady=2)

        #mu
        muInput = StringVar()
        def muRetrieve():
            stringMu = muInput.get()
            try:
                self.mu = float(stringMu)
                muValue = Label(mainFrame, text=u'\u03bc = '+str(self.mu)).grid(row=2, column=3, pady=2 )
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.muLabel = Label(mainFrame, text=u'\u03bc = ').grid(row=2, column=0, pady=2)
        self.muEntry = Entry(mainFrame, textvariable=muInput).grid(row=2, column=1, padx=10, pady=2)
        self.muButton = Button(mainFrame, text='Input', command=muRetrieve).grid(row=2, column=2, pady=2)

        #Hypothesis Testing
        def less():
            self.test = -1 #arbitrary
            hypothesis = Label(mainFrame, text='H: \u03bc < \u03bc\u2090').grid(row=3, column=3, pady=2)
        self.lessThan = Button(mainFrame, text = 'H: \u03bc < \u03bc\u2090', command=less).grid(row=3, column=0, pady=2)
        def greater():
            self.test = 1 #arbitrary
            hypothesis = Label(mainFrame, text='H: \u03bc > \u03bc\u2090').grid(row=3, column=3, pady=2)
        self.lessThan = Button(mainFrame, text = 'H: \u03bc > \u03bc\u2090', command=greater).grid(row=3, column=1, pady=2)
        def neq():
            self.test = 0 #arbitrary
            self.hypothesis = Label(mainFrame, text='H: \u03bc \u2260 \u03bc\u2090').grid(row=3, column=3, pady=2)
        self.lessThan = Button(mainFrame, text = 'H: \u03bc \u2260 \u03bc\u2090', command=neq).grid(row=3, column=2, pady=2)

        #Sample Mean
        meanInput = StringVar()
        def meanRetrieve():
            meanString = meanInput.get()
            try:
                self.mean = float(meanString)
                meanValue = Label(mainFrame, text='x = '+str(self.mean)).grid(row=4, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.meanLabel = Label(mainFrame, text='Sample Mean').grid(row=4, column=0, pady=2)
        self.meanEntry = Entry(mainFrame, textvariable=meanInput).grid(row=4, column=1, padx=10, pady=2)
        self.meanButton = Button(mainFrame, text='Input', command=meanRetrieve).grid(row=4, column=2, pady=2)

        #Sample Standard Deviation
        stdInput = StringVar()
        def stdRetrieve():
            stdString = stdInput.get()
            try:
                self.stdDev= float(stdString)
                stdValue = Label(mainFrame, text='s = '+str(self.stdDev)).grid(row=5, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.stdLabel = Label(mainFrame, text='Sample Std. Dev').grid(row=5, column=0, pady=2)
        self.stdEntry = Entry(mainFrame, textvariable=stdInput).grid(row=5, column=1, padx=10, pady=2)
        self.stdButton = Button(mainFrame, text='Input', command=stdRetrieve).grid(row=5, column=2, pady=2)

        # Sample Size
        nInput = StringVar()
        def nRetrieve():
            nString = nInput.get()
            try:
                self.n = float(nString)
                self.df = self.n - 1
                nValue = Label(mainFrame, text='n = ' + str(self.n)).grid(row=6, column=3, pady=2)
            except:
                self.status.configure(text='Invalid Input')
                self.status.update()

        self.nLabel = Label(mainFrame, text='Sample Size').grid(row=6, column=0, pady=2)
        self.nEntry = Entry(mainFrame, textvariable=nInput).grid(row=6, column=1, padx=10, pady=2)
        self.nButton = Button(mainFrame, text='Input', command=nRetrieve).grid(row=6, column=2, pady=2)
        # Data Location
        locationInput = StringVar()
        def locationRetrieve():
            location = locationInput.get()
            data = self.dataBreakdown(location) #calls function
            if data == 'good':
                meanValue = Label(mainFrame, text='x = ' + str(self.mean)).grid(row=4, column=3, pady=2)
                nValue = Label(mainFrame, text='n = ' + str(self.n)).grid(row=6, column=3, pady=2)
                stdValue = Label(mainFrame, text='s = ' + str(self.stdDev)).grid(row=5, column=3, pady=2)
        self.locationLabel = Label(mainFrame, text='Data Input (Optional)').grid(row=7, column=0, pady=2)
        self.locationEntry = Entry(mainFrame, textvariable=locationInput).grid(row=7, column=1, padx=10, pady=2)
        self.locationButton = Button(mainFrame, text='Input', command=locationRetrieve).grid(row=7, column=2, pady=2)
        #Calculate Button
        self.calculateButton = Button(mainFrame, text='Calculate',command=self.calculate).grid(row=8,columnspan=3,pady=2)

    def dataBreakdown(self, location): #ADD THIS, THEN DO GRAPHING, THEN GOOD
        try:
            with open(location, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                count = 0 #to count total data\
                position = -1
                dataList = []
                for row in reader:
                    if count == 0: #first line, find what position the data is at
                        for i in range(0, len(row)):
                            if row[i] == 'data' or 'Data':
                                position = i #sets the position
                        count += 1
                    else:
                        if position == -1: #if position was not found, break
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
                self.mean = total/self.n
                self.df = self.n - 1
                for item in dataList:
                    partialSum += (float(item) - self.mean)**2
                self.stdDev = np.sqrt(partialSum/(self.n-1))
                return 'good' #return if it be good
                # except:
                #     self.status.configure(text='Data Issue: Check that all data are floats')
                #     self.status.update()
                #     return
        except FileNotFoundError as fnf_error:
            self.status.configure(text=fnf_error+'failed here')
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
            tScore = (self.mean - self.mu)/(self.stdDev/np.sqrt(self.n))
            pValue = 0
            if self.test == -1: #less than
                pValue = sci.t.cdf(tScore, self.df)
            elif self.test == 0: #not equal
                pValue = 2 * (1 - sci.t.cdf(abs(tScore), self.df))
            elif self.test == 1:
                pValue = 1 - sci.t.cdf(tScore, self.df)
            if pValue < self.alpha:
                self.status.configure(text='t = ' + str(tScore) + ', p = ' + str(pValue) + ', Reject H\u2092')
                self.status.update()
            if pValue >= self.alpha:
                self.status.configure(text='t = ' + str(tScore) + ', p = ' + str(pValue) + ', Fail to reject H\u2092')
                self.status.update()

main = Tk()
main.geometry("1024x500")
main.wm_title("Tk and MatLibPlot Project")
#needed functions
def zTest():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    ZTest(main)
def oneSampTTest():
    for widget in main.winfo_children():
        widget.destroy()
    createMenus()
    oneTTest(main)
def twoSampTTest():
    print('two sample T test here')


def twoDimensional():
    print('2d graphing here')
def threeDimensional():
    print('2d graphing here')
def scatterplot():
    print('Scatterplot here')
def histogram():
    print('histogram here')
def lineGraphing():
    print('Line graphing')
def pieCharts():
    print('Pit charts here')
#will need classes for buttons
def createMenus():
    menu = Menu(main)
    main.config(menu=menu)
    #Stats Menu
    statsMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Statistics', menu=statsMenu)
    statsMenu.add_command(label='Z-Test', command=zTest)
    statsMenu.add_command(label='One Sample T-Test', command=oneSampTTest)
    statsMenu.add_command(label='Two Sample T-Test', command=twoSampTTest)
    statsMenu.add_separator()
    # Graphing Menu
    graphMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Graphing', menu=graphMenu)
    graphMenu.add_command(label='2D Graphing', command=twoDimensional)
    graphMenu.add_command(label='3D Graphing', command=threeDimensional)
    graphMenu.add_separator()
    graphMenu.add_command(label='Scatterplot', command=scatterplot)
    graphMenu.add_command(label='Histogram', command=histogram)
    graphMenu.add_command(label='Line Graph', command=lineGraphing)
    graphMenu.add_command(label='Pie Graph', command=pieCharts)

#Perhaps Another menu

createMenus()
mainFrame = Frame(main)
mainFrame.pack()

introduction = Label(mainFrame, text="Welcome to BLAHHH",bd=1)
introduction.config(font=("Courier", 44))
introduction.pack(side=TOP, fill=X, expand=1)
#Embedding Original Graph, code from MATLIB Original Sight
fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(-3, 3, .01)
fig.add_subplot(133).plot(t, (1/(np.sqrt(2*np.pi)))*np.e**(-(t**2)/2))
fig.add_subplot(131).plot(t, t+np.sin(t)**2)
fig.add_subplot(132).plot(t, t**2+np.sin(t)-2*t)
#figure out o get a random plot
canvas = FigureCanvasTkAgg(fig, master=mainFrame)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

#Don't update toolbar yet, that's for second part
# toolbar = NavigationToolbar2Tk(canvas, main)
# toolbar.update()
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)


# savefig('../figures/grid_ex.png',dpi=48)

#Need first screen to just be a basic explanation of everything
#For statistics, give graph (ex show normal dist and the z-distribution stuffs, learn how to show area)
#Have option to find data from CSV file, which they can input, but they still need to input test statistic and whatever
#For other stuff figure that shit out

main.mainloop()