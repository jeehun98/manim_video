"""9:16 edition of the approved 164-second narration; independently composed."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc01_same_answers.scene import *

config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1920'))
config.frame_width=9;config.frame_height=16

class SameAnswersShorts(SameAnswersDifferentAlgorithms):
    def construct(self):
        data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        assert data['duration']==164
        self.fixed=VGroup(t('신경망 내부의 계산  /  01',y=7.4,size=20,color=MUTED,width=7.6),
            t('정답만 가르쳤는데\nAI는 어떻게 풀이를 배울까?',y=6.55,size=29,width=7.5),
            Line(p(-3.9,5.8),p(3.9,5.8),color=ZERO),
            RoundedRectangle(width=7.9,height=1.85,corner_radius=.12,stroke_width=0,
                fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2)),
            t('내부 연결·모델 수·비율은 개념도',y=-7.45,size=16,color=MUTED,width=7.5))
        self.add(self.fixed);self.stage=VGroup();self.heading=VGroup();self.caption=VGroup()
        for index,seg in enumerate(data['segments']):
            self.to(seg['start'])
            for obj in list(self.mobjects):
                if obj is not self.fixed:self.remove(obj)
            self.heading=t(f'{index+1:02}  {seg["title"]}',y=5.25,size=24,color=ACCENT,width=7.7)
            self.stage=VGroup();self.add(self.heading)
            callbacks=self.build(index)
            self.caption=self.caption_obj(seg['cues'][0]['text']);self.add(self.caption)
            self.check_layout(index)
            self.play(FadeIn(self.stage,shift=UP*.08),run_time=.3)
            for local,cue in enumerate(seg['cues']):
                self.to(cue['start']);self.remove(self.caption)
                self.caption=self.caption_obj(cue['text']);self.add(self.caption)
                if local in callbacks:callbacks[local]()
                self.to(cue['end'])
        self.to(164)
    def caption_obj(self,s):
        lines=textwrap.fill(s,width=29,break_long_words=False,break_on_hyphens=False)
        obj=t(lines,y=-6.2,size=25,width=7.2)
        if obj.height>1.5:obj.scale_to_fit_height(1.5)
        return obj
    def note(self,s):
        self.show(t(s,y=-4.85,size=17,color=MUTED,width=7.6))
    def check_layout(self,k):
        for obj in self.stage:
            if obj.get_left()[0]<-4.0 or obj.get_right()[0]>4.0 or obj.get_top()[1]>4.85 or obj.get_bottom()[1]<-5.1:
                raise ValueError(f'Portrait scene {k+1} outside safe area: {obj}')
    def build(self,k):
        cb={}
        if k==0:
            seq=BracketSequence('()()',y=3.6,color=INK)
            net=NeuralNetwork(0,.9,w=4.2,h=1.8)
            labels=VGroup(card('()()  →  올바름',y=-1.05,w=6.2,color=GOOD),
                card('(()   →  틀림',y=-2.35,w=6.2,color=PRUNE))
            self.show(seq,net,labels,arr(0,3.05,0,2.1),arr(0,-.15,0,-.55))
            self.note('입력과 정답만 제공 · 풀이 과정 없음')
            cb={0:lambda:net.pulse(self),1:lambda:self.pulse(labels)}
        elif k==1:
            net=NeuralNetwork(0,1,w=4.6,h=2.1)
            yes=card('정답  ✓',y=3.4,w=6,color=GOOD,size=32)
            no=card('풀이 방법  ?',y=-1.55,w=6,color=ACCENT,size=32)
            self.show(net,yes,no,arr(0,2.9,0,2.3),arr(0,-.2,0,-1),
                t('개수 비교?     순서 확인?',y=-3.3,size=25,color=MUTED,width=7.2))
            cb={0:lambda:self.pulse(no)}
        elif k==2:
            net=NeuralNetwork(0,2.4,w=4,h=1.8)
            wrong=card('예측: 틀림',-1.8,.65,3.2,.75,PRUNE,24)
            truth=card('정답: 올바름',1.8,.65,3.2,.75,GOOD,24)
            err=card('오차 → 가중치 갱신',y=-.65,w=6.7,color=ACCENT)
            a=card('가능한 계산 A',y=-2.25,w=6.2,color=COUNT)
            b=card('가능한 계산 B',y=-3.55,w=6.2,color=NEST)
            self.show(net,wrong,truth,err,a,b)
            cb={0:lambda:self.play(Indicate(err),net.edges.animate.set_stroke(width=1.8,opacity=.65),run_time=1),
                1:lambda:net.pulse(self),2:lambda:self.pulse(a,b)}
        elif k==3:
            counter=CountingAlgorithm(x=0,y=1.3)
            self.show(t('A · Equal-Count',y=3.8,size=32,color=COUNT),counter,
                card('순서는 검사하지 않는다',y=-1.5,w=6.8,color=COUNT,size=27),
                t('여는 수 = 닫는 수',y=-3.1,size=29,color=COUNT))
            self.note('설명용 후보 규칙 · 중첩의 정답 기준과 구별')
            cb={0:lambda:counter.run(self)}
        elif k==4:
            tracker=DepthTracker(x=0,y=1.05)
            self.show(t('B · Nested',y=3.8,size=32,color=NEST),tracker,
                t('여는 괄호 +1    닫는 괄호 −1',y=-1.55,size=26,color=NEST,width=7.4),
                card('모든 깊이 ≥ 0',y=-2.8,w=6.7,color=GOOD),
                card('마지막 깊이 = 0',y=-3.85,w=6.7,color=GOOD))
            cb={0:lambda:self.pulse(self.stage[0]),1:lambda:tracker.run(self),2:lambda:self.pulse(self.stage[3],self.stage[4])}
        elif k==5:
            rows=VGroup(t('훈련 예시       A       B',y=3.7,size=24,color=MUTED,width=7.4))
            for i,(s,v,color) in enumerate([('()()','수락',GOOD),('(())','수락',GOOD),('(()','거부',PRUNE),('())','거부',PRUNE)]):
                yy=2.6-i*1.1
                rows.add(card(s,-2.1,yy,2,.7,INK,27,True),t(v,.7,yy,26,color,2),t(v,2.6,yy,26,color,2))
            common=card('둘 다 훈련 예시 모두 정답',y=-2.1,w=7.2,color=GOOD,size=26)
            self.show(rows,common,t('A · 개수 비교',-1.9,-3.45,23,COUNT,3.6),t('B · 중첩 확인',1.9,-3.45,23,NEST,3.6))
            self.note('교육용 예시 · 논문 전체 데이터셋 재현 아님')
            cb={0:lambda:self.pulse(rows),1:lambda:self.pulse(common),2:lambda:self.pulse(self.stage[2],self.stage[3])}
        elif k==6:
            count=CountingAlgorithm('())(',x=0,y=2.35)
            depth=DepthTracker('())(',x=0,y=-1.6)
            self.show(t('A · 개수 비교',y=4.25,size=25,color=COUNT),count,
                Line(p(-3.5,.65),p(3.5,.65),color=ZERO),
                t('B · 중첩 확인',y=.3,size=25,color=NEST),depth)
            for seq in (count.seq,depth.seq):
                for token in seq:token[0].set_stroke(color=ACCENT)
            self.note('새 입력 / OOD · 실제 정답은 올바르지 않음')
            cb={0:lambda:self.pulse(count.seq,depth.seq),1:lambda:count.run(self),2:lambda:depth.run(self)}
        elif k==7:
            self.show(card('훈련에서는 둘 다 정답',y=3.7,w=7,color=GOOD,size=29),
                arr(-.7,3.15,-2,2),arr(.7,3.15,2,2),
                card('개수 비교',-2,1.3,3.4,.9,COUNT),card('중첩 확인',2,1.3,3.4,.9,NEST),
                card('새 입력\n올바름',-2,-.7,3.4,1.4,COUNT),card('새 입력\n올바르지 않음',2,-.7,3.4,1.4,PRUNE,23),
                t('같은 훈련 정답\n≠\n같은 일반화 규칙',y=-3.2,size=30,color=ACCENT,width=7.4))
            cb={0:lambda:self.pulse(self.stage[-1])}
        elif k==8:
            pop=ModelPopulation(0,.65)
            self.show(t('Patterning · 괄호 분류 연구',y=3.75,size=28,width=7.5),
                card('같은 훈련 분포로 학습',y=2.4,w=7,color=GOOD),pop,
                arr(-.6,-.35,-1.8,-1.4,COUNT),arr(.6,-.35,1.8,-1.4,NEST),
                card('개수 비교에\n대응하는 행동',-1.95,-2.25,3.5,1.35,COUNT,23),
                card('중첩 판별에\n대응하는 행동',1.95,-2.25,3.5,1.35,NEST,23))
            self.note('연구 결과의 개념도 · 모델 비율은 실제 통계 아님')
            cb={0:lambda:self.pulse(self.stage[1]),1:lambda:self.pulse(pop)}
        elif k==9:
            net=NeuralNetwork(0,1.8,w=5.2,h=2.3)
            code=t('if   for   count',y=1.8,size=33,color=MUTED,width=6)
            self.show(net,code,card('가중치 + 활성화',y=-.5,w=6.5,color=NEST,size=29),
                t('입력 → 층별 변환 → 출력',y=-2,size=27,width=7.5),
                t('알고리즘\n= 학습된 계산 규칙',y=-3.5,size=30,color=ACCENT,width=7.5))
            self.note('실제 회로의 측정·추출 결과가 아닌 개념도')
            cb={0:lambda:self.pulse(self.stage[4]),1:lambda:self.play(FadeOut(code),run_time=.8),2:lambda:net.pulse(self)}
        elif k==10:
            net=NeuralNetwork(0,1.1,w=4,h=1.8)
            boxes=VGroup(card('모델 구조',-1.95,3.5,3.5,.8,NEST),card('초기 가중치',1.95,3.5,3.5,.8,NEST),
                card('최적화 과정',y=-1,w=7,color=NEST),card('데이터 분포',y=-2.5,w=7,color=ACCENT))
            self.show(net,boxes,t('어떤 계산 규칙이 형성되는가?',y=-3.95,size=26,width=7.5))
            def conditions():
                for box in boxes:self.pulse(box)
            cb={0:lambda:net.pulse(self),1:conditions}
        elif k==11:
            weighting=DistributionWeighting(0,2.7)
            training=card('비중 변경 → 다시 학습',y=.35,w=7,color=ACCENT,size=27)
            pop=ModelPopulation(0,-1.7);target=pop.copy();pop.set_opacity(0)
            self.show(weighting,training,pop,t('정답 라벨은 유지',y=4.25,size=25,width=7.5),
                arr(0,1.35,0,.9,ACCENT),arr(0,-.2,0,-.85,ACCENT),
                t('새 모델 집단의\n일반화 경향 변화',y=-3.4,size=28,color=NEST,width=7.5))
            self.note('샘플 비중·모델 수·비율은 설명용 개념도')
            def weigh():weighting.reweight(self);self.pulse(training)
            cb={0:lambda:self.pulse(self.stage[3]),1:weigh,2:lambda:self.play(Transform(pop,target),run_time=1.3)}
        elif k==12:
            left=card('정답을 맞히는가?',y=3.3,w=7,color=GOOD,size=31)
            right=card('어떤 계산을 배우는가?',y=.1,w=7,color=NEST,size=29)
            self.show(left,t('훈련 목표와 예측 성능',y=2.05,size=27,color=GOOD,width=7.5),right,
                t('학습된 규칙과 일반화',y=-1.2,size=27,color=NEST,width=7.5),
                card('데이터 분포\n↓\n학습되는 계산의 경향',y=-3.2,w=7,h=2,color=ACCENT,size=25))
            cb={0:lambda:self.pulse(left),1:lambda:self.pulse(right,self.stage[4])}
        elif k==13:
            weighting=DistributionWeighting(0,2.7)
            training=card('분포 변경 → 다시 학습',y=.4,w=7,color=ACCENT,size=26)
            pop=ModelPopulation(0,-1.25,[NEST,COUNT,NEST,NEST,NEST,COUNT,NEST,NEST]);target=pop.copy();pop.set_opacity(0)
            self.show(weighting,training,pop,arr(0,1.35,0,.95,ACCENT),arr(0,-.1,0,-.5,ACCENT),
                t('Patterning',y=-2.9,size=33,color=ACCENT,width=7.4),
                t('정답을 지정하는 것\n≠ 풀이까지 지정하는 것',y=-4.1,size=27,width=7.5))
            def retrain():weighting.reweight(self);self.pulse(training);self.play(Transform(pop,target),run_time=.6)
            cb={0:retrain,1:lambda:self.pulse(self.stage[5]),2:lambda:self.pulse(self.stage[6])}
        return cb
