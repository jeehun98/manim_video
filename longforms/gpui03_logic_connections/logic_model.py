"""The actual NAND netlists and transistor edges used by the diagrams."""
NETLISTS={
 'NOT':[('Y','A','A')],
 'AND':[('n','A','B'),('Y','n','n')],
 'OR':[('a','A','A'),('b','B','B'),('Y','a','b')],
 'XOR':[('n','A','B'),('a','A','n'),('b','B','n'),('Y','a','b')],
}
def evaluate(name,a,b):
 values={'A':int(bool(a)),'B':int(bool(b))}
 for out,x,y in NETLISTS[name]:values[out]=1-(values[x]&values[y])
 return values
def transistor_edges(a,b):
 return [('pA','VDD','Y',not a),('pB','VDD','Y',not b),('nA','Y','MID',bool(a)),('nB','MID','GND',bool(b))]
def reachable(edges,start,target):
 seen={start};pending=[start]
 while pending:
  u=pending.pop()
  for _,v,w,on in edges:
   if not on:continue
   nxt=w if v==u else v if w==u else None
   if nxt is not None and nxt not in seen:seen.add(nxt);pending.append(nxt)
 return target in seen
def nand_state(a,b):
 edges=transistor_edges(bool(a),bool(b))
 up=reachable(edges,'Y','VDD');down=reachable(edges,'Y','GND')
 assert up!=down,'Output must be connected to exactly one rail in a stable state.'
 return dict(a=int(bool(a)),b=int(bool(b)),up=up,down=down,y=int(up),edges=edges)
