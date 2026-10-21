"""Model soups: straight parameter interpolation and a conditional low-loss basin."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent
SURFACE_SCENES={0,1,2,15,24}
A=np.array([-1.5,-.1]);B=np.array([1.5,.1]);START=np.array([-1.5,1.6])
EXTRAS=np.array([[-1.2,-.12],[-.6,.16],[.6,-.16],[1.2,.12]])

def t(s,y=0,x=0,size=28,color=INK,width=7.7):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def box(s,x=0,y=0,w=2.2,h=.85,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=color,stroke_width=1.5,fill_color=BG,fill_opacity=1).move_to([x,y,0]),t(s,y,x,size=25,color=color,width=w-.2))

def theta(lam):return (1-lam)*A+lam*B
def barrier(lam):return low_loss(0)+.6*np.sin(np.pi*lam)**2
def low_loss(lam):return landscape(-1.5+3*np.asarray(lam),-.1+.2*np.asarray(lam))
def landscape(x,y):return .22+.24*(y-.13*np.sin(1.4*x))**2+.014*x**4
def surface_point(v):return np.array([v[0]*1.35,v[1]*1.35,landscape(*v)*1.9])

def parameter_line(y=3.2):
    return VGroup(Line([-3.1,y,0],[3.1,y,0],color=WEIGHT,stroke_width=3),Dot([-3.1,y,0],color=WEIGHT,radius=.1),Dot([3.1,y,0],color=SPARSE,radius=.1),
                  t('Model A',y+.6,-2.8,size=24,color=WEIGHT,width=2.3),t('Model B',y+.6,2.8,size=24,color=SPARSE,width=2.3),t('θ(λ) = (1−λ)θA + λθB',1.95,size=29,color=ACCENT))

def loss_panel(good=True):
    ax=Axes(x_range=[0,1,.25],y_range=[0,1,.25],x_length=6.2,y_length=2.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.5}).move_to([0,-1.05,0])
    fn=low_loss if good else barrier
    curve=ax.plot(fn,x_range=[0,1,.01],color=GOOD if good else PRUNE,stroke_width=3)
    ends=VGroup(*[Dot(ax.c2p(lam,fn(lam)),radius=.085,color=WEIGHT if lam==0 else SPARSE) for lam in [0,1]])
    return VGroup(parameter_line(),ax,curve,ends,t('직선 경로 위의 손실 L(θ(λ))',.85,size=24,color=GOOD if good else PRUNE),
                  t('0                     0.5                     1',-2.75,size=22,color=MUTED),t('λ · 파라미터 혼합 비율',-3.4,size=24,color=MUTED),
                  t('설명용 모형 · 성능 실측 아님',-4.45,size=21,color=MUTED))

def compare_paths():
    g=VGroup(parameter_line())
    for x,good in [(-1.95,False),(1.95,True)]:
        ax=Axes(x_range=[0,1,.5],y_range=[0,1,.5],x_length=3.2,y_length=2.8,tips=False,axis_config={'color':MUTED,'stroke_width':1.3}).move_to([x,-.9,0])
        fn=low_loss if good else barrier
        g.add(ax,ax.plot(fn,x_range=[0,1,.01],color=GOOD if good else PRUNE,stroke_width=3),t('낮은 직선 경로' if good else '중간 손실 장벽',1.15,x,size=23,color=GOOD if good else PRUNE,width=3.5),t('A      중간      B',-2.8,x,size=21,color=MUTED,width=3.4))
        if good:g.add(Dot(ax.c2p(.5,fn(.5)),color=ACCENT,radius=.09))
    g.add(t('같은 출발점만으로는 충분하지 않음',-3.7,size=25,color=MUTED),t('서로 다른 설명용 경우 · 성능 실측 아님',-4.45,size=21,color=MUTED))
    return g

def fork():
    root=box('Pretrained θ₀',0,3,4.3,1,color=GOOD)
    aa=box('Model A · θA',-2,0,3.4,1,color=WEIGHT);bb=box('Model B · θB',2,0,3.4,1,color=SPARSE)
    return VGroup(root,Arrow(root.get_bottom(),aa.get_top(),buff=.1,color=WEIGHT),Arrow(root.get_bottom(),bb.get_top(),buff=.1,color=SPARSE),aa,bb,
                  t('설정 A',1.6,-2,size=24,color=WEIGHT,width=2),t('설정 B',1.6,2,size=24,color=SPARSE,width=2),
                  t('같은 구조 · 같은 파라미터 대응',-1.75,size=29,color=ACCENT),t('같은 출발점이어도 평균 성능은 검증해야 함',-3.5,size=23,color=MUTED))

def average():
    return VGroup(box('θA = [2, 4, 6]',-2,2.7,3.6,1,color=WEIGHT),box('θB = [4, 2, 8]',2,2.7,3.6,1,color=SPARSE),
                  Arrow([-2,2,0],[-.5,.65,0],color=MUTED),Arrow([2,2,0],[.5,.65,0],color=MUTED),
                  box('θsoup = [3, 3, 7]',0,0,6,1.2,color=GOOD),t('θsoup = (θA + θB) / 2',-1.65,size=34,color=ACCENT),
                  t('대응하는 좌표끼리 평균 · 숫자는 설명용',-3.1,size=23,color=MUTED),t('평균 모델 생성에 추가 경사하강법은 불필요',-4.3,size=23,color=GOOD))

def ensemble():
    return VGroup(t('예측 평균',3.9,-2,size=28,color=SPARSE,width=3.5),t('가중치 평균',3.9,2,size=28,color=WEIGHT,width=3.5),
                  box('입력 x',-2,2.7,3, .75,MUTED),box('입력 x',2,2.7,3,.75,MUTED),
                  box('Model A',-2.9,1.1,1.7,.9,SPARSE),box('Model B',-1.1,1.1,1.7,.9,SPARSE),box('Model Soup',2,1.1,3,.9,WEIGHT),
                  Arrow([-2,2.2,0],[-2.9,1.7,0],buff=.05,color=MUTED),Arrow([-2,2.2,0],[-1.1,1.7,0],buff=.05,color=MUTED),Arrow([2,2.2,0],[2,1.7,0],buff=.05,color=MUTED),
                  t('2개 모델 실행',-.1,-2,size=24,color=SPARSE,width=3.6),t('1개 모델 실행',-.1,2,size=24,color=WEIGHT,width=3.6),
                  t('f평균가중치(x) ≠ 평균예측(x)',-1.8,size=31,color=ACCENT),t('일반적으로 서로 다른 계산',-3,size=25,color=MUTED),t('추론 비용은 같은 구조의 단일 모델 기준',-4.3,size=22,color=MUTED))

class ModelSoupsGeometry(ThreeDScene):
    def chrome(self,i):
        titles=['좋은 파라미터를 찾아가는 학습','골짜기 아래의 한 지점','좋은 해가 영역에 있다면?','같은 사전학습 모델에서 분기','좋은 성능 · 서로 다른 파라미터','대응하는 가중치를 절반씩 평균',
                '추가 학습 없이 하나의 모델로','Model Soups','가중치 평균은 왜 의미가 있을까?','모델 하나를 파라미터 점 하나로','직선 위의 모든 점도 모델 하나','양 끝이 좋아도 중간은 모른다','높은 손실 장벽이 있을 수도',
                '일부 파인튜닝 결과에서는','직선에서도 낮은 손실이 유지된다','하나의 넓은 골짜기라는 해석','직선의 중간점도 좋은 모델로','기하학적 성질을 이용하는 평균','예측 평균과 가중치 평균의 차이','단일 모델로 추론 비용을 유지','모든 평균이 좋은 것은 아니다',
                '좋은 해의 위치보다 그 사이를 본다','찾은 두 점만 좋은 것은 아니다','그 사이에도 좋은 해가 있을 수 있다','좋은 해는 영역일 수 있다']
        return VGroup(t('신경망의 역설  /  05',7.35,size=20,color=MUTED),t('좋은 해는 점이 아니라\n영역이다?',6.45,size=33),Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),
                      t(titles[i],5.05,size=25,color=ACCENT),t('Model Soups · 파라미터 공간의 기하학',-7.45,size=18,color=MUTED))

    def world(self,i):
        self.set_camera_orientation(phi=65*DEGREES,theta=-60*DEGREES,zoom=1)
        surf=Surface(lambda x,y:surface_point([x,y]),u_range=[-2.1,2.1],v_range=[-1.8,1.8],resolution=(16,12),checkerboard_colors=[ManimColor('#18394C'),ManimColor('#21485B')],fill_opacity=.75,stroke_color=WEIGHT,stroke_width=.35,stroke_opacity=.3)
        axes=ThreeDAxes(x_range=[-3,3,1],y_range=[-2.6,2.6,1],z_range=[0,2.7,1],x_length=6,y_length=5.2,z_length=2.7,tips=False,axis_config={'color':MUTED,'stroke_width':1})
        self.add(axes,surf)
        aa=Dot3D(surface_point(A)+OUT*.04,radius=.075,color=WEIGHT);bb=Dot3D(surface_point(B)+OUT*.04,radius=.075,color=SPARSE)
        if i in [0,1]:
            dot=Dot3D(surface_point(START)+OUT*.04,radius=.09,color=ACCENT);self.add(dot)
            path=ParametricFunction(lambda u:surface_point((1-u)*START+u*A)+OUT*.04,t_range=[0,1],color=ACCENT,stroke_width=3)
            self.play(Create(path),MoveAlongPath(dot,path),run_time=2.2)
            self.add(aa)
        else:self.add(aa,bb)
        label_a=Text('A',font=FONT,font_size=26,color=WEIGHT).move_to(surface_point(A)+UP*.25+OUT*.2)
        self.add_fixed_orientation_mobjects(label_a)
        if i not in [0,1]:
            label_b=Text('B',font=FONT,font_size=26,color=SPARSE).move_to(surface_point(B)+UP*.25+OUT*.2)
            self.add_fixed_orientation_mobjects(label_b)
        if i in [2,15,24]:
            line=ParametricFunction(lambda u:surface_point(theta(u))+OUT*.06,t_range=[0,1],color=ACCENT,stroke_width=3)
            self.play(Create(line),run_time=.7)
            self.add(Dot3D(surface_point(theta(.5))+OUT*.08,radius=.09,color=GOOD))
            if i in [15,24]:
                label_soup=Text('Model Soup',font=FONT,font_size=23,color=ACCENT).move_to(surface_point(theta(.5))+UP*.35+OUT*.35)
                self.add_fixed_orientation_mobjects(label_soup)
        if i==24:
            # Recolor the original mesh, avoiding intersecting coplanar surfaces.
            region=[]
            for face in surf:
                cx,cy=face.get_center()[:2]/1.35
                if abs(cx)<1.7 and abs(cy-.13*np.sin(1.4*cx))<.8*(1-.12*cx*cx):
                    region.append(face)
            self.play(*[face.animate.set_fill(GOOD,opacity=.85) for face in region],run_time=.6)
            for x,y in EXTRAS:
                self.add(Dot3D(surface_point([x,y])+OUT*.08,radius=.055,color=WEIGHT))
        self.move_camera(theta=-45*DEGREES,phi=(45 if i==24 else 65)*DEGREES,run_time=.7)

    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps=['학습은 수많은 파라미터 중에서\n좋은 값을 찾아가는 과정입니다.','경사하강법이 골짜기 아래에서\n하나의 최솟값을 찾는다고 생각합니다.','좋은 해가 하나의 점이 아니라\n넓은 영역에 있다면 어떨까요?',
              '같은 사전학습 모델에서 출발해\n서로 다른 설정으로 파인튜닝합니다.','둘 다 좋은 성능을 보이지만\n최종 파라미터는 다릅니다.','두 모델의 파라미터를\n절반씩 평균내면 어떻게 될까요?',
              '추가 학습 없이 좋은 성능을 보이고\n때로는 개별 모델보다 정확할 수 있습니다.','이것이 Model Soups입니다.','왜 단순한 가중치 평균으로\n좋은 모델이 만들어질까요?',
              '파라미터 공간에서는\n모델 하나를 점 하나로 표현합니다.','두 점을 잇는 직선 위의 모든 점은\n서로 다른 가중치를 가진 모델입니다.','양 끝이 좋은 해라도\n중간이 좋다는 보장은 없습니다.','중간에 높은 손실의\n장벽이 있을 수도 있습니다.',
              '공통 초기 모델에서 출발한 일부\n파인튜닝 결과는 다르게 나타납니다.','두 모델 사이의 직선에서도\n손실이 낮게 유지됩니다.','두 해가 같은 넓은 골짜기에\n있는 것처럼 해석할 수 있습니다.','이 경우 직선의 중간점에서도\n좋은 모델을 얻을 수 있습니다.',
              'Model Soups는 이러한\n기하학적 성질을 이용합니다.','예측을 평균내는 대신\n가중치 자체를 평균내 하나의 모델을 만듭니다.','적절한 조건에서 추론 비용을 늘리지 않고\n일반화 성능을 개선할 수 있습니다.',
              '모든 평균이 좋지는 않습니다.\n호환되는 낮은 손실 영역인지가 중요합니다.','여기서 흥미로운\n사실이 드러납니다.','경사하강법이 찾은 해만\n유일하게 좋은 지점일 필요는 없습니다.','그 해들 사이에도\n좋은 성능을 유지하는 영역이 있을 수 있습니다.',
              '좋은 해는 고립된 점이 아니라\n파라미터 공간의 영역일 수도 있습니다.']
        for i,s in enumerate(data['segments']):
            self.clear()
            overlay=VGroup(self.chrome(i),t(caps[i],-6.15,size=24))
            if i in SURFACE_SCENES:
                overlay.add(t('고차원 파라미터 공간의 2차원 단면 · 설명용 지형',-3.9,size=20,color=MUTED),t('A · B · 중간점의 국소 저손실 해석' if i>=2 else '표면 높이: 손실 · 점: 파라미터',-4.55,size=22,color=GOOD))
                if i==24:overlay.add(t('좋은 해 전체의 볼록성을 보장하지 않음',-3.1,size=21,color=MUTED))
                self.add_fixed_in_frame_mobjects(overlay);self.world(i)
            else:
                self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
                p=self.panel(i)
                self.add_fixed_in_frame_mobjects(overlay,p)
                self.play(FadeIn(p),run_time=.3)
                if i in [10,14,16,22,23]:
                    tracker=ValueTracker(.1 if i==10 else 0)
                    fn=barrier if i==10 else low_loss
                    top=always_redraw(lambda:Dot([-3.1+6.2*tracker.get_value(),3.2,0],color=ACCENT,radius=.11))
                    bottom=always_redraw(lambda:Dot(p[1].c2p(tracker.get_value(),fn(tracker.get_value())),color=ACCENT,radius=.1))
                    self.add_fixed_in_frame_mobjects(top,bottom)
                    self.play(tracker.animate.set_value(.5 if i in [16,22,23] else .9),run_time=1.2)
                    top.clear_updaters();bottom.clear_updaters()
                    if i==16:self.add_fixed_in_frame_mobjects(t('λ = 0.5 · Model Soup',-3.95,size=26,color=GOOD))
                if i==12:
                    dot=Dot(p[1].c2p(.5,barrier(.5)),color=PRUNE,radius=.1)
                    self.add_fixed_in_frame_mobjects(dot);self.play(Flash(dot,color=PRUNE,flash_radius=.3),run_time=.6)
                if i==6:self.play(Indicate(p[1],color=GOOD),run_time=.6)
            remaining=s['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-118)<1/30+.001

    def panel(self,i):
        if i in [3,4]:return fork()
        if i in [5,7,8,17]:return average()
        if i==6:return VGroup(box('평균 가중치 θsoup',0,2.8,6,1.1,GOOD),box('단일 모델로 예측',0,.1,6,1.1,WEIGHT),Arrow([0,2.1,0],[0,.8,0],buff=.1,color=MUTED),t('추가 경사하강법 없이 생성',-1.7,size=30,color=ACCENT),t('좋은 성능을 얻을 수 있음 · 조건부 결과',-3.1,size=24,color=MUTED),t('성능 향상은 검증 데이터로 확인',-4.3,size=24,color=GOOD))
        if i==13:return compare_paths()
        if i in [9,10,11,12,14,16,22,23]:
            p=loss_panel(i not in [10,11,12])
            if i==9:p[2].set_opacity(0);p[3].set_opacity(0);p[4].set_opacity(0)
            return p
        if i in [18,19]:return ensemble()
        if i==20:return VGroup(box('공통 사전학습 모델 · 호환되는 좌표',0,3,7.5,1,WEIGHT),box('직선 보간에서도 낮은 손실',0,1.25,7.5,1,GOOD),box('검증 데이터로 후보와 평균을 평가',0,-.5,7.5,1,ACCENT),t('같은 초기 모델이라는 사실만으로는 충분하지 않음',-2.4,size=23,color=MUTED),t('낮은 손실 ≠ 정확도 향상의 보장',-4,size=26,color=PRUNE))
        return VGroup(parameter_line(2.5),t('찾은 두 점',.3,size=34,color=WEIGHT),t('그 사이의 해는 어떨까?',-1.3,size=37,color=ACCENT),t('전체 좋은 해 집합의 볼록성을 가정하지 않음',-3.8,size=23,color=MUTED))
