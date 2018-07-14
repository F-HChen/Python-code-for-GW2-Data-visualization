'''
Python Script to show pie chart and stack bar-chart of Guild Wars 2 Unidientified Gear.
Displays unopened ratio of rarity, opened ratio of gear rarity, and sell price difference
between the merchant and the Black Lion Market.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, AnnotationBbox)
from matplotlib.widgets import TextBox

df = pd.read_csv('GW2 Pieces of UG stats - Sheet2.csv')

#Print column names
for i in df:
    print(i)

#Creates a pie chart of different rarity(shows percentange and count of each type)
def ratioChart(rarity, count):
    fig, ax = plt.subplots(figsize=(6,3), subplot_kw=dict(aspect="equal"))
    
    items = rarity
    data = count

    def func(pct, allvals):
        absolute = int(np.rint(pct/100.*np.sum(allvals)))
        return "{:.1f}%\n({:d} items)".format(pct, absolute)

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="black"),
                                      #change color to match given information
                                      colors=['green', 'yellow', 'orange'])

    ax.legend(wedges, items, title="Rarity", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    #set title
    ax.set_title("Rarity Porportion of Yellow Unidentified Gear")

    plt.show()

#ratioChart(df["Rarity"], df["Count"])

#Function to return the sum of copper
def singleValue(gold, silver, copper):
    g = np.sum(gold)
    s = np.sum(silver)
    c = np.sum(copper)

    tCopper = np.sum((g*10000) + (s*100) + c)
    return tCopper

#Function to return index position
def posRarity(color, rarityC):

    pList = rarityC.index[rarityC == color].tolist()

    return(pList)

#Function to plot stack bar charts for given input
def valueSellItems(rarity, Mgold, Msilver, Mcopper, Bgold, Bsilver, Bcopper):
    uRarity = rarity
    uMGold = Mgold
    uMSilver = Msilver
    uMCopper = Mcopper
    uBGold = Bgold
    uBSilver = Bsilver
    uBCopper = Bcopper
    width = 0.5

    def rarityMPos(color, uRarity):
        
        tMCopper = singleValue(uMGold[posRarity(color, uRarity)],
                              uMSilver[posRarity(color, uRarity)],
                              uMCopper[posRarity(color, uRarity)])
        return int(tMCopper)

    def rarityBPos(color, uRarity):
        tBCopper = singleValue(uBGold[posRarity(color, uRarity)],
                              uBSilver[posRarity(color, uRarity)],
                              uBCopper[posRarity(color, uRarity)])
        return int(tBCopper)

    cBlue = rarityMPos("Blue", uRarity)
    cGreen = rarityMPos("Green", uRarity)
    cYellow = rarityMPos("Yellow", uRarity)
    
    blueM = plt.bar(1, cBlue, width, color="blue")
    greenM = plt.bar(1, cGreen, width,
                     bottom=cBlue, color="green")
    yellowM = plt.bar(1, cYellow, width,
                      bottom=(cBlue + cGreen),
                      color="yellow")

    sBlue = rarityBPos("Blue", uRarity)
    sGreen = rarityBPos("Green", uRarity)
    sYellow = rarityBPos("Yellow", uRarity)

    blueB = plt.bar(2, sBlue, width, color="blue")
    greenB = plt.bar(2, sGreen, width,
                     bottom=sBlue, color="green")
    yellowB = plt.bar(2, sYellow, width,
                      bottom=(sBlue + sGreen),
                      color="yellow")

    tM = np.sum(cBlue+cGreen+cYellow)
    tB = np.sum(sBlue+sGreen+sYellow)

    plt.ylabel("Copper")
    plt.title("Sell Price of Unidentified Gear (Merchant vs. Black Lion Market)")
    plt.xticks((1, 2), ("Merchant", "Market"))
    plt.legend((blueM, greenM, yellowM),('Common', 'Uncommon', 'Rare'))
    plt.text(1.2,400000,"{0:.1%}".format(((tB - tM)/tB)) + " difference")

    plt.show()

#Call function to create stack bar-chart of unopened unidentified gear(Merchant vs. Market)
'''    
valueSellItems(df["Rarity"], df["Merchant-Gold"], df["Merchant-Silver"],
    df["Merchant-Copper"], df["Market-Gold"], df["Market-Silver"], df["Market-Copper"])
