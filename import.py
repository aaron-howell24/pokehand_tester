import sys
import os
import re
import jsonpickle
from dotenv import load_dotenv
from pathlib import Path

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient


load_dotenv()

RestClient.configure(os.getenv('POKEMONTCG_IO_API_KEY')) 

# 1. Take filename input
# 2. Parse txt file
#       2.1. Make an array of cards that include
#               - Amount in Deck
#               - Name
#               - Set Code
#               - Set Num
# 3. Get all set ptcgo codes in a map
# 4. Hit API for Set IDs and put into map
# 5. For each card in array call API to get card details
# 6. Using card details build text file to copy paste into decks.py

def getSetIdForCode(code):
    sets = Set.where(q='ptcgoCode:"'+code+'"')
    if "swsh12pt5gg" in sets[0].id or "swsh11tg" in sets[0].id:
        return sets[1]
    else:
        return sets[0]

def getCardForSetIdAndSetNum(setId, setNum):
    print("setID: (" + setId + ") setNum: ("+setNum+")")
    cards = Card.where(q='set.id:'+setId+' number:'+setNum)
    return cards[0]

def getEnergyCardByNameAndNumber(name, setNum):
    print("Name: " + name + " setNum: " + setNum)
    cards = Card.where(q='name:"' + name + '" number:'+setNum)
    return cards[0]

filename = sys.argv[1]

inputFile = open(filename, "r")

inputLines = inputFile.readlines()
inputFile.close()

inputCards = []
sets = {}

outputDeck = []

numCardsRegPattern = r'^[^\d]*(\d+)'
cardNameRegPattern = r'(?![0-9]+)(?! )(.*)(?= [A-Z]{3})'
setPTCGOCodePattern = r'(?! )[A-Z]{3}(?= [0-9])'
cardSetNumberPattern = r'(\d+)(?!.*\d)'

basicEnergyPattern = r'(?![0-9]+ )Basic\ .+Energy'

for line in inputLines:
    if "Pokemon - " in line or "Trainer - " in line or "Energy - " in line:
        continue
    
    
    print(line)
    numOfCards = re.findall(numCardsRegPattern, line)[0]
    cardName = ""
    setPTCGOCode = ""
    cardSetNum = re.findall(cardSetNumberPattern, line)[0]
    
    card = []
    
    if not re.findall(basicEnergyPattern, line):
        cardName = re.findall(cardNameRegPattern, line)[0]
        setPTCGOCode = re.findall(setPTCGOCodePattern, line)[0]
        print("Name: " + cardName + ", Code: " + setPTCGOCode + ", setNum: " + cardSetNum)

        if setPTCGOCode not in sets:
            sets[setPTCGOCode] = getSetIdForCode(setPTCGOCode).id

        card = getCardForSetIdAndSetNum(sets[setPTCGOCode], cardSetNum)
    else:
        cardName = re.findall(basicEnergyPattern, line)[0]
        card = getEnergyCardByNameAndNumber(cardName, cardSetNum)
    
    for num in range(int(numOfCards)):
        outputDeck.append(card)
        
               
with open(Path(filename).stem+"_output.txt","w") as outputFile:
    for line in outputDeck:
        outputFile.write(jsonpickle.encode(line) + "\n") # works with any number of elements in a line

