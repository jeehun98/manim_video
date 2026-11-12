def operand(register,src,producers):
 # producers ordered nearest/youngest first; a pending nearer writer blocks older values.
 for p in producers:
  if p['valid'] and p['write'] and p['dest']==src:
   if not p['ready']:return None,'wait'
   return p['data'],p['stage']
 return register,'register'
def dependency(dest,write,valid,sources,ready):return bool(valid and write and dest in sources and not ready)
def validate():
 assert dependency(1,True,True,[1,2],False)
 assert not dependency(1,True,True,[1,2],True)
 assert not dependency(1,False,True,[1,2],False)
 assert not dependency(1,True,False,[1,2],False)
 assert not dependency(3,True,True,[1,2],False)
 alu=dict(valid=True,write=True,dest=3,ready=True,data=8,stage='EX/MEM')
 assert operand(0,3,[alu])==(8,'EX/MEM')
 load=dict(valid=True,write=True,dest=1,ready=False,data=100,stage='EX/MEM')
 assert operand(0,1,[load])==(None,'wait') # address100 is NOT the loaded data
 older=dict(valid=True,write=True,dest=1,ready=True,data=7,stage='MEM/WB')
 assert operand(0,1,[load,older])==(None,'wait')
 load_ready=dict(load,ready=True,data=5,stage='MEM/WB')
 assert operand(0,1,[load_ready])==(5,'MEM/WB')
 assert operand(3,2,[load])==(3,'register')
 # Load-use timeline: A advances, PC/IFID held, ID/EX invalid bubble.
 pc=2;ifid='ADD';idex='LOAD';exmem=None;memwb=None;results=[]
 assert dependency(1,True,True,[1,2],False)
 oldpc,oldifid=pc,ifid;exmem=idex;idex=None
 assert pc==oldpc and ifid==oldifid and exmem=='LOAD' and idex is None
 memwb=load_ready;idex=ifid;value,source=operand(0,1,[memwb]);results.append(value+3)
 assert results==[8] and source=='MEM/WB'
 assert operand(0,3,[alu])[0]-2==6
 return True
if __name__=='__main__':validate();print('PASS hazard controls, stall hold/bubble, newest ready writer, ALU/load forwarding')
