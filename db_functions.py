import sqlite3
from pokemontcgsdk import Card
from pokemontcgsdk import Set

con = sqlite3.connect("pokehand.db")
con.row_factory = sqlite3.Row
 

def insertSet(set):
    #id, code, name
    cur = con.cursor()
    sql = "INSERT INTO SETS(id,code,name) VALUES(?,?,?)"
    setValues = [
        set.id,
        set.ptcgoCode,
        set.name
    ]
    cur.execute(sql,setValues)
    con.commit()
    return cur.lastrowid

def findSetForCode(code):
    cur = con.cursor()
    sql = "SELECT id FROM SETS WHERE code = '%s'" % code
    res = cur.execute(sql).fetchone()
    
    if(res and len(res) > 0):
        return cur.execute(sql).fetchone()[0]
    
    return None

def findCardBySetIdAndNum(setId, num):
    cur = con.cursor()
    sql = "select * from CARDS where set_id = '" + setId + "' and number = " + num
    res = cur.execute(sql).fetchone()
    
    if(res and len(res) > 0):
        return res
    
    return None

def findCardByNameAndNum(name, num):
    cur = con.cursor()
    sql = "select * from CARDS where name = '" + name + "' and number = " + num
    res = cur.execute(sql).fetchone()
    
    if(res and len(res) > 0):
        return res
    
    return None


def insertCard(card):
    cur = con.cursor()
    sql = "INSERT INTO CARDS(id, name, types, supertype, subtypes, set_id, number) values(?,?,?,?,?,?,?)"
    cardValue = [
        card.id,
        card.name,
        ",".join(card.types) if card.types and len(card.types) > 0 else "",
        card.supertype,
        ",".join(card.subtypes) if card.subtypes and len(card.subtypes) > 0 else "",
        card.set.id,
        card.number
    ]
    cur.execute(sql,cardValue)
    con.commit()
    return cur.lastrowid


def getDeckByName(name):
    cur = con.cursor()
    sql = "SELECT * from DECKS where name = '" + name + "'"
    res = cur.execute(sql).fetchone()
    
    if(res and len(res) > 0):
        return res
    
    return None

def insertDeck(name):
    cur = con.cursor()
    sql = "INSERT INTO DECKS(name) values(?)"
    deckValues = [
        name
    ]
    
    cur.execute(sql,deckValues)
    con.commit()
    return getDeckByName(name)

def insertCardIntoDeck(deckId, cardId, quantity):
    cur = con.cursor()
    sql = "INSERT OR IGNORE INTO CARD_DECKS(deck_id, card_id, quantity) values(?,?,?)"
    cardDeckValues = [
        deckId,
        cardId,
        quantity
    ]
    
    cur.execute(sql, cardDeckValues)
    con.commit()
    return cur.lastrowid

def getCardDeckByDeckId(deckId):
    cur = con.cursor()
    sql = "SELECT CARD_DECKS.deck_id, CARD_DECKS.quantity, CARDS.* FROM CARD_DECKS JOIN CARDS on CARDS.id = CARD_DECKS.card_id where CARD_DECKS.deck_id = ?"
    cardDeckValue = [
        deckId
    ]
    res = cur.execute(sql, cardDeckValue).fetchall()
    
    if(res and len(res) > 0):
        return res
    
    return None