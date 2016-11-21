# Notes:
#   Undefined variables are assigned to _
#   Variables: Normal [A-Za-z0-9_], surround with ''s to extend to full Unicode

import re

class ParseElement:
    def getChildren(self):
        return []

class ElementAtom(ParseElement):
    def __init__(self, text):
        self.text = text
    def getChildren(self):
        return []
    def __str__(self):
        return self.text
class ElementVariable(ParseElement):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "'" + self.name + "'"
class ElementContainer(ParseElement):
    def __init__(self, children):
        self.children = children
    def getChildren(self):
        return self.children
    def __str__(self):
        return "[ " + ", ".join(self.children) + " ]"

PAIRS = [":-"]

PATTERN_ALPHANUMERIC = "[\\w\\d_]"

def matches(regex, st):
    return re.search(regex, st) != None

def tokenize(code):
    res = []
    last = code[0]
    current = ""
    for ch in code:
        if ch == " ":
            continue
        if (not matches(PATTERN_ALPHANUMERIC, ch) or not matches(PATTERN_ALPHANUMERIC, last)) and last + ch not in PAIRS:
            res += [current]
            current = ch
        else:
            current += ch
        last = ch
    return res + [current]

