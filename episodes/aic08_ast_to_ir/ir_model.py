"""Teaching IR for a known, pure tensor language; not a general Python compiler."""
import ast
CODE_A='y = relu(x @ W + b)'
CODE_B='t1 = x @ W\nt2 = t1 + b\ny = relu(t2)'
SHARED='a = x @ W\nb = relu(a)\nc = sigmoid(a)\ny = b + c'
SSA_SOURCE='x = 2\nx = x + 3\ny = x * 4'

class IR:
    def __init__(self,source):
        self.nodes=[];self.env={};self.definitions=[]
        for stmt in ast.parse(source).body:
            if not isinstance(stmt,ast.Assign) or len(stmt.targets)!=1:raise ValueError('Only simple assignments supported')
            value=self.lower(stmt.value);name=stmt.targets[0].id
            self.env[name]=value;self.definitions.append((name,value))
    def emit(self,op,args):
        name=f'v{len(self.nodes)}';self.nodes.append(dict(id=name,op=op,args=tuple(args)));return name
    def lower(self,n):
        if isinstance(n,ast.Name):return self.env.get(n.id,n.id)
        if isinstance(n,ast.Constant):return self.emit('Const',(n.value,))
        if isinstance(n,ast.BinOp):
            op={ast.MatMult:'MatMul',ast.Add:'Add',ast.Mult:'Mul'}[type(n.op)]
            return self.emit(op,(self.lower(n.left),self.lower(n.right)))
        if isinstance(n,ast.Call) and len(n.args)==1 and not n.keywords:
            op={'relu':'ReLU','sigmoid':'Sigmoid'}[n.func.id]
            return self.emit(op,(self.lower(n.args[0]),))
        raise ValueError(ast.dump(n))
    def uses(self,value):return tuple(n['id'] for n in self.nodes if value in n['args'] and n['op']!='Const')
    def signature(self):return [(n['op'],n['args']) for n in self.nodes]
    def eval(self,inputs):
        import numpy as np
        env=dict(inputs)
        for n in self.nodes:
            if n['op']=='Const':result=n['args'][0]
            else:
                args=[env[a] for a in n['args']]
                op=n['op']
                if op=='MatMul':result=args[0]@args[1]
                elif op=='Add':result=args[0]+args[1]
                elif op=='Mul':result=args[0]*args[1]
                elif op=='ReLU':result=np.maximum(args[0],0)
                else:result=1/(1+np.exp(-args[0]))
            env[n['id']]=result
        return env[self.env['y']]

CHAIN=IR(CODE_A);BRANCH=IR(SHARED);SSA=IR(SSA_SOURCE)
if __name__=='__main__':
    import numpy as np
    assert CHAIN.signature()==IR(CODE_B).signature()
    assert BRANCH.uses('v0')==('v1','v2')
    assert [n['op'] for n in BRANCH.nodes].count('MatMul')==1
    assert SSA.definitions==[('x','v0'),('x','v2'),('y','v4')]
    # Constants are explicit SSA values; no constant folding is applied.
    assert SSA.eval({})==20
    rng=np.random.default_rng(8)
    for _ in range(20):
        x=rng.normal(size=(2,3));w=rng.normal(size=(3,4));b=rng.normal(size=(4,))
        inputs={'x':x,'W':w,'b':b}
        assert np.array_equal(CHAIN.eval(inputs),IR(CODE_B).eval(inputs))
        assert np.array_equal(CHAIN.eval(inputs),np.maximum(x@w+b,0))
        a=x@w
        assert np.array_equal(BRANCH.eval(inputs),np.maximum(a,0)+1/(1+np.exp(-a)))
    print('Common IR structure, shared producer uses, 20 tensor examples and SSA result=20 verified.')
