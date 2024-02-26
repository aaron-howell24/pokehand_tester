import sys
import random
import jsonpickle
import json
import xlsxwriter
from pathlib import Path
from db_functions import *
from datetime import datetime

def generateHand(deck):
    hand = []
    i = 0
    for i in range(7):
        hand.append(deck.pop())
    return hand

def generatePrizeCards(deck):
    prizeCards = []
    i = 0
    for i in range(6):
        prizeCards.append(deck.pop())
    return prizeCards

def doesHandContainBasicPokemon(hand):
    for card in hand:
        if  "Basic" in card["subtypes"].split(","):
            return True
    return False

def readableCard(card):
    output = {}
    output["name"] = card["name"]
    output["id"] = card["id"]
    output["subtypes"] = card["subtypes"]
    output["supertype"] = card["supertype"]
    return output

# Get deck from text file and unpickle it
unshuffledDeck = []
deckfileName = sys.argv[1]

deckObj = getDeckByName(deckfileName)

for cardDeck in getCardDeckByDeckId(deckObj['id']):
    for quantity in range(int(cardDeck['quantity'])):
        unshuffledDeck.append(cardDeck)

numIterations = sys.argv[2]

workbook = xlsxwriter.Workbook(Path(deckfileName).stem+'_'+numIterations+'_'+datetime.now().strftime("%d-%m-%Y")+'.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0,0,"Hand 1")
worksheet.write(0,1,"Hand 2")
worksheet.write(0,2,"Hand 3")
worksheet.write(0,3,"Hand 4")
worksheet.write(0,4,"Hand 5")
worksheet.write(0,5,"Hand 6")
worksheet.write(0,6,"Hand 7")
worksheet.write(0,7,"First Draw")
worksheet.write(0,8,"Mulligan Count")
worksheet.write(0,9,"Prize Card 1")
worksheet.write(0,10,"Prize Card 2")
worksheet.write(0,11,"Prize Card 3")
worksheet.write(0,12,"Prize Card 4")
worksheet.write(0,13,"Prize Card 5")
worksheet.write(0,14,"Prize Card 6")

for iterationNum in range(int(numIterations)):
    mulliganCount = 0
    deck = random.sample(unshuffledDeck, len(unshuffledDeck))
    prizeCards = []
    
    hand = generateHand(deck)
    
    while(not doesHandContainBasicPokemon(hand)):
        mulliganCount += 1
        hand = generateHand(deck)
        
    prizeCards = generatePrizeCards(deck)
    
    colNum = 0
    for card in hand:
        worksheet.write(iterationNum+1, colNum, json.dumps(readableCard(card)))
        colNum+=1
    
    
    worksheet.write(iterationNum+1, colNum,json.dumps(readableCard(deck.pop())))
    colNum+=1
    worksheet.write(iterationNum+1, colNum,mulliganCount)
    colNum+=1
    
    for card in prizeCards:
        worksheet.write(iterationNum+1, colNum,json.dumps(readableCard(card)))
        colNum+=1
    
    
workbook.close() 
