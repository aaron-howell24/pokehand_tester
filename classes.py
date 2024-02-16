class Card(object):
    name = ""
    id = ""
    supertype = ""
    subtypes = []
    setId = ""
    number = ""
    regulationMark = ""
    
    def __init__(self, id, name, supertype, subtypes, setId, number, regulationMark):
        self.name = name
        self.id = id
        self.supertype = supertype
        self.subtypes = subtypes
        self.setId = setId
        self.number = number
        self.regulationMark = regulationMark
    
    
class Set(object):
    id = ""
    name = ""
    ptcgoCode = ""
    legalities = []
    
    
    