INITIAL={1:5,2:3,3:0,4:9,5:2,6:0}
A=dict(op='ADD',src=(1,2),dest=3,owner='A')
B=dict(op='SUB',src=(4,5),dest=6,owner='B')
def alu(op,a,b):return a+b if op=='ADD' else a-b if op=='SUB' else None
def execute(regs,commands,read_ports=4,units=2):
 snapshot=dict(regs);results=[];reads=0
 for cmd in commands[:units]:
  if reads+len(cmd['src'])>read_ports:break
  reads+=len(cmd['src']);a,b=(snapshot[r] for r in cmd['src']);results.append(dict(value=alu(cmd['op'],a,b),dest=cmd['dest'],owner=cmd['owner'],valid=True))
 return results
def write_edge(regs,results,ports=2):
 chosen=[r for r in results if r['valid']][:ports]
 assert len({r['dest'] for r in chosen})==len(chosen)
 nextregs=dict(regs)
 for r in chosen:nextregs[r['dest']]=r['value']
 return nextregs,[r for r in results if r not in chosen]
def independent(a,b):
 return a['dest'] not in b['src'] and b['dest'] not in a['src'] and a['dest']!=b['dest']
def validate():
 assert independent(A,B)
 assert not independent(A,dict(op='SUB',src=(3,5),dest=4,owner='B'))
 assert independent(A,dict(op='SUB',src=(1,2),dest=6,owner='B')) # shared reads alone aren't a RAW dependency
 assert alu('ADD',5,3)==8 and alu('SUB',9,2)==7
 assert alu('SUB',5,3)==2 and alu('ADD',9,2)==11 # both units support either operation
 result=execute(INITIAL,[A,B]);assert [(r['dest'],r['value']) for r in result]==[(3,8),(6,7)]
 regs,left=write_edge(INITIAL,result);assert regs[3]==8 and regs[6]==7 and not left
 assert all(regs[i]==INITIAL[i] for i in [1,2,4,5])
 regs1,left=write_edge(INITIAL,result,1);assert regs1[3]==8 and regs1[6]==0 and left[0]['dest']==6
 regs2,left=write_edge(regs1,left,1);assert regs2==regs and not left
 assert len(execute(INITIAL,[A,B],2,2))==1
 assert len(execute(INITIAL,[A,B],4,1))==1
 for commands in [[A,B],[B,A]]:
  state=dict(INITIAL)
  for c in commands:state,_=write_edge(state,execute(state,[c]),1)
  assert state==regs
 return True
if __name__=='__main__':validate();print('PASS independent commands, generic ALUs, read bandwidth, buffered destinations, write edge bandwidth')
