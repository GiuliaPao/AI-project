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


def FCEntails(kb, q):
    count = {}
    inferred = {}
    queue = []
    order = []

    for symbol in kb.listOfSymbols:
        inferred[symbol.lit] = False

    for rule in kb.listOfRules:
        count[rule.name] = rule.numOfSymbols

    for symbol in kb.listOfSymbols:
        if hasattr(symbol, 'truthValue') and symbol.truthValue :
            queue.append(symbol)

    while len(queue) != 0:
        p = queue.pop()
        print(p.lit)
        if p == q:
            return True
        if not inferred[p.lit]:
            inferred[p.lit] = True
            for r in kb.listOfRules:
                for s in r.premises:
                    if p.lit == s.lit:
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
    print(q.lit)
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


nB11 = Literal("B(1,1)", True)
nB11.setTruthValue(True)
#B21 = Literal("B(2,1)")
#B21.setTruthValue(True)
nP12 = Literal("P(1,2)", True)
nP21 = Literal("P(2,1)", True)
nP12 = Literal("P(1,2)", True)


R1 = Sentence([nB11], [nP12], "R1")
R2 = Sentence([nB11], [nP21], "R2")



symbols = [nB11, nP12, nP21, nP12]
rules = [R1, R2]

KB = KnowledgeBase(symbols, rules)
result = FCEntails(KB, nP12)
print(result)

print("bc:")
orderlist = []
result2 = BCEntailment(KB, nP12, orderlist)
print(result2)
print(orderlist)


