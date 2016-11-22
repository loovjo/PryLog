# Notes:
#   Undefined variables are assigned to _
#   Variables: Normal [A-Za-z0-9_], surround with ''s to extend to full Unicode

import re, string

class ParseElement:
    def getChildren(self):
        return []

class ElementAtom(ParseElement):
    def __init__(self, text):
        self.text = text
    def getChildren(self):
        return []
    def __repr__(self):
        return self.text
    def __str__(self):
        return "ElementAtom('%s')" % self.text
    def pretty(self):
        return "'%s'" % self.text
    def __eq__(self, other):
        if isinstance(other, ElementAtom):
            return self.text == other.text
        return False
class ElementVariable(ParseElement):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "ElementVariable('%s')" % self.name
    __repr__ = __str__
    def pretty(self):
        return "%s" % self.name
    def __eq__(self, other):
        if isinstance(other, ElementVariable):
            return self.name == other.name
        return False
class ElementContainer(ParseElement):
    def __init__(self, children, text=""):
        self.children = children
        self.text = text
    def getChildren(self):
        return self.children
    def __str__(self):
        return "ElementContainer([%s]])" % ", ".join(map(str, self.children))
    __repr__ = __str__
    def pretty(self):
        lines = ["Container( '%s'" % " ".join(self.text)]
        for j, ch in enumerate(self.children):
            lines.extend(["\t" + line for line in ch.pretty().split("\n")])
            lines[-1] += ","
        lines.append(")")
        return "\n".join(lines)
    def __eq__(self, other):
        if isinstance(other, ElementContainer):
            return self.children == other.children
        return False

PAIRS = [":-"]

PATTERN_ALPHANUMERIC = "[\\w\\d_]"

def matches(regex, st):
    res = re.search(regex, st)
    return res != None and res.span() == (0, len(st))

def tokenize(code):
    res = []
    last = code[0]
    current = ""
    for ch in code:
        if ch == " ":
            continue
        if (not matches(PATTERN_ALPHANUMERIC, ch) or not matches(PATTERN_ALPHANUMERIC, last)) and last + ch not in PAIRS and len(current) > 0:
            res += [current]
            current = ch
        else:
            current += ch
        last = ch
    return res + [current]

SYMBOL_PRIORITY = [
        ".",
        ":-",
        ","
]
OPEN_PARENS = "([{"
CLOSE_PARENS = ")]}"

def parse(code):
    if len(code) == 0:
        return ElementAtom("__NONE__")
    if len(code) == 1 or type(code) == str:
        first = code if type(code) == str else code[0]
        if first[0] in string.ascii_uppercase:
            return ElementVariable(first)
        return ElementAtom(first)
    if any(map(lambda x: x in OPEN_PARENS or x in CLOSE_PARENS, code)):
        firstParen = list(map(lambda x: x in OPEN_PARENS or x in CLOSE_PARENS, code)).index(True)
        depth = 0
        index = 0
        for i in range(firstParen, len(code)):
            if code[i] in OPEN_PARENS:
                depth += 1
            elif code[i] in CLOSE_PARENS:
                depth -= 1
            if depth == 0:
                index = i
                break
        before = code[:firstParen]
        inside_parens = code[firstParen : index + 1]
        after = code[index + 1:]
        if before == after == []:
            return ElementContainer([ElementAtom(inside_parens[0]), parse(inside_parens[1:-1]), ElementAtom(inside_parens[-1])], code)
        if before:
            parsedBeforeLast = parse(before[-1])
            if isinstance(parsedBeforeLast, ElementAtom) or isinstance(parsedBeforeLast, ElementVariable):
                if after:
                    if len(before) > 1:
                        return ElementContainer([parse(before[:-1]), parsedBeforeLast, parse(inside_parens), parse(after)], code)
                    return ElementContainer([parsedBeforeLast, parse(inside_parens), parse(after)], code)
                if len(before) > 1:
                    return ElementContainer([parse(before[:-1]), parsedBeforeLast, parse(inside_parens)], code)
                return ElementContainer([parsedBeforeLast, parse(inside_parens)], code)

            if after:
                return ElementContainer([parse(before), parse(inside_parens), parse(after)], code)
            return ElementContainer([parse(before), parse(inside_parens)], code)
        if after:
            return ElementContainer([parse(inside_parens), parse(after)], code)
    if any(map(lambda x: x in SYMBOL_PRIORITY, code)):
        highestPrio = sorted(zip(code, range(len(code))), key=lambda x: SYMBOL_PRIORITY.index(x[0]) if x[0] in SYMBOL_PRIORITY else len(SYMBOL_PRIORITY))[0]
        before = code[:highestPrio[1]]
        after = code[highestPrio[1] + 1:]
        if before:
            if after:
                return ElementContainer([parse(before), parse(highestPrio[0]), parse(after)], code)
            return ElementContainer([parse(before), parse(highestPrio[0])], code)
        if after:
            return ElementContainer([parse(highestPrio[0]), parse(after)], code)
        return ElementContainer([parse(highestPrio[0])], code)
    return ElementContainer(list(map(parse, code)), code)

