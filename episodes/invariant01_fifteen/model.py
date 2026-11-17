"""The blank is element 16; checker colors belong to fixed board squares."""
SOLVED=tuple(range(1,16))+(0,)
IMPOSSIBLE=SOLVED[:13]+(15,14,0)

def neighbors(blank):
    r,c=divmod(blank,4)
    return [4*(r+dr)+c+dc for dr,dc in ((-1,0),(0,-1),(1,0),(0,1))
            if 0<=r+dr<4 and 0<=c+dc<4]

def parity(board):
    values=[16 if n==0 else n for n in board]
    return sum(values[i]>values[j] for i in range(16) for j in range(i+1,16))%2

def color(board):
    r,c=divmod(board.index(0),4)
    return (r+c)%2

def invariant(board):return parity(board)^color(board)

def move(board,index):
    blank=board.index(0)
    if index not in neighbors(blank):raise ValueError('Only a tile adjacent to the blank may move')
    result=list(board);result[index],result[blank]=result[blank],result[index]
    result=tuple(result)
    assert parity(result)==1-parity(board)
    assert color(result)==1-color(board)
    assert invariant(result)==invariant(board)
    return result

def samples(start,count):
    """Deterministic legal walk, avoiding immediate reversals when possible."""
    state=start;previous=-1
    for k in range(count):
        choices=[i for i in neighbors(state.index(0)) if i!=previous]
        index=choices[(k*7+3)%len(choices)]
        previous=state.index(0)
        state=move(state,index)
        yield state
