"""From character spans to tokens and two different syntax trees."""
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from visual_library.manim import configure_vertical,txt,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
from episodes.aic07_lexing_parsing.syntax_model import lex,parse,IDENTIFIER
configure_vertical();config.disable_caching=True
CUES=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
def p(x,y):return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):return txt(str(s),size,color,width).move_to(p(x,y))
def box(s,x,y,w=2.2,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=.8,corner_radius=.12,color=color,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(s,x,y,24,color,w-.15))
def arrow(a,b,color=MUTED):return Arrow(p(*a),p(*b),buff=.17,color=color,stroke_width=2,max_tip_length_to_length_ratio=.16)

def token_row(source='a+b*c',y=3.5):
    ts=lex(source)[:-1];g=VGroup()
    # Avoid pretending each character is a token: each lexeme is one box.
    for j,(kind,s) in enumerate(ts):
        x=(j-(len(ts)-1)/2)*1.17
        g.add(box(s,x,y,1.02,WEIGHT if kind=='IDENT' else SPARSE))
    return g

def syntax_tree(source,x=0,y=2.8,width=7.2,dy=1.5):
    ast=parse(source);nodes={};lines=[]
    def children(n):
        if n[0]=='id':return []
        if n[0]=='call':return [n[2]]
        return [n[1],n[2]]
    def leaves(n):return sum(leaves(c) for c in children(n)) if children(n) else 1
    def build(n,left,right,level,path):
        xx=(left+right)/2;yy=y-level*dy
        label=n[1] if n[0]=='id' else 'Call: '+n[1] if n[0]=='call' else n[0]
        color=WEIGHT if n[0]=='id' else GOOD if n[0]=='call' else ACCENT if level==0 else SPARSE
        nodes[path]=box(label,xx,yy,1.55 if n[0]=='call' else .9,color)
        current=left;total=leaves(n)
        for j,c in enumerate(children(n)):
            extent=(right-left)*leaves(c)/total
            childxy=build(c,current,current+extent,level+1,path+(j,))
            lines.append(Line(p(xx,yy-.4),p(childxy[0],childxy[1]+.4),color=MUTED,stroke_width=2))
            current+=extent
        return xx,yy
    build(ast,x-width/2,x+width/2,0,())
    g=VGroup(VGroup(*lines),VGroup(*nodes.values()));g.nodes=nodes;g.ast=ast
    return g

def grammar():
    return VGroup(text('Expr  → Term ( "+" Term )*',y=3.3,size=31,color=ACCENT),text('Term → Factor ( "*" Factor )*',y=1.7,size=30,color=SPARSE),text('Factor → IDENT | "(" Expr ")"',y=.1,size=30,color=WEIGHT),text('EBNF 표기 · 덧셈은 바깥, 곱셈은 항 안에',y=-2,size=24,color=MUTED),text('반복 표기 *와 곱셈 토큰 "*"를 구분',y=-3.5,size=23,color=MUTED))

def compute_ir(x=0,top=2.8):
    g=VGroup(box('MatMul',x,top,2.5,WEIGHT),box('Add',x,top-2,2.5,SPARSE),box('ReLU',x,top-4,2.5,GOOD),arrow((x,top-.4),(x,top-1.6),SPARSE),arrow((x,top-2.4),(x,top-3.6),GOOD))
    return g

