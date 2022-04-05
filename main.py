class Literal:
    # letterale
    def __init__(self, lit, negative=False):
        self.is_negate = negative
        if self.is_negate:
            self.lit = 'neg' + str(lit)
        else:
            self.lit = lit

    def setTruthValue(self, value):
        self.truthValue = bool(value)

    def __eq__(self, cmp):
        return self.lit == cmp.lit


class Sentence:
    # sentenza
    def __init__(self, premises, consequences, name):
        self.premises = []
        self.consequences = []
        self.numOfSymbols = 0
        for premise in premises:
            self.premises.append(premise)
            self.numOfSymbols += 1
        for consequence in consequences:
            self.consequences.append(consequence)
        self.name = name


class KnowledgeBase:
    def __init__(self, listOfSymbols=[], listOfRules=[]):
        self.listOfSymbols = []
        self.listOfRules = []
        for symbol in listOfSymbols:
            self.listOfSymbols.append(symbol)
        for rule in listOfRules:
            self.listOfRules.append(rule)


def FCEntails(kb, q, order = []):
    count = {}
    inferred = {}
    queue = []

    for symbol in kb.listOfSymbols:
        inferred[symbol.lit] = False

    for rule in kb.listOfRules:
        count[rule.name] = rule.numOfSymbols

    for symbol in kb.listOfSymbols:
        if hasattr(symbol, 'truthValue') and symbol.truthValue :
            queue.append(symbol)

    while len(queue) != 0:
        s = queue.pop()
        #print(s.lit)
        order.append(s.lit)
        if s == q:
            return True
        if not inferred[s.lit]:
            inferred[s.lit] = True
            for r in kb.listOfRules:
                for p in r.premises:
                    if s.lit == p.lit:
                        count[r.name] -= 1
                        if count[r.name] == 0:
                            for c in r.consequences:
                                c.truthValue = True
                                queue.append(c)
    return False


def BCEntailment(kb, q, orderList=[]):
    count = {}
    inferred = {}

    for symbol in kb.listOfSymbols:
        inferred[symbol.lit] = False

    for rule in kb.listOfRules:
        count[rule.name] = rule.numOfSymbols

    return BCEntails(kb, q, inferred, count, orderList)


def BCEntails(kb, q, inferred=[], count=[], orderList=[]):
    if inferred[q.lit]:
        return True
    #print(q.lit)
    if hasattr(q, 'truthValue') and q.truthValue:
        orderList.append(q.lit)
        return True
    for r in kb.listOfRules:
        for c in r.consequences:
            if q == c:
                sum = 0
                for p in r.premises:
                    result = BCEntails(kb, p, inferred, count, orderlist)
                    if result:
                        sum=sum+1
                if sum == r.numOfSymbols:
                    q.truthValue = True
                    return True
    return False

print("First test: ")
nB11 = Literal("B(1,1)", True)
nB11.setTruthValue(True)
nP12 = Literal("P(1,2)", True)
nP21 = Literal("P(2,1)", True)
nP12 = Literal("P(1,2)", True)

R1 = Sentence([nB11], [nP12], "R1")
R2 = Sentence([nB11], [nP21], "R2")
symbols = [nB11, nP12, nP21]
rules = [R1, R2]
KB = KnowledgeBase(symbols, rules)

orderlist = []
result = FCEntails(KB, nP12, orderlist)
print("FC results: ", result)
print("The order of analyzed symbols in FC is the following: ", orderlist)

nP12.setTruthValue(False)
orderlist = []
result2 = BCEntailment(KB, nP12, orderlist)
print("BC results: ", result2)
print("The order of analyzed symbols in BC is the following: ", orderlist)

print("\nSecond test: ")
nB11 = Literal("B(1,1)", True)
nB11.setTruthValue(True)
nP12 = Literal("P(1,2)", True)
nP21 = Literal("P(2,1)", True)
P12 = Literal("P(1,2)")
R1 = Sentence([nB11], [nP12], "R1")
R2 = Sentence([nB11], [nP21], "R2")
symbols = [nB11, nP12, nP21, P12]
rules = [R1, R2]
KB = KnowledgeBase(symbols, rules)

orderlist = []
result = FCEntails(KB, P12, orderlist)
print("FC results: ", result)
print("The order of analyzed symbols in FC is the following: ", orderlist)

orderlist = []
result2 = BCEntailment(KB, P12, orderlist)
print("BC results: ", result2)
print("The order of analyzed symbols in BC is the following: ", orderlist)

print("\nThird test: ")
nS12 = Literal("S(1,2)", True)
nS12.setTruthValue(True)
S21 = Literal("S(2,1)")
S21.setTruthValue(True)
nW22 = Literal("W(2,2)", True)
W31 = Literal("W(3,1)")
nW31 = Literal("W(3,1)", True)

R1 = Sentence([nS12, S21], [nW22], "R1")
R2 = Sentence([S21, nW22], [W31], "R2")
symbols = [nS12, S21, nW22, W31, nW31]
rules = [R1, R2]
KB = KnowledgeBase(symbols, rules)

orderlist = []
result = FCEntails(KB, W31, orderlist)
print("FC results: ", result)
print("The order of analyzed symbols in FC is the following: ", orderlist)

W31.setTruthValue(False)
orderlist = []
result2 = BCEntailment(KB, W31, orderlist)
print("BC results: ", result2)
print("The order of analyzed symbols in BC is the following: ", orderlist)


print("\nFourth test: ")
nS12 = Literal("S(1,2)", True)
nS12.setTruthValue(True)
S21 = Literal("S(2,1)")
S21.setTruthValue(True)
nW22 = Literal("W(2,2)", True)
W31 = Literal("W(3,1)")
nW31 = Literal("W(3,1)", True)

R1 = Sentence([nS12, S21], [nW22], "R1")
R2 = Sentence([S21, nW22], [W31], "R2")
symbols = [nS12, S21, nW22, W31, nW31]
rules = [R1, R2]
KB = KnowledgeBase(symbols, rules)

orderlist = []
result = FCEntails(KB, nW31, orderlist)
print("FC results: ", result)
print("The order of analyzed symbols in FC is the following: ", orderlist)

W31.setTruthValue(False)
orderlist = []
result2 = BCEntailment(KB, nW31, orderlist)
print("BC results: ", result2)
print("The order of analyzed symbols in BC is the following: ", orderlist)


