"""Born-again networks: same capacity, different targets and independently learned weights."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent
TEACHER=np.array([.7,.2,.1])
STUDENT=np.array([.4,.4,.2])
Q_FIXED=np.array([.6,.25,.15])
P_HIGH=np.array([.95,.03,.02])
P_LOW=np.array([.55,.30,.15])
TEACHER_ERROR=17.69
STUDENT_ERROR=16.69

def t(s,y=0,x=0,size=28,color=INK,width=7.7):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def box(s,x=0,y=0,w=2.2,h=.85,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=color,stroke_width=1.5,fill_color=BG,fill_opacity=1).move_to([x,y,0]),t(s,y,x,size=24,color=color,width=w-.2))

def network(x=0,y=0,color=WEIGHT):
    layers=[VGroup(*[Circle(.095,color=color,fill_color=BG,fill_opacity=1,stroke_width=1.7).move_to([x+dx,y+(n-1)*.27-j*.54,0]) for j in range(n)]) for dx,n in [(-.85,3),(0,4),(.85,3)]]
    edges=VGroup(*[Line(a.get_center(),b.get_center(),color=color,stroke_width=1,stroke_opacity=.35) for layer,next_layer in zip(layers,layers[1:]) for a in layer for b in next_layer])
    return VGroup(edges,*layers)

def twins(question=False):
    return VGroup(t('Teacher',3.7,-2,size=30,color=SPARSE,width=3),t('Student',3.7,2,size=30,color=WEIGHT,width=3),
                  network(-2,2,SPARSE),network(2,2,WEIGHT),Arrow([-1.02,2,0],[1.02,2,0],buff=.1,color=ACCENT,stroke_width=3),
                  t('출력 분포 p',.75,size=24,color=ACCENT),t('학습 완료',-.3,-2,size=24,color=SPARSE,width=3),t('새 초기값에서 학습',-.3,2,size=24,color=WEIGHT,width=3.6),
                  t('동일한 구조 · 동일한 파라미터 수',-1.6,size=28,color=GOOD),t('Student > Teacher ?' if question else '일부 실험에서 Student 정확도 > Teacher',-3,size=30,color=ACCENT),
                  t('설명용 토폴로지 · 성능 향상은 보편적 보장이 아님',-4.4,size=20,color=MUTED))

def bars(probs,top=2.6,color=WEIGHT):
    g=VGroup()
    for i,(name,p) in enumerate(zip(['고양이','호랑이','자동차'],probs)):
        y=top-i*.75
        g.add(t(name,y,-3,size=23,width=1.6),Rectangle(width=4,height=.36,color=MUTED,stroke_width=1).move_to([.15,y,0]))
        if p>0:g.add(Rectangle(width=4*p,height=.32,stroke_width=0,fill_color=color,fill_opacity=.85).move_to([-1.85+2*p,y,0]))
        g.add(t(f'{p*100:g}%',y,3.1,size=25,color=color,width=1.4))
    return g

def target_comparison():
    return VGroup(t('실제 정답 y · One-Hot',4,size=27,color=GOOD),bars([1,0,0],3,GOOD),
                  t('교사의 예측 p · Soft Target',.25,size=27,color=SPARSE),bars(TEACHER,-.7,SPARSE),t('설명용 확률 · 특정 이미지의 실측값이 아님',-3.65,size=21,color=MUTED),t('비정답 클래스에 대한 판단도 전달',-4.5,size=24,color=ACCENT))

def kl(p,q):return float(np.sum(np.asarray(p)*np.log(np.asarray(p)/np.asarray(q))))

def distillation(q=STUDENT):
    return VGroup(VGroup(t('Teacher p · 학습 중 고정',4,size=25,color=SPARSE),bars(TEACHER,3,SPARSE)),
                  VGroup(t('Student q · 학습으로 변화',.35,size=25,color=WEIGHT),bars(q,-.55,WEIGHT)),
                  t(f'KL(p ∥ q) = {kl(TEACHER,q):.3f}',-3.2,size=32,color=ACCENT),t('이 입력에서 분포 차이를 줄이는 학습 · T = 1',-4.4,size=21,color=MUTED))

def gradient_panel(p=P_HIGH):
    g=Q_FIXED-p
    panel=VGroup(t(f'교사 p = ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})',3.65,size=29,color=SPARSE),
                 t('학생 q = (0.60, 0.25, 0.15) 고정',2.65,size=26,color=WEIGHT),t('∂L/∂zᵢ = qᵢ − pᵢ',1.45,size=37,color=ACCENT),Line([0,.55,0],[0,-2.2,0],color=MUTED,stroke_width=1.5))
    for i,(name,v) in enumerate(zip(['고양이','호랑이','자동차'],g)):
        y=.05-i*.9;length=abs(v)*5
        panel.add(t(name,y,-3.2,size=23,width=1.5))
        if length>1e-8:panel.add(Rectangle(width=length,height=.35,stroke_width=0,fill_color=PRUNE if v>0 else GOOD,fill_opacity=.8).move_to([v*2.5,y,0]))
        panel.add(t(f'{v:+.2f}' if abs(v)>1e-8 else '0',y,v*5+(.48 if v>=0 else -.48),size=24,color=PRUNE if v>0 else GOOD,width=1.2))
    panel.add(t('로짓 z는 기울기 g의 반대 방향으로 이동',-2.85,size=23,color=MUTED),t('고양이 로짓을 높이는 신호' if g[0]<0 else '고양이 로짓을 낮추는 신호',-3.65,size=27,color=GOOD if g[0]<0 else PRUNE),t('증류 항만 비교 · 가상 분포 · 온도 T = 1',-4.5,size=20,color=MUTED))
    return panel

def objectives():
    return VGroup(t('Teacher · 정답으로 학습',3.6,size=28,color=SPARSE),box('Lteacher = CE(y, p)',0,2.1,7.3,1.1,SPARSE),
                  t('Student · 교사 출력으로도 학습',.5,size=28,color=WEIGHT),box('LKD = KL(p ∥ q)',0,-.9,7.3,1.1,WEIGHT),
                  t('CE(p, q)와는 교사 엔트로피만큼의 상수 차이',-2.5,size=22,color=MUTED),t('정답 손실을 병행하는 설정도 가능',-3.5,size=25,color=GOOD),t('구조는 같아도 학습 목적이 달라진다',-4.5,size=24,color=ACCENT))

def trajectories():
    g=VGroup()
    for x,color,title in [(-1.95,SPARSE,'Teacher · Lteacher'),(1.95,WEIGHT,'Student · LKD')]:
        g.add(RoundedRectangle(width=3.55,height=4.2,corner_radius=.1,color=MUTED,stroke_width=1).move_to([x,1.2,0]),t(title,3.85,x,size=24,color=color,width=3.6))
        center=np.array([x+(.4 if x<0 else -.4),.8 if x<0 else 1.7,0])
        for size in [.8,1.4,2.,2.65]:g.add(Ellipse(width=size,height=size*.6,color=color,stroke_width=1,stroke_opacity=.5).move_to(center))
    tp=CubicBezier([-3.2,2.7,0],[-2.9,1.3,0],[-2.4,.1,0],[-1.55,.8,0],color=SPARSE,stroke_width=3)
    sp=CubicBezier([3.1,-.3,0],[2.7,.8,0],[3,2.1,0],[1.55,1.7,0],color=WEIGHT,stroke_width=3)
    sp.set_stroke(opacity=.25)
    sd=Dot(sp.get_start(),color=ACCENT,radius=.09)
    g.add(tp,Dot(tp.get_end(),color=SPARSE,radius=.1),sp,sd,t('교사의 가중치에서 이어서 시작하지 않음',-2,size=26,color=ACCENT),t('새 초기값 · 다른 목표 · 다른 파라미터 해',-3.2,size=27,color=GOOD),t('서로 다른 목적함수의 설명용 단면 · 손실 높이 비교 아님',-4.5,size=19,color=MUTED))
    g.student_path=sp;g.student_dot=sd
    return g

def results():
    def result_card(title,error,x,color):
        return VGroup(RoundedRectangle(width=3.5,height=1.7,corner_radius=.12,color=color,stroke_width=1.5,fill_color=BG,fill_opacity=1).move_to([x,.95,0]),
                      t(title,1.4,x,size=24,color=color,width=3.25),t(f'{error:.2f}%',.65,x,size=41,color=color,width=3.25))
    return VGroup(t('CIFAR-100 · DenseNet-90-60',3.8,size=29,color=INK),t('테스트 오류율 · 낮을수록 좋음',2.75,size=25,color=MUTED),
                  result_card('Teacher',TEACHER_ERROR,-2,SPARSE),result_card('BAN Student',STUDENT_ERROR,2,WEIGHT),
                  t('동일한 구조의 단일 모델',-.65,size=29,color=GOOD),t('오류율 1.00%p 감소',-1.7,size=32,color=ACCENT),t('Furlanello et al. · ICML 2018 · Table 2',-2.8,size=22,color=MUTED),
                  t('BAN: 교사 출력으로 학습한 설정',-3.65,size=23,color=MUTED),t('일부 실험 예시 · 모든 설정에서 향상되는 것은 아님',-4.5,size=20,color=MUTED))

def generations():
    return VGroup(box('Teacher',0,3.2,5,1,SPARSE),box('학생 1',0,.85,5,1,WEIGHT),box('학생 2',0,-1.5,5,1,GOOD),
                  Arrow([0,2.55,0],[0,1.5,0],color=ACCENT,buff=.05),Arrow([0,.2,0],[0,-.85,0],color=ACCENT,buff=.05),
                  t('출력 분포',2,1.7,size=22,color=ACCENT,width=2.6),t('출력 분포',-.35,1.7,size=22,color=ACCENT,width=2.6),t('매 세대 같은 구조 · 새로운 초기값',-3.15,size=27,color=WEIGHT),t('세대가 늘어도 성능이 항상 향상되지는 않음',-4.4,size=21,color=MUTED))

class BornAgainNetworks(Scene):
    def chrome(self,i):
        titles=['학생이 스승을 뛰어넘는다면?','신경망에서의 청출어람','같은 구조 · 같은 크기','같은 크기인데 더 높은 정확도?','Born-Again Networks','교사의 성능이 학생의 한계일까?',
                '하나의 고양이 입력','정답 하나만 알려주는 학습','교사의 판단은 확률분포','정답 외의 판단도 담길 수 있다','출력 분포가 새로운 학습 신호로','Knowledge Distillation',
                '완전한 복사라면 같은 성능일 텐데','가중치를 복사하는 것이 아니다','새 초기값에서 새로운 파라미터로','학습 목표가 달라진다','정답과 교사 예측을 구별한다','교사가 언제나 옳지는 않다',
                '교사의 확신이 기울기를 바꾼다','다른 목표로 다른 해를 찾는다','같은 구조의 학생이 교사를 넘어선 사례','물려받는 것은 성능 상한이 아니다','판단을 새로운 학습 신호로','스승의 답이 학생의 한계는 아니다','신경망에서의 청출어람']
        return VGroup(t('신경망의 역설  /  06',7.35,size=20,color=MUTED),t('신경망에서의 청출어람',6.45,size=35),Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(titles[i],5.05,size=25,color=ACCENT),t('Born-Again Networks · Self-Distillation',-7.45,size=18,color=MUTED))

    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps=['학생이 스승에게 배웠는데\n오히려 더 뛰어난 실력을 갖게 된다면요?','신경망에서도\n이러한 청출어람이 발견되었습니다.','학습된 교사를 두고, 같은 구조와 크기의\n새 신경망을 학생으로 학습시킵니다.','학생이 교사보다\n높은 정확도를 얻을 수 있습니다.','이것이 Born-Again Networks입니다.','같은 크기의 신경망이\n왜 교사보다 좋은 결과를 얻을까요?',
              '고양이 사진 하나를\n생각해 보겠습니다.','보통은 정답이 고양이라는\n사실만 알려줍니다.','교사는 고양이 70%, 호랑이 20%, 자동차 10%처럼\n여러 클래스의 예측 확률을 출력할 수 있습니다.','교사가 다른 클래스들을 어떻게 판단했는지도\n정보로 담겨 있을 수 있습니다.','학생은 정답뿐 아니라 교사의 확률분포도\n학습 신호로 활용할 수 있습니다.','이것이 지식 증류입니다.',
              '교사의 판단을 그대로 복사하기만 한다면\n교사를 뛰어넘기 어려울 것 같습니다.','학생은 교사의 가중치를\n복사하지 않습니다.','새로운 초기값에서 시작해 전달받은 분포로\n자신의 파라미터를 학습합니다.','학생이 최소화하는 손실은\n교사가 처음 학습한 손실과 달라집니다.','정답뿐 아니라 교사의 예측 확률까지\n고려하도록 학습 목표가 바뀝니다.','교사의 판단이\n언제나 옳다는 뜻은 아닙니다.',
              '교사의 확신과 비정답 클래스의 확률도\n학생의 학습 방향에 영향을 줄 수 있습니다.','이 변화는 다른 해를 찾고 때로 더 좋은\n일반화 성능을 얻도록 도울 수 있습니다.','같은 크기의 학생이 교사를 뛰어넘는\n실험 결과가 보고되었습니다.','물려받는 것은 교사의 파라미터도\n교사의 성능 한계도 아닙니다.','교사가 만들어낸 판단을\n새로운 학습 신호로 활용합니다.','스승에게 배운다고 해서\n스승과 같은 답에 머무는 것은 아닙니다.','이것이 신경망에서 발견된\n청출어람의 역설입니다.']
        for i,s in enumerate(data['segments']):
            self.clear();self.add(self.chrome(i),t(caps[i],-6.15,size=24))
            p=self.panel(i);self.play(FadeIn(p),run_time=.3)
            if i==9:self.play(Circumscribe(p[3],color=ACCENT),run_time=.8)
            if i==10:
                for q in [np.array([.6,.25,.15]),TEACHER]:
                    self.play(Transform(p[1],VGroup(t('Student q · 학습으로 변화',.35,size=25,color=WEIGHT),bars(q,-.55,WEIGHT))),Transform(p[2],t(f'KL(p ∥ q) = {kl(TEACHER,q):.3f}',-3.2,size=32,color=ACCENT)),run_time=.75)
            if i in [14,19]:
                self.play(MoveAlongPath(p.student_dot,p.student_path),p.student_path.animate.set_stroke(opacity=1),run_time=1.5)
            if i==18:
                self.wait(2.2)
                self.play(FadeOut(p),run_time=.2)
                p=gradient_panel(P_LOW)
                self.play(FadeIn(p),run_time=.25)
                self.play(Circumscribe(p[2],color=ACCENT),run_time=.7)
            if i==20:self.play(Indicate(p[3],color=GOOD),run_time=.8)
            remaining=s['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-121)<1/30+.001

    def panel(self,i):
        if i in [0,1,2,3,4,5]:return twins(i in [0,5])
        if i in [6,7]:
            photo=ImageMobject(str(ROOT/'assets'/'cat_photo.png')).set_height(3.3).move_to([0,1.9,0])
            return Group(photo,t('실제 정답: 고양이',-.5,size=31,color=GOOD),bars([1,0,0],-1.5,GOOD),t('One-Hot 정답 목표',-4.3,size=25,color=MUTED))
        if i in [8,9,16]:return target_comparison()
        if i==10:return distillation()
        if i==11:return VGroup(t('Knowledge Distillation',2.6,size=36,color=WEIGHT),t('LKD = KL(p ∥ q)',.7,size=39,color=ACCENT),t('p: 교사 목표 · q: 학생 예측',-1.2,size=28,color=INK),t('교사 출력을 학생의 학습 목표로',-3.1,size=30,color=GOOD),t('온도 T = 1 · 정답 손실을 병행할 수도 있음',-4.4,size=20,color=MUTED))
        if i==12:return VGroup(box('모든 입력에서 예측이 완전히 같다면',0,2.8,7.5,1,SPARSE),t('평가 성능도 같다',1.2,size=37,color=INK),t('실제 증류는 유한한 학습 입력에서 진행',-.8,size=29,color=WEIGHT),t('다른 초기값·학습 목표로 다른 함수를 얻을 수 있음',-2.5,size=24,color=GOOD),t('완전한 함수 복제 자체가 성능 향상의 원인은 아님',-4.2,size=22,color=MUTED))
        if i==13:return VGroup(network(-2,2.3,SPARSE),network(2,2.3,WEIGHT),t('θTeacher',.8,-2,size=27,color=SPARSE,width=3),t('새 θStudent',.8,2,size=27,color=WEIGHT,width=3),t('θStudent ← θTeacher',-.8,size=32,color=PRUNE),Cross(stroke_color=PRUNE,stroke_width=3).scale(.45).move_to([0,-.8,0]),t('파라미터 복사 대신 출력 분포를 전달',-2.7,size=29,color=ACCENT),t('교사 고정 · 학생은 별도 최적화',-4.2,size=24,color=MUTED))
        if i in [14,19]:return trajectories()
        if i==15:return objectives()
        if i==17:return VGroup(t('실제 정답',3.5,size=26,color=GOOD),box('고양이',0,2.4,5,1,GOOD),t('교사의 판단은 틀릴 수도 있음',.75,size=30,color=PRUNE),bars([.1,.8,.1],-.4,SPARSE),t('학습 신호로 활용 ≠ 교사 판단이 항상 참',-3.4,size=25,color=ACCENT),t('오분류를 설명하기 위한 가상 예시',-4.4,size=21,color=MUTED))
        if i==18:return gradient_panel()
        if i==20:return results()
        if i==21:return generations()
        if i==22:return VGroup(t('물려받는 것',3.4,size=28,color=MUTED),box('교사가 만든 출력 분포 p',0,2,7,1.1,SPARSE),Arrow([0,1.3,0],[0,.2,0],color=ACCENT),box('학생의 새로운 학습 목표',0,-.5,7,1.1,WEIGHT),t('자신의 초기값과 파라미터로 학습',-2.4,size=29,color=GOOD),t('같은 구조라도 선택되는 해는 달라질 수 있다',-4,size=24,color=MUTED))
        return VGroup(t('같은 구조 · 다른 학습 신호',3,size=35,color=WEIGHT),t('스승의 지식을 배우는 것과',1.1,size=34,color=INK),t('스승의 한계에 머무르는 것은 다르다',-.5,size=32,color=ACCENT),t('Born-Again Networks',-2.4,size=33,color=GOOD),t('일반화 개선은 조건부 결과 · 보편적 보장은 아님',-4.2,size=21,color=MUTED))