class LexingParsing(Scene):
    DURATION=164
    def to(self,t):
        if self.time>t+1/30:raise RuntimeError(f'Timeline overflow {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def show(self,m,d=.45):self.play(FadeIn(m),run_time=d);self.stage.add(m);return m
    def cue(self,i,title,clear=True):
        self.to(CUES[i]['start']);cap=text(CUES[i]['caption'],y=-6.2,size=26);head=text(title,y=5.05,size=27,color=ACCENT)
        anim=[]
        if clear and len(self.stage):anim.append(FadeOut(self.stage))
        if len(self.caption):anim.append(ReplacementTransform(self.caption,cap))
        else:self.add(cap)
        if len(self.head):anim.append(ReplacementTransform(self.head,head))
        else:self.add(head)
        if anim:self.play(*anim,run_time=.2)
        if clear:self.stage=VGroup()
        self.caption=cap;self.head=head
    def construct(self):
        self.stage=VGroup();self.caption=VGroup();self.head=VGroup()
        self.add(text('AI 컴파일러 / 07',y=7.35,size=21,color=MUTED),text('문자를 읽는 것과\n구조를 이해하는 것은 다르다',y=6.4,size=32),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text('문자 → 토큰 → 구문 구조 → 계산 표현',y=-7.45,size=19,color=MUTED))
        self.cue(0,'01  같은 변수와 연산자, 다른 묶음')
        self.show(text('a + b × c',y=2.9,size=52,color=WEIGHT));self.show(text('(a + b) × c',y=-.2,size=52,color=SPARSE));self.show(text('a + (b × c)       (a + b) × c',y=-3.1,size=30,color=MUTED))
        self.cue(1,'01  알아본 문자만으로 충분할까?')
        self.show(VGroup(token_row(y=3.4),text('a, b, c · 덧셈 · 곱셈',y=1.5,size=33,color=WEIGHT),text('어떤 연산이 어떤 묶음에 속할까?',y=-.6,size=32,color=ACCENT),text('토큰 식별 규칙 + 구조를 해석하는 규칙',y=-3.2,size=27,color=GOOD)))

        self.cue(2,'02  Lexer: 문자 나열을 토큰으로')
        self.show(text('result = a + b * c',y=3.9,size=38,color=ACCENT))
        for j,(kind,s) in enumerate(lex('result = a + b * c')[:-1]):
            y=2.6-j*.92
            self.show(VGroup(box(s,-2.4,y,2,WEIGHT),text(kind,1.4,y,26,SPARSE,3)),.2)
        self.cue(3,'02  여섯 문자가 하나의 토큰이 된다')
        letters=VGroup(*[text(ch,(j-2.5)*.75,3.2,37,WEIGHT,.65) for j,ch in enumerate('result')]);self.show(letters)
        one=box('IDENT(result)',0,1.3,5,ACCENT)
        self.play(TransformFromCopy(letters,one),run_time=.9);self.stage.add(one)
        self.show(VGroup(text('6개 문자 → 1개 식별자 토큰',y=-.2,size=31,color=GOOD),box('=  ASSIGN',-2.3,-2,2.5,SPARSE),box('+  PLUS',.3,-2,2.2,SPARSE),box('*  STAR',2.7,-2,2.2,SPARSE),text('문자 수와 토큰 수는 다르다',y=-4,size=28,color=MUTED)))
        self.cue(4,'02  식별자는 문자 패턴으로 정의할 수 있다')
        self.show(VGroup(text(IDENTIFIER,y=3.6,size=34,color=ACCENT),box('시작 문자',-2,1.7,3,WEIGHT),box('이후 문자',2,1.7,3,SPARSE),text('영문자 / _',-2,.4,27,WEIGHT,3),text('영문자 / 숫자 / _',2,.4,25,SPARSE,3.5),text('result · a · value_2',y=-1.5,size=35,color=GOOD),text('정규 표현식 → 유한 오토마타',y=-3,size=30,color=ACCENT),text('설명을 위한 ASCII 식별자 규칙',y=-4.4,size=23,color=MUTED)))
        self.cue(5,'02  토큰 목록에는 아직 트리가 없다')
        self.show(token_row(y=3.4));self.show(VGroup(text('무엇인지: 식별자와 연산자',y=1.5,size=30,color=WEIGHT),text('어떻게 묶이는지: 아직 구조로 만들지 않음',y=-.5,size=27,color=ACCENT),text('a + [ b * c ]',y=-2.5,size=44,color=SPARSE)))

        self.cue(6,'03  Parser: 토큰 사이의 계층 구조')
        self.show(VGroup(box('토큰 목록',0,3.2,4,WEIGHT),arrow((0,2.7),(0,1.5)),box('문법 규칙으로 분석',0,1,5,ACCENT),arrow((0,.5),(0,-.7)),box('구문 구조',0,-1.2,4,GOOD),text('어떤 토큰이 어떤 식의 일부인가?',y=-3.6,size=29,color=MUTED)))
        self.cue(7,'03  우선순위를 문법의 계층에 반영한다')
        g=self.show(grammar());self.play(Indicate(g[0],color=ACCENT),Indicate(g[1],color=SPARSE),run_time=.8)
        self.cue(8,'03  괄호 안에는 다시 식이 들어간다')
        self.show(VGroup(text('Factor → "(" Expr ")"',y=3.6,size=40,color=WEIGHT),box('Expr',0,1.5,3,ACCENT),box('Term',0,-.1,3,SPARSE),box('Factor',0,-1.7,3,WEIGHT),arrow((0,1.05),(0,.35)),arrow((0,-.55),(0,-1.25)),CurvedArrow(p(1.7,-1.7),p(1.7,1.5),angle=PI/2,color=GOOD),text('다시 Expr',2.9,-.1,22,GOOD,1.8),text('문맥 자유 문법의 재귀적 구조',y=-4,size=29,color=GOOD)))
        self.cue(9,'03  이번 문법은 우선순위를 반영한다')
        self.show(grammar());self.show(text('a + b * c → a + (b * c)',y=-4.65,size=29,color=GOOD))

        self.cue(10,'04  덧셈 아래에 곱셈이 놓인다')
        row=self.show(token_row().scale(.58).move_to(p(-2.1,4.1)));left=self.show(syntax_tree('a+b*c',x=-2.1,y=2.1,width=3.3,dy=1.35))
        self.show(text('a + b * c',-2.1,-2.2,28,WEIGHT,3.5))
        for token,path in [(row[0],(0,)),(row[1],()),(row[2],(1,0)),(row[3],(1,)),(row[4],(1,1))]:
            target=left.nodes[path].copy()
            self.play(TransformFromCopy(token,target),run_time=.3);self.stage.add(target)
        self.cue(11,'04  괄호를 바꾸면 트리의 뿌리가 바뀐다',clear=False)
        self.show(token_row('(a+b)*c').scale(.43).move_to(p(2.1,4.1)))
        right=self.show(syntax_tree('(a+b)*c',x=2.1,y=2.1,width=3.3,dy=1.35))
        self.show(text('(a + b) * c',2.1,-2.2,28,SPARSE,3.5));self.play(Circumscribe(left.nodes[()],color=ACCENT),Circumscribe(right.nodes[()],color=GOOD),run_time=.7)
        self.show(text('덧셈의 오른쪽이 곱셈 / 곱셈의 왼쪽이 덧셈',y=-4,size=25,color=MUTED))
        self.cue(12,'04  일렬로 나열된 토큰이 계층 구조로')
        self.show(VGroup(token_row().scale(.58).move_to(p(-2.1,4.1)),token_row('(a+b)*c').scale(.43).move_to(p(2.1,4.1))));a=self.show(syntax_tree('a+b*c',x=-2.1,y=2.1,width=3.3,dy=1.35));b=self.show(syntax_tree('(a+b)*c',x=2.1,y=2.1,width=3.3,dy=1.35))
        self.show(VGroup(text('a + b * c',-2.1,-2.2,28,WEIGHT,3.5),text('(a + b) * c',2.1,-2.2,28,SPARSE,3.5),text('무엇이 무엇에 속하는가',y=-4,size=34,color=ACCENT)))
        self.cue(13,'04  AST: 추상 구문 트리')
        self.show(syntax_tree('a+b*c',y=3.3,width=6,dy=1.7));self.show(VGroup(text('Abstract Syntax Tree',y=-1.8,size=34,color=ACCENT),text('핵심 구문을 노드와 관계로 표현',y=-3.3,size=28,color=GOOD),text('원문의 모든 기호를 그대로 남길 필요는 없음',y=-4.5,size=23,color=MUTED)))
        self.cue(14,'04  괄호 기호 대신, 괄호가 만든 구조')
        self.show(text('(a + b) * c',y=4.1,size=38,color=SPARSE));g=self.show(syntax_tree('(a+b)*c',y=2.4,width=6,dy=1.6))
        self.play(Circumscribe(g.nodes[(0,)],color=ACCENT),run_time=.7);self.show(text('괄호 노드 없이도 덧셈의 묶음이 남음',y=-3.8,size=29,color=GOOD))

        self.cue(15,'05  중첩된 식을 처리하고 바깥으로 돌아온다')
        self.show(VGroup(text('( a + ( b * c ) )',y=3.6,size=43,color=WEIGHT),box('바깥 식 분석',-1.8,1.7,3.4,ACCENT),box('안쪽 식 분석',1.8,-.3,3.4,SPARSE),arrow((-.2,1.25),(1.3,.15),SPARSE),CurvedArrow(p(1.5,-.9),p(-2,.9),angle=-PI/2,color=GOOD),text('복귀',-.9,-.8,24,GOOD,1.3),text('재귀 호출 / 명시적인 스택 등',y=-2.8,size=29,color=GOOD),text('고전적 정규식만으로 임의 깊이를 일반 판정할 수 없음',y=-4.4,size=22,color=MUTED)))
        self.cue(16,'05  서로 다른 규칙을 다루는 두 역할')
        self.show(VGroup(box('Lexer',-2.1,2.8,3.4,WEIGHT),box('Parser',2.1,2.8,3.4,SPARSE),text('문자 패턴',-2.1,1.1,29,WEIGHT,3.5),text('문법 규칙',2.1,1.1,29,SPARSE,3.5),text('토큰 식별',-2.1,-.5,29,WEIGHT,3.5),text('구조 분석',2.1,-.5,29,SPARSE,3.5),text('처리할 문제에 맞게 규칙을 나눈다',y=-3.2,size=31,color=ACCENT)))
        self.cue(17,'05  역할 구분과 구현 모듈은 다르다')
        self.show(VGroup(box('토큰 식별',0,2.7,4,WEIGHT),box('구문 구조 분석',0,.4,4,SPARSE),text('두 역할은 구분할 수 있음',y=-1.5,size=32,color=ACCENT),text('반드시 별도 모듈이어야 하는 것은 아님',y=-3.6,size=27,color=MUTED)))

        self.cue(18,'06  소스 기반 프런트엔드의 구문 분석')
        self.show(text('y = relu(x @ W + b)',y=4.25,size=36,color=ACCENT));g=self.show(syntax_tree('y=relu(x@W+b)',y=2.95,width=6.5,dy=1.35))
        self.show(text('할당 → 함수 호출 → 이항 연산',y=-4.2,size=27,color=GOOD))
        self.cue(19,'06  의미를 확인한 뒤 계산 IR로')
        self.show(text('이름 · 타입 · 연산 의미 확인',y=4.15,size=28,color=ACCENT));self.show(compute_ir(top=2.5))
        self.show(VGroup(text('x, W',-2.7,2.5,27,WEIGHT,2),arrow((-1.8,2.5),(-1.25,2.5),WEIGHT),text('b',-2.7,.5,29,SPARSE,1),arrow((-1.8,.5),(-1.25,.5),SPARSE),text('행렬곱 가능 · 덧셈의 형상과 타입 확인',y=-3.1,size=24,color=MUTED),text('알려진 ReLU 함수라는 조건',y=-4.3,size=23,color=MUTED)))
        self.cue(20,'06  표현의 목적과 추상화 수준')
        self.show(VGroup(box('AST',-2,3.2,3.4,WEIGHT),box('계산 IR',2,3.2,3.4,SPARSE),text('소스의 구문',-2,1.8,27,WEIGHT,3.5),text('분석·변환 목적',2,1.8,27,SPARSE,3.5)))
        self.show(syntax_tree('a+b*c',x=-2,y=.3,width=3,dy=1.3));self.show(compute_ir(x=2,top=.3).scale(.67,about_point=p(2,.3)))
        self.show(text('둘 모두 연산 관계를 표현할 수 있음',y=-4.3,size=26,color=GOOD))
        self.cue(21,'06  AST도 IR의 한 형태가 될 수 있다')
        self.show(VGroup(RoundedRectangle(width=7,height=4.8,color=SPARSE,corner_radius=.2).move_to(p(0,1)),text('넓은 의미의 중간 표현 IR',y=2.8,size=31,color=SPARSE),box('AST',-1.7,.7,2.5,WEIGHT),box('계산 IR',1.7,.7,2.5,GOOD),text('분류는 시스템과 사용 목적에 따라 다름',y=-.8,size=23,color=MUTED),text('중요한 것은 표현의 목적과 추상화 수준',y=-3.3,size=29,color=ACCENT)))
        self.cue(22,'06  계산 표현을 얻는 다른 경로도 있다')
        self.show(VGroup(box('소스 분석',-2,3.3,3.2,WEIGHT),box('연산 추적·캡처',2,3.3,3.5,SPARSE),arrow((-2,2.8),(0,1.4),WEIGHT),arrow((2,2.8),(0,1.4),SPARSE),box('계산 표현',0,.9,4,GOOD),text('모든 AI 컴파일러가 소스를 직접 파싱하지 않음',y=-2.1,size=26,color=MUTED)))
        self.cue(23,'결론  식별하는 일과 구조를 만드는 일')
        self.show(VGroup(text('문자 → 토큰',y=2.8,size=43,color=WEIGHT),text('토큰 → 구문 구조',y=.3,size=43,color=SPARSE),text('서로 다른 역할 · 함께 드러나는 구조',y=-3,size=30,color=ACCENT)))
        self.cue(24,'결론  소스 코드 변환의 출발점')
        self.show(VGroup(text('일렬로 나열된 코드에서',y=3,size=35,color=WEIGHT),text('코드가 나타내는 구조로',y=1.4,size=35,color=SPARSE)))
        self.show(syntax_tree('a+b*c',y=-.15,width=5,dy=1.35));self.show(text('먼저, 구조를 알아내는 것입니다',y=-4.2,size=31,color=ACCENT))
        self.to(self.DURATION)
