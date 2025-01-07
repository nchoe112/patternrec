import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker 
import matplotlib.dates as mdates 
import numpy as np 
from datetime import datetime
from functools import reduce
import time 

totalStart = time.time()

#date parser using strptime 
def strpdate2num(date_str):
    return mdates.date2num(datetime.strptime(date_str, '%Y%m%d%H%M%S'))

def percentChange(startPoint, currentPoint):
    try:
        x = (float(currentPoint)-startPoint)/abs(startPoint)*100.00
        if x == 0.0:
            return 0.0000000000001
        else:
            return x
    except:
        return 0.0000000001
date,bid,ask = np.loadtxt('GBPUSD1d.txt',unpack=True,
                            delimiter=',',
                            converters={0: lambda s: strpdate2num(s)})

#function uses percent change makes patterns 
def patternStorage():
    patStartTime = time.time() 


    #look n number of digits into the future and average to mark the change 
    x = len(avgLine)-60 
    #starting point 
    y = 31 
    while y < x:
        pattern = []
        for i in range(29, -1, -1):
            pattern.append(percentChange(avgLine[y-30], avgLine[y-i]))

        outcomeRange = avgLine[y+20:y+30]
        currentPoint = avgLine[y]

        try:
            #for every x and y add them together and then divide by length of outcome range 
            avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
        except Exception as e:
            print(str(e))
            avgOutcome = 0 
        
        futureOutcome = percentChange(currentPoint, avgOutcome)

        patternAr.append(pattern)
        performanceAr.append(futureOutcome)

        #print(currentPoint)
        #print('____')
        #print(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10)

        y += 1 
    
    patEndTime = time.time()
    print(len(patternAr))
    print(len(performanceAr))
    print('Pattern storage took:', patEndTime-patStartTime, 'seconds')

def currentPattern():

    for i in range(30, 0, -1):
        cp = percentChange(avgLine[-31], avgLine[-i])
        patForRec.append(cp)


    print(patForRec)

def patternRecognition():
    predictedOutcomesAr = []
    patFound = 0
    plotPatAr = [] 

    for eachPattern in patternAr:
        #compare each step of the pattern for recent pattern and all previous patterns      
        similarities = []

        for i in range(30):
            sim = 100.00 - abs(percentChange(eachPattern[i], patForRec[i]))
            similarities.append(sim)

        howSim = sum(similarities) / 30.00

        if howSim > 70:
            patdex = patternAr.index(eachPattern)

            #pattern found is true 
            patFound = 1

            '''print("------------")
            print(patForRec)
            print("************")
            print(eachPattern)
            print("predicted outcome", performanceAr[patdex])'''



            xp = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
            plotPatAr.append(eachPattern)

    predArray = []

    if patFound == 1:
        #fig = plt.figure(figsize=(10,6))

        for eachPatt in plotPatAr:
            futurePoints = patternAr.index(eachPatt)

            if performanceAr[futurePoints]>patForRec[29]:
                pcolor = '#24bc00'
                #prediction is pos
                predArray.append(1.000)
            else:
                pcolor = '#d40000'
                predArray.append(-1.000)

            plt.plot(xp,eachPatt)
            predictedOutcomesAr.append(performanceAr[futurePoints])
            plt.scatter(35, performanceAr[futurePoints], c=pcolor, alpha=.3)

        realOutcomeRange = allData[toWhat+20:toWhat+30]
        realAvgOutcome = reduce(lambda x, y: x+y, realOutcomeRange) / len(realOutcomeRange)
        realMovement = percentChange(allData[toWhat],realAvgOutcome)
        predictedAvgOutcome = reduce(lambda x, y: x+y, predictedOutcomesAr) / len(predictedOutcomesAr)
        
        #BACKTESTING
        print(predArray)
        #average of all predictions
        predictionAverage = reduce(lambda x, y: x+y, predArray) / len(predArray)

        print(predictionAverage)


        if predictionAverage < 0:
            print('drop predicted')
            #print last point
            print(patForRec[29])
            print(realMovement)
            if realMovement < patForRec[29]:
                accuracyArray.append(100)
            else:
                accuracyArray.append(0)
        if predictionAverage > 0:
            print('rise predicted')
            #print last point
            print(patForRec[29])
            print(realMovement)
            if realMovement > patForRec[29]:
                accuracyArray.append(100)
            else:
                accuracyArray.append(0)

        
        plt.scatter(40,realMovement,c='#54fff7', s=25)
        plt.scatter(40,predictedAvgOutcome,c='b',s=25)

        #original line
        plt.plot(xp, patForRec, '#54fff7', linewidth = 3)
        plt.grid(True)
        plt.title('Pattern Recognition')
        plt.show(block=True)

#numpy opens up text file 
def graphRawFX():
    fig = plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40),(0,0), rowspan=40, colspan=40)

    ax1.plot(date,bid)
    ax1.plot(date,ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date,0,(ask-bid), facecolor='g', alpha=.3)

    
    plt.subplots_adjust(bottom=.23)

    #plt.grid(True)
    plt.show()

dataLength = int(bid.shape[0])
print('data length is', dataLength)

#data to start with 
toWhat = 37000
allData = ((bid+ask)/2)

accuracyArray = []
samps = 0


while toWhat < dataLength:
    #by averaging bid and ask not considering spread 
    #avgLine = ((bid+ask)/2)
    #need data to update real time everything before toWhat is past 
    avgLine = allData[:toWhat]

    patternAr = []
    performanceAr = []
    patForRec = []

    #graphRawFX()
    patternStorage()
    currentPattern()
    patternRecognition()
    totalTime= time.time()-totalStart
    print("entire processing time took: ", totalTime)
    #moveOn = input('Press ENTER to continue...')
    samps+=1
    toWhat += 1
    accuracyAverage = reduce(lambda x, y: x+y, accuracyArray) / len(accuracyArray)
    print('Backtested Accuracy is', str(accuracyAverage)+ '% after', samps,'samples')



