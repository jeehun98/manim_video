"""Equivalent compact epsilon NFA and subset DFA; no engine timing claims."""
from functools import lru_cache

# q1 is the repetition boundary; q2 is halfway through the aa alternative.
# This is a compact equivalent NFA, not a literal Thompson fragment layout.
EDGES = ((0, '', 1), (1, 'a', 1), (1, 'a', 2), (2, 'a', 1), (1, 'b', 3))
ALPHABET = ('a', 'b', 'c')
START = 0
ACCEPT = 3

def closure(states):
    result=set(states);todo=list(result)
    while todo:
        q=todo.pop()
        for a,label,b in EDGES:
            if a==q and not label and b not in result:
                result.add(b);todo.append(b)
    return frozenset(result)

def step(states, char):
    return closure({b for a,label,b in EDGES if label==char and a in states})

def trace(word):
    history=[closure({START})]
    for char in word:history.append(step(history[-1],char))
    return history

def accepts(word):return ACCEPT in trace(word)[-1]

def subsets():
    states=[closure({START})];table={};todo=list(states)
    while todo:
        source=todo.pop(0)
        for char in ALPHABET:
            target=step(source,char)
            if target not in states:states.append(target);todo.append(target)
            table[states.index(source),char]=states.index(target)
    return states,table

@lru_cache(None)
def splits(n):
    if n==0:return ((),)
    return tuple((first,)+rest for first in (1,2) if first<=n for rest in splits(n-first))

@lru_cache(None)
def count(n):
    if n<2:return 1
    return count(n-1)+count(n-2)

def show_set(states):return '{'+', '.join('q'+str(i) for i in sorted(states))+'}' if states else '∅'

if __name__=='__main__':
    import itertools,re
    states,table=subsets();checks=0
    for n in range(9):
        for chars in itertools.product(ALPHABET,repeat=n):
            word=''.join(chars);q=0
            for ch in word:q=table[q,ch]
            expected=re.fullmatch(r'(a|aa)*b',word) is not None
            assert accepts(word)==expected==(ACCEPT in states[q]),word
            checks+=1
    assert len(splits(5))==count(5)==8
    assert [count(i) for i in (5,10,15,20)]==[8,89,987,10946]
    assert trace('aaaaac')[-1]==frozenset()
    assert len(states)==4
    print(f'{checks} NFA/DFA/fullmatch comparisons passed; 8 splits; 4 reachable subset states.')
