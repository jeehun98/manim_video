"""Small teaching language: identifiers, assignment, calls, +, *, @, parentheses."""
import re
IDENTIFIER=r'[A-Za-z_][A-Za-z0-9_]*'
KINDS={'=':'ASSIGN','+':'PLUS','*':'STAR','@':'MATMUL','(':'LPAREN',')':'RPAREN'}

def lex(source):
    result=[];i=0
    while i<len(source):
        if source[i].isspace():i+=1;continue
        match=re.match(IDENTIFIER,source[i:])
        if match:
            s=match.group();result.append(('IDENT',s));i+=len(s)
        elif source[i] in KINDS:
            result.append((KINDS[source[i]],source[i]));i+=1
        else:raise SyntaxError(f'Unexpected character at {i}')
    return result+[('EOF','')]

class Parser:
    def __init__(self,source):self.tokens=lex(source);self.i=0
    def at(self,kind):return self.tokens[self.i][0]==kind
    def take(self,kind):
        if not self.at(kind):raise SyntaxError(f'Expected {kind}, got {self.tokens[self.i]}')
        token=self.tokens[self.i];self.i+=1;return token[1]
    def factor(self):
        if self.at('LPAREN'):
            self.take('LPAREN');node=self.expr();self.take('RPAREN');return node
        name=self.take('IDENT')
        if self.at('LPAREN'):
            self.take('LPAREN');arg=self.expr();self.take('RPAREN');return ('call',name,arg)
        return ('id',name)
    def term(self):
        node=self.factor()
        while self.at('STAR') or self.at('MATMUL'):
            op=self.tokens[self.i][1];self.i+=1;node=(op,node,self.factor())
        return node
    def expr(self):
        node=self.term()
        while self.at('PLUS'):
            self.take('PLUS');node=('+',node,self.term())
        return node
    def parse(self):
        if self.at('IDENT') and self.tokens[self.i+1][0]=='ASSIGN':
            name=self.take('IDENT');self.take('ASSIGN');node=('=',('id',name),self.expr())
        else:node=self.expr()
        self.take('EOF');return node

def parse(source):return Parser(source).parse()

if __name__=='__main__':
    import ast
    def normalize(n):
        if isinstance(n,ast.Name):return ('id',n.id)
        if isinstance(n,ast.BinOp):return ({ast.Add:'+',ast.Mult:'*',ast.MatMult:'@'}[type(n.op)],normalize(n.left),normalize(n.right))
        if isinstance(n,ast.Call):return ('call',n.func.id,normalize(n.args[0]))
        if isinstance(n,ast.Assign):return ('=',normalize(n.targets[0]),normalize(n.value))
        raise ValueError(type(n))
    examples=['a+b*c','(a+b)*c','result = a + b * c','y = relu(x @ W + b)','a+b+c','a*b*c','((a+b)*c)','a@b*c','f(a+b)']
    for source in examples:
        n=ast.parse(source).body[0];n=n.value if isinstance(n,ast.Expr) else n
        assert parse(source)==normalize(n),source
    for source in ['a + * b','(a+b','a b','1abc','a+b)']:
        try:parse(source)
        except SyntaxError:pass
        else:raise AssertionError(source)
    assert lex('result = a + b * c')==[('IDENT','result'),('ASSIGN','='),('IDENT','a'),('PLUS','+'),('IDENT','b'),('STAR','*'),('IDENT','c'),('EOF','')]
    print('9 AST comparisons to Python, 5 syntax rejections, exact token stream passed.')