'''

#variables to hold columns without nan cells
bRar = df["Yellow-Rarity"].dropna()
bCon = df["Yellow-Count"].dropna()

#Function to sum total rarity
def rCount(rarity, bRar, bCon):
    rarPos = posRarity(rarity, bRar)
    rarCount = 0
    for i in rarPos:
        rarCount = rarCount + bCon[i]

    return rarCount

#Function to create dataframe with count of unique variables in rarity
def crePDF(bRar, bCon):
    rarity = bRar.unique()
    tempPD = pd.DataFrame(columns = ["Rarity", "Count"])
    tempPD["Rarity"] = rarity
    i = 0
    for r in rarity:
        tempPD["Count"].iloc[i] = rCount(r, bRar, bCon)
        i += 1
        
    return tempPD

#pandas dataframe of both rarity and count
mDF = crePDF(bRar, bCon)

#ratioChart(mDF["Rarity"], mDF["Count"])

#Function to return the sum of copper
def singleTValue(silver, copper):
    s = np.sum(silver)
    c = np.sum(copper)

    tCopper = np.sum((s*100) + c)
    return tCopper

#Function to return index position 
def posRar(color, rarityC):

    pList = rarityC.index[rarityC == color].tolist()

    return pList

#Function to plot stack bar charts for given input
def valueSellId(rarity, Msilver, Mcopper, Bsilver, Bcopper):
    uRarity = rarity
    uMSilver = Msilver
    uMCopper = Mcopper
    uBSilver = Bsilver
    uBCopper = Bcopper
    width = 0.5

    def rarityMPos(color, uRarity):

        posList = posRar(color, uRarity)
        tMCopper = 0
        for i in posList:
            tMC = singleTValue(uMSilver[i], uMCopper[i])

            tMCopper += tMC
            
        return int(tMCopper)

    def rarityBPos(color, uRarity):

        posList = posRar(color, uRarity)
        tBCopper = 0
        for i in posList:
            tBC = singleTValue(uBSilver[i], uBCopper[i])

            tBCopper += tBC
            
        return int(tBCopper)

    cBnG = rarityMPos("G/B", uRarity)
    cYellow = rarityMPos("Y", uRarity)
    cOrange = rarityMPos("O", uRarity)

    bngM = plt.bar(1, cBnG, width, color="blue")
    yellowM = plt.bar(1, cYellow, width,
                     bottom=cBnG, color="yellow")
    orangeM = plt.bar(1, cOrange, width,
                      bottom=(cBnG + cYellow),
                      color="orange")

    sBnG = rarityBPos("G/B", uRarity)
    sYellow = rarityBPos("Y", uRarity)
    sOrange = rarityBPos("O", uRarity)

    bngB = plt.bar(2, sBnG, width, color="blue")
    yellowB = plt.bar(2, sYellow, width,
                     bottom=sBnG, color="yellow")
    orangeB = plt.bar(2, sOrange, width,
                      bottom=(sBnG + sYellow),
                      color="orange")

    tM = np.sum(cBnG+cYellow+cOrange)
    tB = np.sum(sBnG+sYellow+sOrange)

    plt.ylabel("Copper")
    #Title needs to be manually changed
    plt.title("Sell Price of Yellow-Unidentified Gear (Merchant vs. Black Lion Market)")
    plt.xticks((1, 2), ("Merchant", "Market"))
    plt.legend((bngM, yellowM, orangeM),('C/UnC', 'Rare', 'Exotic'))
    #Displays percentage difference between selling to the merchant
    #and selling on the Black Lion Market
    #(first variable changes horizontal position, second changes vertical position)
    plt.text(1.4,150000,"{0:.1%}".format(((tB - tM)/tB)) + " difference")

    plt.show()

'''
#Returns stacked bar chart for sell value of Bleue Unidentified Gear(Common)
valueSellId(df["Blue-Rarity"], df["BMerchant-Silver"], df["BMerchant-Copper"],
            df["BMarket-Silver"], df["BMarket-Copper"])

#Returns stacked bar chart for sell value of Green Unidentified Gear(Uncommon)
valueSellId(df["Green-Rarity"], df["GMerchant-Silver"], df["GMerchant-Copper"],
            df["GMarket-Silver"], df["GMarket-Copper"])

#Returns stacked bar chart for sell value of Yellow Unidentified Gear(Rare)
valueSellId(df["Yellow-Rarity"], df["YMerchant-Silver"], df["YMerchant-Copper"],
            df["YMarket-Silver"], df["YMarket-Copper"])

'''
