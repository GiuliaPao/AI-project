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


def FCEntailment(kb, q):
    count = {}
    inferred = {}
    queue = []

    for symbol in kb.listOfSymbols:
        inferred[symbol.lit] = False

    for rule in kb.listOfRules:
        count[rule.name] = rule.numOfSymbols

    for symbol in kb.listOfSymbols:
        if hasattr(symbol, 'truthValue') and symbol.truthValue == True:
            queue.append(symbol)

    while len(queue) != 0:
        p = queue.pop()
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


def BCEntailment(kb, q):
    count = {}
    inferred = {}

    for symbol in kb.listOfSymbols:
        inferred[symbol.lit] = False

    for rule in kb.listOfRules:
        count[rule.name] = rule.numOfSymbols

    BCInference(kb, q, inferred, count)

    if hasattr(q, 'truthValue') and q.truthValue:
        return True
    else:
        return False


def BCInference(kb, q, inferred, count):
    for rule in kb.listOfRules:
        for c in rule.consequences:
            if q == c:
                for p in rule.premises:
                    if not inferred[p.lit]:
                        if hasattr(p, 'truthValue') and p.truthValue:
                            inferred[p.lit] = True
                            count[rule.name] -= 1
                    else:
                        BCInference(kb, p, inferred, count)
            if count[rule.name] == 0:
                q.truthValue = True
                inferred[q.lit] = True


nB11 = Literal("B(1,1)", True)
nB11.setTruthValue(True)
#B21 = Literal("B(2,1)")
#B21.setTruthValue(True)
nP12 = Literal("P(1,2)", True)
nP21 = Literal("P(2,1)", True)
P11 = Literal("P(1,1)")


R1 = Sentence([nB11], [nP12, nP21], "R1")


symbols = [nB11, nP12, nP21, P11]
rules = [R1]

KB = KnowledgeBase(symbols, rules)
result = BCEntailment(KB, P11)

print(result)


