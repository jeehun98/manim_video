"""Standard entry/exit Thompson fragments; shared by animation and validation."""
AST = ('cat', 'root',
       ('star', 'repeat', ('alt', 'choice', ('lit', 'choice_A', 'A'), ('lit', 'choice_B', 'B'))),
       ('cat', 'suffix_ABB', ('lit', 'suffix_A', 'A'),
        ('cat', 'suffix_BB', ('lit', 'suffix_B1', 'B'), ('lit', 'suffix_B2', 'B'))))


class Thompson:
    def __init__(self):
        self.count = 0
        self.edges = []
        self.fragments = {}
        self.root = self.build(AST)

    def state(self):
        q = self.count
        self.count += 1
        return q

    def edge(self, a, label, b):
        i = len(self.edges)
        self.edges.append((a, label, b))
        return i

    def build(self, ast):
        op, name, *args = ast
        if op == 'lit':
            start, end = self.state(), self.state()
            states = {start, end}
            edges = [self.edge(start, args[0], end)]
        elif op == 'star':
            child = self.build(args[0])
            start, end = self.state(), self.state()
            states = set(child['states']) | {start, end}
            edges = child['edges'] + [self.edge(start, '', child['start']), self.edge(start, '', end),
                                     self.edge(child['end'], '', child['start']), self.edge(child['end'], '', end)]
        else:
            left, right = self.build(args[0]), self.build(args[1])
            states = set(left['states']) | set(right['states'])
            edges = left['edges'] + right['edges']
            if op == 'alt':
                start, end = self.state(), self.state()
                states |= {start, end}
                edges += [self.edge(start, '', left['start']), self.edge(start, '', right['start']),
                          self.edge(left['end'], '', end), self.edge(right['end'], '', end)]
            elif op == 'cat':
                start, end = left['start'], right['end']
                edges += [self.edge(left['end'], '', right['start'])]
            else:
                raise ValueError(op)
        fragment = dict(start=start, end=end, states=sorted(states), edges=sorted(edges))
        self.fragments[name] = fragment
        return fragment

    def closure(self, states):
        reached = set(states)
        todo = list(reached)
        while todo:
            q = todo.pop()
            for a, label, b in self.edges:
                if a == q and label == '' and b not in reached:
                    reached.add(b)
                    todo.append(b)
        return reached

    def move(self, states, symbol):
        return {b for a, label, b in self.edges if a in states and label == symbol}

    def trace(self, word):
        states = self.closure({self.root['start']})
        steps = [dict(symbol='', moved={self.root['start']}, closed=set(states))]
        for symbol in word:
            moved = self.move(states, symbol)
            states = self.closure(moved)
            steps.append(dict(symbol=symbol, moved=moved, closed=set(states)))
        return steps

    def accepts(self, word):
        return self.root['end'] in self.trace(word)[-1]['closed']


MODEL = Thompson()
