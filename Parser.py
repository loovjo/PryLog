
# Notes:
#   Undefined variables are assigned to _
#   Variables: Normal [A-Za-z0-9_], surround with ''s to extend to full Unicode

class ParseElement:
    def getChildren(self):
        return []

class ElementAtom(ParseElement):
    def __init__(self, text):
        self.text = text
    def getChildren(self):
        return []
    def __str__(self):
        return "'" + self.text + "'"
class ElementLogicalSymbol(ParseElement):
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return "( " + self.type + " )"
class ElementContainer(ParseElement):
    def __init__(self, children):
        self.children = children
    def getChildren(self):
        return self.children
    def __str__(self):
        return "[ " + ", ".join(self.children) + " ]"

def tokenize(code):
    res = []
    return res


# print(ElementLogicalSymbol(":-"))
